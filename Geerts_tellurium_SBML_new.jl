using SBMLImporter
using Catalyst, GraphMakie, NetworkLayout
using CairoMakie

# filename = "C:\\Users\\elber\\Documents\\git\\PBPK_SBML_JAX\\models\\Geerts\\generated\\sbml\\combined_master_model.xml"
# filename = "C:\\Users\\elber\\Documents\\git\\PBPK_SBML_JAX\\models\\Geerts\\generated\\sbml\\qsp_model.xml"
# filename = "C:\\Users\\elber\\Documents\\git\\Elbert_Patterson\\Elbert_Patterson_Bateman_2015\\Geerts_model_antimony.sbml"
# filename = "C:\\Users\\elber\\Documents\\git\\Elbert_Patterson\\Elbert_Patterson_Bateman_2015\\combined_master_model.xml"
filename = "C:\\Users\\elber\\Documents\\git\\Elbert_Patterson\\Elbert_Patterson_Bateman_2015\\Antimony_PBPK_model.xml"
prn, cb = load_SBML(filename, massaction=true)
rs = prn.rn
@show typeof(rs)
@show rs.eqs[1]
@show rs.rxs[1]
@show rs.species[1]
@show rs.unknowns[1]
@show rs.ps[1]


# lrs = latexify(rs, form = :ode)
# display(lrs)

# Catalyst.plot_network(rs)

using ModelingToolkit
sys = structural_simplify(convert(ODESystem, prn.rn))

@show unknowns(sys)

# Print the differential equations from sys
println("\n=== Differential Equations from sys ===")
for (i, eq) in enumerate(equations(sys))
    println("Equation $i: $eq")
end

using OrdinaryDiffEq
tspan = (0.0, 100.0*365*24)
oprob = ODEProblem(sys, prn.u0, tspan, prn.p, jac=true)

# Print the differential equations from oprob
println("\n=== Differential Equations from oprob ===")
for (i, eq) in enumerate(equations(oprob.f.sys))
    println("Equation $i: $eq")
end

# Alternative way to print equations from oprob
println("\n=== Alternative: Equations from oprob.f.sys ===")
@show equations(oprob.f.sys)

sol = solve(oprob, Rodas5P())

# tspan = (0.0, 1.0*365*24)
# oprob = ODEProblem(sys, sol.u[end], tspan, prn.p, jac=true)
# sol = solve(oprob, Rodas5P())
# println(sol[:AB40_Monomer])
println(sol[:AB42_O1_ISF])
# println(sol[:APP])
fig = Figure()
ax = Axis(fig[1, 1], xlabel="Time", ylabel="Concentration")

lines!(ax, sol.t/24/365, sol[:AB42_O1_ISF], label="AB42_Monomer")
# lines!(ax, sol.t/24/365, sol[:AB42_Monomer], label="AB42_Monomer")
# lines!(ax, sol.t/24/365, sol[:APP], label="APP")
axislegend(ax, position=:rt)
fig

