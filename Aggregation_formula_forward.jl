using Plots

function calculate_aggregation_rates(j,kf0,kf1,Asymp,Hill)
    KF = (kf1 - Asymp*kf1)/(kf0 - kf1)
    kj_f = (kf0 - Asymp*kf1)*(KF/(j^Hill+KF))+Asymp*kf1
    return kj_f
end
function calculate_aggregation_rates_Hill(j,kf0,kf1,Asymp,Hill)
    KF = (kf1 - Asymp*kf1)/(kf0 - kf1)
    kj_f = (kf0 - Asymp*kf1)*(KF^Hill/(j^Hill+KF^Hill))+Asymp*kf1
    return kj_f
end
function calculate_aggregation_rates_new(j,kf0,kf1,Asymp,Hill)
    KF = (kf0 - Asymp*kf1)/(kf0 - kf1)
    kj_f = (kf0 - Asymp*kf1)*(KF/(j^Hill+KF))+Asymp*kf1
    return kj_f
end
function calculate_aggregation_rates_new_Hill(j,kf0,kf1,Asymp,Hill)
    KF = (kf0 - Asymp*kf1)/(kf0 - kf1)
    kj_f = (kf0 - Asymp*kf1)*(KF^Hill/(j^Hill+KF^Hill))+Asymp*kf1
    return kj_f
end
function main()
    kf0_40 = 50*3.6e-6
    kf1_40 = 20*3.6e-6
    kf0_42 = 990*3.6e-6
    kf1_42 = 38*3.6e-6
    @show kf0_40, kf1_40, kf0_42, kf1_42
    kb0_40 = 0.0027*3600
    kb1_40 = 0.00001/3600*3600
    kb0_42 = 0.0127*3600
    kb1_42 = 0.0003*3600

    Asymp_40 = 0.3
    Asymp_42 = 2
    Hill_40 = 2.5
    Hill_42 = 3.0

    kf0minuskf1_40 = kf0_40 - kf1_40
    kf0minuskf1_42 = kf0_42 - kf1_42

    kb0minuskb1_40 = kb0_40 - kb1_40
    kb0minuskb1_42 = kb0_42 - kb1_42    

    kf0minusAkf1_40 = kf0_40 - Asymp_40*kf1_40
    kf0minusAkf1_42 = kf0_42 - Asymp_42*kf1_42

    kb0minusAkb1_40 = kb0_40 - Asymp_40*kb1_40
    kb0minusAkb1_42 = kb0_42 - Asymp_42*kb1_42

    kf1minusAkf1_40 = kf1_40 - Asymp_40*kf1_40
    kf1minusAkf1_42 = kf1_42 - Asymp_42*kf1_42
    @show kf1minusAkf1_40, kf0minusAkf1_40,kf1minusAkf1_42, kf0minusAkf1_42

    kb1minusAkb1_40 = kb1_40 - Asymp_40*kb1_40
    kb1minusAkb1_42 = kb1_42 - Asymp_42*kb1_42

    KF40 = kf1minusAkf1_40/kf0minuskf1_40
    KB40 = kb1minusAkb1_40/kb0minuskb1_40

    KF42 = kf1minusAkf1_42/kf0minuskf1_42
    KB42 = kb1minusAkb1_42/kb0minuskb1_42

    KF40new = kf0minusAkf1_40/kf0minuskf1_40
    KB40new = kb0minusAkb1_40/kb0minuskb1_40

    KF42new = kf0minusAkf1_42/kf0minuskf1_42
    KB42new = kb0minusAkb1_42/kb0minuskb1_42

    @show KF40, KB40, KF42, KB42, KF40new, KB40new, KF42new, KB42new
    Final_40 = Vector{Float64}(undef,24)*0.0
    Final_42 = Vector{Float64}(undef,24)*0.0
    Final_40_Hill = Vector{Float64}(undef,24)*0.0
    Final_42_Hill = Vector{Float64}(undef,24)*0.0
    Final_40_new = Vector{Float64}(undef,24)*0.0
    Final_42_new = Vector{Float64}(undef,24)*0.0
    Final_40_new_Hill = Vector{Float64}(undef,24)*0.0
    Final_42_new_Hill = Vector{Float64}(undef,24)*0.0
    for i in 1:24
        Final_40[i] = calculate_aggregation_rates(i,kf0_40,kf1_40,Asymp_40,Hill_40)
        Final_42[i] = calculate_aggregation_rates(i,kf0_42,kf1_42,Asymp_42,Hill_42)
        # @show i,Final_40, Final_42,KF40/(i^Hill_40+KF40),KF42/(i^Hill_42+KF42)
        Final_40_Hill[i] = calculate_aggregation_rates_Hill(i,kf0_40,kf1_40,Asymp_40,Hill_40)
        Final_42_Hill[i] = calculate_aggregation_rates_Hill(i,kf0_42,kf1_42,Asymp_42,Hill_42)
        Final_40_new[i] = calculate_aggregation_rates_new(i,kf0_40,kf1_40,Asymp_40,Hill_40)
        Final_42_new[i] = calculate_aggregation_rates_new(i,kf0_42,kf1_42,Asymp_42,Hill_42)
        # @show i,Final_40_new, Final_42_new,KF40new/(i^Hill_40+KF40new),KF42new/(i^Hill_42+KF42new)
        Final_40_new_Hill[i] = calculate_aggregation_rates_new_Hill(i,kf0_40,kf1_40,Asymp_40,Hill_40)
        Final_42_new_Hill[i] = calculate_aggregation_rates_new_Hill(i,kf0_42,kf1_42,Asymp_42,Hill_42)
    end
    # plot(1:24,Final_40,label="Final_40",legend=:outertopright)
    plot(1:24,Final_42,label="Final_42")
    # plot!(1:24,Final_40_new,label="Final_40_new")
    plot!(1:24,Final_42_new,label="Final_42_new")
    plot!(1:24,Final_42_new_Hill,label="Final_42_new_Hill")
    plot!(1:24,Final_42_Hill,label="Final_42_Hill")
    # hline!([kf0_40],label="kf0")
    # hline!([kf1_40],label="kf1")
    hline!([kf0_42],label="kf0")
    hline!([kf1_42],label="kf1")

end
main()
