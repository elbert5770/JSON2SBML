# using GLMakie

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
    oligo = 12000.0
    proto = 70000.0
    plaque = 20.0
    C1 = 2.5
    C2 = 400000.0
    C3 = 1.3
    Hill = 3.5
    t = 0.0:0.01:100.0
    SUVR = suvr(oligo, proto, plaque, C1, C2, C3, Hill)
    @show SUVR
    # fig = Figure()
    # ax = Axis(fig[1, 1], xlabel="Time", ylabel="SUVR", title="SUVR")
    # lines!(ax, sol.t/24/365, SUVR, label="SUVR")
    # vlines!(ax, [70.0], color=:black, linestyle=:dash, linewidth=1.5)
    # plot!(ax, [70], [1.4], color=:blue, markersize=14)
    # axislegend(ax, position=:lt)
    # fig
end

main()