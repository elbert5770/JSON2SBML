using SBMLImporter
using Catalyst, GraphMakie, NetworkLayout
using GLMakie
using ModelingToolkit
using OrdinaryDiffEq

function suvr(oligo, proto, plaque, C1=2.5, C2=400000, C3=1.3, Hill=3.5)
    """
    Calculate SUVR using the provided formula.
    
    Parameters:
    oligo, proto, plaque: input oligomer values
    X1, X2, X3: parameters to fit
    C1, C2, C3, Hill: constants from the formula
    
    Returns:
    SUVR: predicted SUVR value
    """
    numerator = oligo .+ proto .+ C3 .*  24.0 .* plaque
    denominator = numerator.^Hill .+ C2.^Hill
    
    if denominator == 0
        return 1.0  # Avoid division by zero
    end
    suvr = 1.0 .+ C1 .* (numerator.^Hill) ./ denominator
    return suvr
end

function main()
    # filename = "C:\\Users\\elber\\Documents\\git\\PBPK_SBML_JAX\\models\\Geerts\\generated\\sbml\\combined_master_model.xml"
    # filename = "C:\\Users\\elber\\Documents\\git\\PBPK_SBML_JAX\\models\\Geerts\\generated\\sbml\\qsp_model.xml"
    # filename = "C:\\Users\\elber\\Documents\\git\\Elbert_Patterson\\Elbert_Patterson_Bateman_2015\\Geerts_model_antimony.sbml"
    # filename = "C:\\Users\\elber\\Documents\\git\\Elbert_Patterson\\Elbert_Patterson_Bateman_2015\\combined_master_model.xml"
    filename = "Antimony_PBPK_model.xml"
    prn, cb = load_SBML(filename, massaction=true)
    rs = prn.rn
    @show typeof(rs)
    @show rs.eqs[1]
    @show rs.rxs[1]
        @show rs.species[1]
    @show rs.unknowns[1]
    # lrs = latexify(rs, form = :ode)
    # display(lrs)

    # Catalyst.plot_network(rs)

    
    sys = structural_simplify(convert(ODESystem, prn.rn))

    @show unknowns(sys)

    # # Print the differential equations from sys
    # println("\n=== Differential Equations from sys ===")
    # for (i, eq) in enumerate(equations(sys))
    #     println("Equation $i: $eq")
    # end


    tspan = (0.0, 100.0*365*24)
    # oprob = ODEProblem(sys, prn.u0, tspan, prn.p)
    # oprob = ODEProblem(sys, prn.u0, tspan, prn.p, jac=true)
    @show  prn.p
    @show parameters(prn)
    oprob = ODEProblem(sys, prn.u0, tspan, prn.p, jac=true, sparse=true)
    # You can access the parameters in an ODEProblem via `oprob.p`, which is typically a NamedTuple or Dict.
    # For example, to access the value of :k_O1_O2_AB42_ISF:
    @show oprob.p
    # Print the differential equations from oprob
    # println("\n=== Differential Equations from oprob ===")
    # for (i, eq) in enumerate(equations(oprob.f.sys))
    #     println("Equation $i: $eq")
    # end

    # Alternative way to print equations from oprob
    println("\n=== Alternative: Equations from oprob.f.sys ===")
    # @show equations(oprob.f.sys)

    @time sol = solve(oprob, Rodas5P())

    # tspan = (0.0, 1.0*365*24)
    # oprob = ODEProblem(sys, sol.u[end], tspan, prn.p, jac=true)
    # sol = solve(oprob, Rodas5P())
    # println(sol[:AB40_Monomer])
    # println(sol[:AB42_O1_ISF])
    # println(sol[:APP])
    fig = Figure()
    ax1 = Axis(fig[1, 1], xlabel="Time", ylabel="Concentration", title="Oligomers")
    ax2 = Axis(fig[1, 2], xlabel="Time", ylabel="Concentration", title="Proto")
    ax3 = Axis(fig[2, 1], xlabel="Time", ylabel="Concentration", title="SUVR")
    ax4 = Axis(fig[2, 2], xlabel="Time", ylabel="Concentration", title="AB42_O1_ISF and AB42_O25_ISF")
    # sol_70 = sol(70*24*365)
    # @show typeof(sol_70)
    
    # # Get the symbol-to-index mapping from the system
    # symbol_to_index = Dict{Symbol, Int}()
    # for (i, sym) in enumerate(unknowns(sys))
    #     symbol_to_index[Symbol(sym)] = i
    # end
    
    # # Print the mapping for debugging
    # println("\n=== Symbol to Index Mapping ===")
    # println("All symbols in system:")
    # for (sym, idx) in symbol_to_index
    #     println("$sym -> $idx")
    # end
    
    # println("\nAB42 symbols in system:")
    # for (sym, idx) in symbol_to_index
    #     if contains(string(sym), "AB42")
    #         println("$sym -> $idx")
    #     end
    # end
    
    # oligomer_sum = 0.0  
    # for i in 2:17
    #     # Try different possible naming patterns
    #     possible_names = [
    #         Symbol(string("AB42_O", i, "_ISF")),
    #         Symbol(string("AB42_O", i)),
    #         Symbol(string("AB42_O", i, "_ISF"))
    #     ]
        
    #     found = false
    #     for symbol_name in possible_names
    #         if haskey(symbol_to_index, symbol_name)
    #             oligomer_sum += sol_70[symbol_to_index[symbol_name]]
    #             found = true
    #             break
    #         end
    #     end
        
    #     if !found
    #         println("Warning: Symbol AB42_O$i not found in solution")
    #     end
    # end
    # oligomer_weighted_sum = 0.0 
    # for i in 2:17
    #     # Try different possible naming patterns
    #     possible_names = [
    #         Symbol(string("AB42_O", i, "_ISF")),
    #         Symbol(string("AB42_O", i)),
    #         Symbol(string("AB42_O", i, "_ISF"))
    #     ]
        
    #     found = false
    #     for symbol_name in possible_names
    #         if haskey(symbol_to_index, symbol_name)
    #             oligomer_weighted_sum += sol_70[symbol_to_index[symbol_name]] * (i-1)
    #             found = true
    #             break
    #         end
    #     end
        
    #     if !found
    #         println("Warning: Symbol AB42_O$i not found in solution")
    #     end
    # end
    # proto_sum = 0.0
    # for i in 18:24
    #     # Try different possible naming patterns
    #     possible_names = [
    #         Symbol(string("AB42_O", i, "_ISF")),
    #         Symbol(string("AB42_O", i)),
    #         Symbol(string("AB42_O", i, "_ISF"))
    #     ]
        
    #     found = false
    #     for symbol_name in possible_names
    #         if haskey(symbol_to_index, symbol_name)
    #             proto_sum += sol_70[symbol_to_index[symbol_name]]
    #             found = true
    #             break
    #         end
    #     end
        
    #     if !found
    #         println("Warning: Symbol AB42_O$i not found in solution")
    #     end
    # end
    # proto_weighted_sum = 0.0
    # for i in 18:24
    #     # Try different possible naming patterns
    #     possible_names = [
    #         Symbol(string("AB42_O", i, "_ISF")),
    #         Symbol(string("AB42_O", i)),
    #         Symbol(string("AB42_O", i, "_ISF"))
    #     ]
        
    #     found = false
    #     for symbol_name in possible_names
    #         if haskey(symbol_to_index, symbol_name)
    #             proto_weighted_sum += sol_70[symbol_to_index[symbol_name]] * (i-1)
    #             found = true
    #             break
    #         end
    #     end
        
    #     if !found
    #         println("Warning: Symbol AB42_O$i not found in solution")
    #     end
    # end
    # @show oligomer_sum
    # @show oligomer_weighted_sum
    # @show proto_sum
    # @show proto_weighted_sum
    oligomer_sum = sol[:AB42_O2_ISF]./0.2505
    for i in 3:17
        oligomer_sum .+= sol[Symbol(string("AB42_O", i, "_ISF"))]
    end
    lines!(ax1, sol.t/24/365, oligomer_sum, label="Oligomers")
    oligomer_weighted_sum = sol[:AB42_O2_ISF]./0.2505 * 1
    for i in 3:17
        oligomer_weighted_sum .+= sol[Symbol(string("AB42_O", i, "_ISF"))]./0.2505 * (i-1)
    end
    lines!(ax1, sol.t/24/365, oligomer_weighted_sum, label="Oligomers weighted")
    vlines!(ax1, [70.0], color=:black, linestyle=:dash, linewidth=1.5)
    plot!(ax1, [70], [12000], color=:orange, markersize=14)
    axislegend(ax1, position=:lt)

    proto_sum = sol[:AB42_O18_ISF]./0.2505
    for i in 19:24
        proto_sum .+= sol[Symbol(string("AB42_O", i, "_ISF"))]
    end
    lines!(ax2, sol.t/24/365, proto_sum, label="Proto")
    proto_weighted_sum = sol[:AB42_O18_ISF]./0.2505 * 17
    for i in 19:24  
        proto_weighted_sum .+= sol[Symbol(string("AB42_O", i, "_ISF"))]./0.2505 * (i-1)
    end
    lines!(ax2, sol.t/24/365, proto_weighted_sum, label="Proto weighted")
    vlines!(ax2, [70.0], color=:black, linestyle=:dash, linewidth=1.5)
    plot!(ax2, [70], [70000], color=:orange, markersize=14)
    axislegend(ax2, position=:lt, fontsize=7)
    plaque_sum = sol[:AB42_O25_ISF]
    SUVR = suvr(oligomer_weighted_sum, proto_weighted_sum, plaque_sum)
    lines!(ax3, sol.t/24/365, SUVR, label="SUVR")
    vlines!(ax3, [70.0], color=:black, linestyle=:dash, linewidth=1.5)
    plot!(ax3, [70], [1.4], color=:blue, markersize=14)
    axislegend(ax3, position=:lt)
    # lines!(ax, sol.t/24/365, sol[:APP], label="APP")
    lines!(ax4, sol.t/24/365, sol[:AB42_O1_ISF]./0.2505, label="AB42_O1_ISF")
    lines!(ax4, sol.t/24/365, sol[:AB42_O25_ISF]./0.2505, label="AB42_O25_ISF")
    vlines!(ax4, [70.0], color=:black, linestyle=:dash, linewidth=1.5)
    plot!(ax4, [70], [1.3], color=:blue, markersize=14)
    # plot!(ax4, [70], [5100], color=:orange, markersize=14)
    axislegend(ax4, position=:rt)
    fig
end
main()