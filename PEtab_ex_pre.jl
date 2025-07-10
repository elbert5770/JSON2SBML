using Catalyst, PEtab

rn = @reaction_network begin
    @parameters S0 c3=1.0
    @species S(t)=S0
    c1, S + E --> SE
    c2, SE --> S + E
    c3, SE --> P + E
end
speciemap = [:E => 50.0, :SE => 0.0, :P => 0.0]

@unpack E, S, P = rn
@parameters sigma
obs_sum = PEtabObservable(S + E, 3.0)
obs_p = PEtabObservable(P, sigma)
observables = Dict("obs_p" => obs_p, "obs_sum" => obs_sum)

# Unlike the starting tutorial we do not estimate S0 here as it below
# dictates simulation conditions
p_c1 = PEtabParameter(:c1)
p_c2 = PEtabParameter(:c2)
p_sigma = PEtabParameter(:sigma)
pest = [p_c1, p_c2, p_sigma]

cond1 = Dict(:S0 => 3.0)
cond2 = Dict(:S0 => 5.0)

cond_preeq = Dict(:S0 => 2.0)

conds = Dict("cond_preeq" => cond_preeq, "cond1" => cond1, "cond2" => cond2)

using DataFrames
measurements = DataFrame(simulation_id=["cond1", "cond1", "cond2", "cond2"],
                         pre_eq_id=["cond_preeq", "cond_preeq", "cond_preeq", "cond_preeq"],
                         obs_id=["obs_p", "obs_sum", "obs_p", "obs_sum"],
                         time=[1.0, 10.0, 1.0, 20.0],
                         measurement=[0.7, 0.1, 1.0, 1.5])

model = PEtabModel(rn, observables, measurements, pest;
simulation_conditions = conds)
petab_prob = PEtabODEProblem(model)
x0 = get_x(petab_prob)
    
res = calibrate(petab_prob, x0, IPNewton())
@show res.xmin

using Plots
plot(res, petab_prob; linewidth = 2.0)