"""
Rate Constant Extrapolation Module for Amyloid Beta Aggregation

This module calculates forward and backward rate constants for amyloid beta (Aβ) oligomerization
and fibrillization processes. It uses known experimental values for small oligomers (dimers and trimers)
to extrapolate rates for larger species using Hill function-based relationships.

Key Features:
- Extrapolates forward (association) and backward (dissociation) rates for oligomers up to size 24
- Handles both Aβ40 and Aβ42 species separately
- Uses experimentally determined rates for small oligomers as anchor points
- Implements Hill function-based extrapolation with asymptotic behavior
- Converts rates from literature units (M⁻¹s⁻¹, s⁻¹) to model units (nM⁻¹h⁻¹, h⁻¹)
- Calculates gain factors (forward/backward ratios) to assess aggregation propensity
- Calculates size-dependent plaque formation rates (multiplied by oligomer/fibril length)

The extrapolated rates are used by the oligomer and fibril modules to model the complete
aggregation cascade from monomers through oligomers to fibrils and plaques.

References:
- Original rate constants from literature for AB40 and AB42 dimer/trimer formation
- Hill function parameters tuned to match experimental observations of aggregation behavior
"""

# Calculation of forward and backward Rates 
# Note no plaque rates 
# Note no 24 to 12 breakdown

using GLMakie
using DataFrames
using Printf

# Define the equations for forward (KF) and backward (KB) rate extrapolation
function extrapolate_kf(kf0, kf1, j, Asymp, HillA)
    """
    Extrapolate forward rate constants for higher order oligomers
    kf0: Rate constant for O1->O2 (known)
    kf1: Rate constant for O2->O3 (known)
    j: Oligomer size
    Asymp: Asymptotic value
    HillA: Hill coefficient for forward rates
    """
    KF = (kf1 - Asymp * kf1) / (kf0 - kf1)
    kj_f = (kf0 - Asymp * kf1) * (KF / (j^HillA + KF)) + Asymp * kf1
    return kj_f
end

function extrapolate_kb(kb0, kb1, j, Asymp, HillB, rate_cutoff=nothing)
    """
    Extrapolate backward rate constants for higher order oligomers
    kb0: Rate constant for O2->O1 (known)
    kb1: Rate constant for O3->O2 (known)
    j: Oligomer size
    Asymp: Asymptotic value
    HillB: Hill coefficient for backward rates
    rate_cutoff: Minimum allowed rate, if nothing no cutoff is applied
    """
    KB = (kb1 - Asymp * kb1) / (kb0 - kb1)
    kj_b = (kb0 - Asymp * kb1) * (KB / (j^HillB + KB)) + Asymp * kb1
    
    # Apply rate cutoff if specified
    if rate_cutoff !== nothing && kj_b < rate_cutoff
        kj_b = rate_cutoff
    end
        
    return kj_b
end

function calculate_plaque_rates(baseline_ab40_rate, baseline_ab42_rate, forward_rates_forty, forward_rates_fortytwo, enable_forward_rate_multiplier=true)
    """
    Calculate plaque formation rates for oligomers and fibrils.
    If enable_forward_rate_multiplier is true, rates are multiplied by the forward rate for that aggregate.
    
    Args:
        baseline_ab40_rate: Baseline plaque formation rate for AB40
        baseline_ab42_rate: Baseline plaque formation rate for AB42
        forward_rates_forty: Dictionary of forward rates for AB40 aggregates
        forward_rates_fortytwo: Dictionary of forward rates for AB42 aggregates
        enable_forward_rate_multiplier: If true, multiply rates by forward rate for that aggregate
    
    Returns:
        Dictionary containing plaque formation rates
    """
    plaque_rates = Dict{String, Float64}()
    
    # Generate oligomer sizes from 13 to 16 (oligomers that can form plaques)
    oligomer_sizes = collect(13:16)
    
    # Generate fibril sizes from 17 to 20 (fibrils that can form plaques)
    fibril_sizes = collect(17:20)
    
    # Calculate plaque rates for oligomers
    for size in oligomer_sizes
        if enable_forward_rate_multiplier
            # Get the forward rate for this oligomer size
            forward_rate_key_40 = "k_O$(size-1)_O$(size)_forty"
            forward_rate_key_42 = "k_O$(size-1)_O$(size)_fortytwo"
            
            if haskey(forward_rates_forty, forward_rate_key_40) && haskey(forward_rates_fortytwo, forward_rate_key_42)
                # Multiply baseline by forward rate
                plaque_rates["k_O$(size)_Plaque_forty"] = baseline_ab40_rate * forward_rates_forty[forward_rate_key_40]
                plaque_rates["k_O$(size)_Plaque_fortytwo"] = baseline_ab42_rate * forward_rates_fortytwo[forward_rate_key_42]
            else
                # Fallback to baseline rates if forward rates not found
                println("Warning: Forward rates not found for oligomer size $size, using baseline rates")
                plaque_rates["k_O$(size)_Plaque_forty"] = baseline_ab40_rate
                plaque_rates["k_O$(size)_Plaque_fortytwo"] = baseline_ab42_rate
            end
        else
            # Use baseline rates
            plaque_rates["k_O$(size)_Plaque_forty"] = baseline_ab40_rate
            plaque_rates["k_O$(size)_Plaque_fortytwo"] = baseline_ab42_rate
        end
    end
    
    # Calculate plaque rates for fibrils
    for size in fibril_sizes
        if enable_forward_rate_multiplier
            # Get the forward rate for this fibril size
            if size == 17
                # Special case: transition from oligomer to fibril
                forward_rate_key_40 = "k_O$(size-1)_F$(size)_forty"
                forward_rate_key_42 = "k_O$(size-1)_F$(size)_fortytwo"
            else
                # Normal fibril growth
                forward_rate_key_40 = "k_F$(size-1)_F$(size)_forty"
                forward_rate_key_42 = "k_F$(size-1)_F$(size)_fortytwo"
            end
            
            if haskey(forward_rates_forty, forward_rate_key_40) && haskey(forward_rates_fortytwo, forward_rate_key_42)
                # Multiply baseline by forward rate
                plaque_rates["k_F$(size)_Plaque_forty"] = size * baseline_ab40_rate * forward_rates_forty[forward_rate_key_40]
                plaque_rates["k_F$(size)_Plaque_fortytwo"] = size * baseline_ab42_rate * forward_rates_fortytwo[forward_rate_key_42]
            else
                # Fallback to baseline rates if forward rates not found
                println("Warning: Forward rates not found for fibril size $size, using baseline rates")
                plaque_rates["k_F$(size)_Plaque_forty"] = baseline_ab40_rate
                plaque_rates["k_F$(size)_Plaque_fortytwo"] = baseline_ab42_rate
            end
        else
            # Use baseline rates
            plaque_rates["k_F$(size)_Plaque_forty"] = baseline_ab40_rate
            plaque_rates["k_F$(size)_Plaque_fortytwo"] = baseline_ab42_rate
        end
    end
    
    return plaque_rates
end

function convert_forward_rate(rate_M_s)
    """Convert from M⁻¹s⁻¹ to nM⁻¹h⁻¹"""
    # 1 M⁻¹s⁻¹ = 3.6 × 10⁻⁶ nM⁻¹h⁻¹
    return rate_M_s * 3.6e-6
end

function convert_backward_rate(rate_s)
    """Convert from s⁻¹ to h⁻¹"""
    # 1 s⁻¹ = 3600 h⁻¹
    return rate_s * 3600
end

function calculate_k_rates(;
    # Original rates from literature (M⁻¹s⁻¹ for forward, s⁻¹ for backward)
    garai_original_kf0_forty=0.5e2,  # AB40 monomer to dimer
    garai_original_kf0_fortytwo=9.9e2,  # AB42 monomer to dimer
    garai_original_kf1_forty=20.0,  # AB40 dimer to trimer
    garai_original_kf1_fortytwo=38.0,  # AB42 dimer to trimer
    garai_original_kb0_forty=2.7e-3,  # AB40 dimer to monomer
    garai_original_kb0_fortytwo=12.7e-3,  # AB42 dimer to monomer
    garai_original_kb1_forty=0.3e-3,  # AB40 trimer to dimer
    garai_original_kb1_fortytwo=0.0,  # AB42 trimer to dimer
    
    # Hill coefficients and asymptotic values
    # Geerts 2024 forAsymp40 = 0.24375
    forAsymp40=0.3,  # DIMENSIONLESS	Fitted to nat history abeta accumulation	Asymptotic value for extrapolation of forward rate constants for Ab40 aggregation
    # Geerts 2024 forAsymp42 = 2
    forAsymp42=2.0,  # DIMENSIONLESS	Fitted to nat history abeta accumulation	Asymptotic value for extrapolation of forward rate constants for Ab42 aggregation
    backAsymp40=0.3,  # ?
    backAsymp42=2.0,  # ?
    # Geerts 2024 forGain40 = 7.775 Gain factor for Ab40 aggregation
    forGain40 = 10, # DIMENSIONLESS	Fitted to nat history abeta accumulation	Gain value for extrapolation of forward rate constants for Ab40 aggregation
    # Geerts 2024 forGain42 = 7
    forGain42 = 7, # DIMENSIONLESS	Fitted to nat history abeta accumulation	Gain value for extrapolation of forward rate constants for Ab42 aggregation
    # Geerts 2024 forHill40 = 2.3125
    forHill40=2.0,    # DIMENSIONLESS	Fitted to nat history abeta accumulation	Hill coefficient for extrapolation of forward rate constants for Ab40 aggregation
    # Geerts 2024 forHill42 = 3
    forHill42=3.0,    # DIMENSIONLESS	Fitted to nat history abeta accumulation	hill coefficient for extrapolation of forward rate constants for Ab42 aggregation
    # Geerts 2024 BackHill40 = 2.3125
    BackHill40=2.5,   # DIMENSIONLESS	Fitted to nat history abeta accumulation	Hill coeficient for extrapolation of backwards rate constants for Ab40 aggregation
    # Geerts 2024 BackHill42 = 3
    BackHill42=3.0,   # DIMENSIONLESS	Fitted to nat history abeta accumulation	Hill coeficient for extrapolation of backwards rate constants for Ab42 aggregation
    
    # Rate cutoff
    rate_cutoff=1e-8,# DIMENSIONLESS	Assumed	Used for Minimal backward rate constant in extrapolation
    
    # Baseline rate constants
    # Baseline_AB40_down_cut_off is the minimum value for the backward rate constant
    Baseline_AB40_down_cut_off =	1.00E-05, #	1 / h	Assumed from Garai K 2013 PNAS v110 n0 p3321-3326.	Cut off minimum value for the baseline rate constant for removal of a monomer to AB40 oligomer 3 or higher.  
    Baseline_AB40_Oligomer_Fibril_Plaque =	5.00E-06, #	L / (nano * mol * h)	Assumed	Rate constant for formation of plaques from fibrils and oligomers for AB40. 
    Baseline_AB40_Oligomer_Fibril_splitting =	2, #	DIMENSIONLESS	Assumed	Baseline rate constant for splitting of fibrils and oligomers for AB40.  
    # Baseline_AB40_up_cut_off is the minimum value for the forward rate constant
    Baseline_AB40_up_cut_off =	0, #	L / (nano * mol * h)	Assumed from Garai K 2013 PNAS v110 n0 p3321-3326.	Cut off minimum value for the baseline rate constant for addition of a monomer to AB40 oligomer 3 or higher.  Lower limit set by asymptotic behavior of function, so limit here set to 0.  Based on in vitro data from 
    # Baseline_AB42_down_cut_off is the minimum value for the backward rate constant
    Baseline_AB42_down_cut_off =	1.00E-05, #	1 / h	Assumed from Garai K 2013 PNAS v110 n0 p3321-3326.	Cut off minimum value for the baseline rate constant for removal of a monomer to AB40 oligomer 3 or higher.  
    Baseline_AB42_Oligomer_Fibril_Plaque =	5.00E-05, #	L / (nano * mol * h)	Assumed	Baseline rate constant for formation of plaques from fibrils and oligomers for AB42.  
    Baseline_AB42_Oligomer_Fibril_splitting =	1, #	DIMENSIONLESS	Assumed	Baseline rate constant for splitting of fibrils and oligomers for AB42.  
    # Baseline_AB42_up_cut_off is the minimum value for the forward rate constant
    Baseline_AB42_up_cut_off =	0, #	L / (nano * mol * h)	Assumed from Garai K 2013 PNAS v110 n0 p3321-3326.	Cut off minimum value for the baseline rate constant for addition of a monomer to AB42 oligomer 3 or higher.  Lower limit set by asymptotic behavior of function, so limit here set to 0.
    
    # Plaque formation parameters
    enable_plaque_forward_rate_multiplier=true   # If true, multiply plaque rates by forward rate for that aggregate
)
    """
    Calculate forward and backward rates for both AB40 and AB42 oligomers
    using provided parameters based on known values from literature
    
    Parameters:
    -----------
    garai_original_kf0_forty: float
        AB40 monomer to dimer forward rate (M⁻¹s⁻¹)
    garai_original_kf0_fortytwo: float
        AB42 monomer to dimer forward rate (M⁻¹s⁻¹)
    garai_original_kf1_forty: float
        AB40 dimer to trimer forward rate (M⁻¹s⁻¹)
    garai_original_kf1_fortytwo: float
        AB42 dimer to trimer forward rate (M⁻¹s⁻¹)
    garai_original_kb0_forty: float
        AB40 dimer to monomer backward rate (s⁻¹)
    garai_original_kb0_fortytwo: float
        AB42 dimer to monomer backward rate (s⁻¹)
    garai_original_kb1_forty: float
        AB40 trimer to dimer backward rate (s⁻¹)
    garai_original_kb1_fortytwo: float
        AB42 trimer to dimer backward rate (s⁻¹)
    forAsymp40: float
        Asymptotic value for AB40 forward rates
    forAsymp42: float
        Asymptotic value for AB42 forward rates
    backAsymp40: float
        Asymptotic value for AB40 backward rates
    backAsymp42: float
        Asymptotic value for AB42 backward rates
    forHill40: float
        Hill coefficient for AB40 forward rates
    forHill42: float
        Hill coefficient for AB42 forward rates
    BackHill40: float
        Hill coefficient for AB40 backward rates
    BackHill42: float
        Hill coefficient for AB42 backward rates
    rate_cutoff: float
        Minimum allowed rate for backward reactions
    Baseline_AB40_Oligomer_Fibril_Plaque: float
        Baseline plaque formation rate for AB40
    Baseline_AB42_Oligomer_Fibril_Plaque: float
        Baseline plaque formation rate for AB42
    enable_plaque_forward_rate_multiplier: bool
        If true, multiply plaque rates by forward rate for that aggregate
    
    Returns:
    --------
    dict
        Dictionary containing all extrapolated rate constants including plaque rates
    """
    garai_original_kb1_forty = Baseline_AB40_down_cut_off/3600
    garai_original_kb1_fortytwo = Baseline_AB42_down_cut_off/3600
    # Convert rates to appropriate units
    kf0_forty = convert_forward_rate(garai_original_kf0_forty)  
    kb0_forty = convert_backward_rate(garai_original_kb0_forty)
    kf0_fortytwo = convert_forward_rate(garai_original_kf0_fortytwo)
    kb0_fortytwo = convert_backward_rate(garai_original_kb0_fortytwo)
    kf1_forty = convert_forward_rate(garai_original_kf1_forty)
    kb1_forty = convert_backward_rate(garai_original_kb1_forty)
    kf1_fortytwo = convert_forward_rate(garai_original_kf1_fortytwo)
    kb1_fortytwo = convert_backward_rate(garai_original_kb1_fortytwo)
    
    # Create and print conversion table
    #println("\nRate Constant Unit Conversion:")
    table_data = [
        ("k+12 (Aβ40)", @sprintf("%.1f M⁻¹s⁻¹", garai_original_kf0_forty), @sprintf("%.6f nM⁻¹h⁻¹", kf0_forty)),
        ("k-12 (Aβ40)", @sprintf("%.3f s⁻¹", garai_original_kb0_forty), @sprintf("%.6f h⁻¹", kb0_forty)),
        ("k+23 (Aβ40)", @sprintf("%.1f M⁻¹s⁻¹", garai_original_kf1_forty), @sprintf("%.6f nM⁻¹h⁻¹", kf1_forty)),
        ("k-23 (Aβ40)", @sprintf("%.3f s⁻¹", garai_original_kb1_forty), @sprintf("%.6f h⁻¹", kb1_forty)),
        ("k+12 (Aβ42)", @sprintf("%.1f M⁻¹s⁻¹", garai_original_kf0_fortytwo), @sprintf("%.6f nM⁻¹h⁻¹", kf0_fortytwo)),
        ("k-12 (Aβ42)", @sprintf("%.3f s⁻¹", garai_original_kb0_fortytwo), @sprintf("%.6f h⁻¹", kb0_fortytwo)),
        ("k+23 (Aβ42)", @sprintf("%.1f M⁻¹s⁻¹", garai_original_kf1_fortytwo), @sprintf("%.6f nM⁻¹h⁻¹", kf1_fortytwo)),
        ("k-23 (Aβ42)", @sprintf("%.3f s⁻¹", garai_original_kb1_fortytwo), @sprintf("%.6f h⁻¹", kb1_fortytwo))
    ]
    headers = ["Rate Constant", "Original Value", "Converted Value"]
    #println(tabulate(table_data, headers, tablefmt="grid"))
    
    # Generate oligomer sizes from 4 to 24
    oligomer_sizes = collect(4:24)

    # Calculate rates for each oligomer size
    kf_forty = [extrapolate_kf(kf0_forty, kf1_forty, size, forAsymp40, forHill40) for size in oligomer_sizes]
    kb_forty = [extrapolate_kb(kb0_forty, kb1_forty, size, backAsymp40, BackHill40, Baseline_AB40_down_cut_off) for size in oligomer_sizes]
    kf_fortytwo = [extrapolate_kf(kf0_fortytwo, kf1_fortytwo, size, forAsymp42, forHill42) for size in oligomer_sizes]
    kb_fortytwo = [extrapolate_kb(kb0_fortytwo, kb1_fortytwo, size, backAsymp42, BackHill42, Baseline_AB42_down_cut_off) for size in oligomer_sizes]
    
    # Create dictionary to store the rates with proper naming convention
    rates = Dict{String, Float64}()
    
    # Store rates with appropriate prefixes (O for oligomers, F for fibrils)
    for (i, size) in enumerate(oligomer_sizes)
        if size < 17
            # Oligomer rates (size < 17)
            rates["k_O$(size-1)_O$(size)_forty"] = kf_forty[i]
            rates["k_O$(size)_O$(size-1)_forty"] = kb_forty[i]
            rates["k_O$(size-1)_O$(size)_fortytwo"] = kf_fortytwo[i]
            rates["k_O$(size)_O$(size-1)_fortytwo"] = kb_fortytwo[i]
        elseif size == 17
            # Special case: transition between oligomer and fibril
            rates["k_O$(size-1)_F$(size)_forty"] = kf_forty[i]
            rates["k_F$(size)_O$(size-1)_forty"] = kb_forty[i]
            rates["k_O$(size-1)_F$(size)_fortytwo"] = kf_fortytwo[i]
            rates["k_F$(size)_O$(size-1)_fortytwo"] = kb_fortytwo[i]
        else
            # Fibril rates (size >= 17)
            rates["k_F$(size-1)_F$(size)_forty"] = kf_forty[i]
            rates["k_F$(size)_F$(size-1)_forty"] = kb_forty[i]
            rates["k_F$(size-1)_F$(size)_fortytwo"] = kf_fortytwo[i]
            rates["k_F$(size)_F$(size-1)_fortytwo"] = kb_fortytwo[i]
        end
    end
    
    # Create separate dictionaries for forward rates only (needed for plaque calculation)
    forward_rates_forty = Dict{String, Float64}()
    forward_rates_fortytwo = Dict{String, Float64}()
    
    for (i, size) in enumerate(oligomer_sizes)
        if size < 17
            # Oligomer forward rates
            forward_rates_forty["k_O$(size-1)_O$(size)_forty"] = kf_forty[i]
            forward_rates_fortytwo["k_O$(size-1)_O$(size)_fortytwo"] = kf_fortytwo[i]
        elseif size == 17
            # Transition forward rates
            forward_rates_forty["k_O$(size-1)_F$(size)_forty"] = kf_forty[i]
            forward_rates_fortytwo["k_O$(size-1)_F$(size)_fortytwo"] = kf_fortytwo[i]
        else
            # Fibril forward rates
            forward_rates_forty["k_F$(size-1)_F$(size)_forty"] = kf_forty[i]
            forward_rates_fortytwo["k_F$(size-1)_F$(size)_fortytwo"] = kf_fortytwo[i]
        end
    end
    
    # Calculate and add plaque formation rates
    plaque_rates = calculate_plaque_rates(
        Baseline_AB40_Oligomer_Fibril_Plaque, 
        Baseline_AB42_Oligomer_Fibril_Plaque, 
        forward_rates_forty,
        forward_rates_fortytwo,
        enable_plaque_forward_rate_multiplier
    )
    merge!(rates, plaque_rates)
    
    # Print plaque rate information if forward rate multiplier is enabled
    if enable_plaque_forward_rate_multiplier
        #println("\nPlaque formation rates with forward rate multiplier enabled:")
        #println("Baseline AB40 rate: $(@sprintf("%.6f", Baseline_AB40_Oligomer_Fibril_Plaque)) L/(nM·h)")
        #println("Baseline AB42 rate: $(@sprintf("%.6f", Baseline_AB42_Oligomer_Fibril_Plaque)) L/(nM·h)")
        #println("\nExample plaque rates (rate = baseline × forward_rate):")
        example_sizes = [13, 16, 17, 20]
        for size in example_sizes
            if size < 17
                key_40 = "k_O$(size)_Plaque_forty"
                key_42 = "k_O$(size)_Plaque_fortytwo"
                forward_key_40 = "k_O$(size-1)_O$(size)_forty"
                forward_key_42 = "k_O$(size-1)_O$(size)_fortytwo"
            else
                key_40 = "k_F$(size)_Plaque_forty"
                key_42 = "k_F$(size)_Plaque_fortytwo"
                forward_key_40 = "k_F$(size-1)_F$(size)_forty"
                forward_key_42 = "k_F$(size-1)_F$(size)_fortytwo"
            end
            
            if haskey(plaque_rates, key_40) && haskey(plaque_rates, key_42)
                forward_rate_40 = get(forward_rates_forty, forward_key_40, 0.0)
                forward_rate_42 = get(forward_rates_fortytwo, forward_key_42, 0.0)
                #println("  Size $size: AB40 = $(@sprintf("%.6f", plaque_rates[key_40])) (forward_rate = $(@sprintf("%.6f", forward_rate_40))), AB42 = $(@sprintf("%.6f", plaque_rates[key_42])) (forward_rate = $(@sprintf("%.6f", forward_rate_42)))")
            end
        end
    #else
        #println("\nPlaque formation rates using baseline values (no forward rate multiplier):")
        #println("AB40 rate: $(@sprintf("%.6f", Baseline_AB40_Oligomer_Fibril_Plaque)) L/(nM·h)")
        #println("AB42 rate: $(@sprintf("%.6f", Baseline_AB42_Oligomer_Fibril_Plaque)) L/(nM·h)")
    end
    
    return rates
end

function calculate_gain_factors(rates)
    """
    Calculate the gain factor (ratio of forward to backward rates) for each oligomer size
    
    Parameters:
    rates: Dictionary of rate constants
    
    Returns:
    Dictionary of gain factors for AB40 and AB42
    """
    gain_factors = Dict{String, Float64}()
    
    # Calculate gain factors for sizes 4 to 24
    for size in 4:24
        if size < 17
            # Oligomer gain factors
            gain_factors["gain_O$(size)_forty"] = rates["k_O$(size-1)_O$(size)_forty"] / rates["k_O$(size)_O$(size-1)_forty"]
            gain_factors["gain_O$(size)_fortytwo"] = rates["k_O$(size-1)_O$(size)_fortytwo"] / rates["k_O$(size)_O$(size-1)_fortytwo"]
        elseif size == 17
            # Transition gain factors
            gain_factors["gain_F$(size)_forty"] = rates["k_O$(size-1)_F$(size)_forty"] / rates["k_F$(size)_O$(size-1)_forty"]
            gain_factors["gain_F$(size)_fortytwo"] = rates["k_O$(size-1)_F$(size)_fortytwo"] / rates["k_F$(size)_O$(size-1)_fortytwo"]
        else
            # Fibril gain factors
            gain_factors["gain_F$(size)_forty"] = rates["k_F$(size-1)_F$(size)_forty"] / rates["k_F$(size)_F$(size-1)_forty"]
            gain_factors["gain_F$(size)_fortytwo"] = rates["k_F$(size-1)_F$(size)_fortytwo"] / rates["k_F$(size)_F$(size-1)_fortytwo"]
        end
    end
    
    return gain_factors
end

function main()
    # Example usage with default parameters
    rates = calculate_k_rates()

    # Calculate gain factors
    gain_factors = calculate_gain_factors(rates)

    # Print the calculated rates
    #println("\nCalculated rate constants:")
    #for size in 4:24
        #println("\nFor size $size:")
        #if size < 17
            # Oligomer rates
            #println("AB40 forward (O$(size-1)->O$size): $(@sprintf("%.3e", rates["k_O$(size-1)_O$(size)_forty"])) nM⁻¹h⁻¹")
            #println("AB40 backward (O$size->O$(size-1)): $(@sprintf("%.3e", rates["k_O$(size)_O$(size-1)_forty"])) h⁻¹")
            #println("AB40 gain factor: $(@sprintf("%.3e", gain_factors["gain_O$(size)_forty"]))")
            #println("AB42 forward (O$(size-1)->O$size): $(@sprintf("%.3e", rates["k_O$(size-1)_O$(size)_fortytwo"])) nM⁻¹h⁻¹")
            #println("AB42 backward (O$size->O$(size-1)): $(@sprintf("%.3e", rates["k_O$(size)_O$(size-1)_fortytwo"])) h⁻¹")
            #println("AB42 gain factor: $(@sprintf("%.3e", gain_factors["gain_O$(size)_fortytwo"]))")
        #elseif size == 17
            # Transition between oligomer and fibril
            #println("AB40 forward (O$(size-1)->F$size): $(@sprintf("%.3e", rates["k_O$(size-1)_F$(size)_forty"])) nM⁻¹h⁻¹")
            #println("AB40 backward (F$size->O$(size-1)): $(@sprintf("%.3e", rates["k_F$(size)_O$(size-1)_forty"])) h⁻¹")
            #println("AB40 gain factor: $(@sprintf("%.3e", gain_factors["gain_F$(size)_forty"]))")
            #println("AB42 forward (O$(size-1)->F$size): $(@sprintf("%.3e", rates["k_O$(size-1)_F$(size)_fortytwo"])) nM⁻¹h⁻¹")
            #println("AB42 backward (F$size->O$(size-1)): $(@sprintf("%.3e", rates["k_F$(size)_O$(size-1)_fortytwo"])) h⁻¹")
            #println("AB42 gain factor: $(@sprintf("%.3e", gain_factors["gain_F$(size)_fortytwo"]))")
        #else
            # Fibril rates
            #println("AB40 forward (F$(size-1)->F$size): $(@sprintf("%.3e", rates["k_F$(size-1)_F$(size)_forty"])) nM⁻¹h⁻¹")
            #println("AB40 backward (F$size->F$(size-1)): $(@sprintf("%.3e", rates["k_F$(size)_F$(size-1)_forty"])) h⁻¹")
            #println("AB40 gain factor: $(@sprintf("%.3e", gain_factors["gain_F$(size)_forty"]))")
            #println("AB42 forward (F$(size-1)->F$size): $(@sprintf("%.3e", rates["k_F$(size-1)_F$(size)_fortytwo"])) nM⁻¹h⁻¹")
            #println("AB42 backward (F$size->F$(size-1)): $(@sprintf("%.3e", rates["k_F$(size)_F$(size-1)_fortytwo"])) h⁻¹")
            #println("AB42 gain factor: $(@sprintf("%.3e", gain_factors["gain_F$(size)_fortytwo"]))")
        #end
    #end

    # Optional: Plot the rates to visualize the extrapolation
    sizes = collect(4:24)

    # Create figure with two subplots
    fig = Figure(resolution=(800, 600))
    
    # AB40 subplot
    ax1 = Axis(fig[1, 1], 
        xlabel="Size", 
        ylabel="Rate (nM⁻¹h⁻¹ or h⁻¹)", 
        title="AB40 Rate Constants",
        yscale=log10
    )
    
    # AB42 subplot
    ax2 = Axis(fig[2, 1], 
        xlabel="Size", 
        ylabel="Rate (nM⁻¹h⁻¹ or h⁻¹)", 
        title="AB42 Rate Constants",
        yscale=log10
    )
    
    # Prepare data for plotting
    oligomer_sizes = [s for s in sizes if s < 17]
    fibril_sizes = [s for s in sizes if s > 17]
    
    # AB40 Oligomer forward rates
    oligomer_forward_40 = [rates["k_O$(size-1)_O$(size)_forty"] for size in oligomer_sizes]
    lines!(ax1, oligomer_sizes, oligomer_forward_40, 
        color=:blue, linewidth=2.5, alpha=0.3, label="Forward (Oligomers)")
    
    # AB40 Oligomer backward rates
    oligomer_backward_40 = [rates["k_O$(size)_O$(size-1)_forty"] for size in oligomer_sizes]
    lines!(ax1, oligomer_sizes, oligomer_backward_40, 
        color=:blue, linewidth=2.5, linestyle=:dash, label="Backward (Oligomers)")
    
    # AB40 Transition rates
    Makie.scatter!(ax1, [17], [rates["k_O16_F17_forty"]], 
        color=:green, markersize=6, label="Forward (Transition)")
    Makie.scatter!(ax1, [17], [rates["k_F17_O16_forty"]], 
        color=:green, markersize=6, marker=:circle, label="Backward (Transition)")
    
    # AB40 Fibril forward rates
    fibril_forward_40 = [rates["k_F$(size-1)_F$(size)_forty"] for size in fibril_sizes]
    lines!(ax1, fibril_sizes, fibril_forward_40, 
        color=:red, linewidth=2.5, label="Forward (Fibrils)")
    
    # AB40 Fibril backward rates
    fibril_backward_40 = [rates["k_F$(size)_F$(size-1)_forty"] for size in fibril_sizes]
    lines!(ax1, fibril_sizes, fibril_backward_40, 
        color=:red, linewidth=2.5, linestyle=:dash, label="Backward (Fibrils)")
    
    # AB40 Transition line
    vlines!(ax1, [17], color=:black, linestyle=:dot, linewidth=1.5, label="Transition")
    
    # AB42 Oligomer forward rates
    oligomer_forward_42 = [rates["k_O$(size-1)_O$(size)_fortytwo"] for size in oligomer_sizes]
    lines!(ax2, oligomer_sizes, oligomer_forward_42, 
        color=:blue, linewidth=2.5, alpha=0.3, label="Forward (Oligomers)")
    
    # AB42 Oligomer backward rates
    oligomer_backward_42 = [rates["k_O$(size)_O$(size-1)_fortytwo"] for size in oligomer_sizes]
    lines!(ax2, oligomer_sizes, oligomer_backward_42, 
        color=:blue, linewidth=2.5, linestyle=:dash, label="Backward (Oligomers)")
    println(string(oligomer_forward_40[1]," ", oligomer_backward_40[1], " ", oligomer_forward_42[1], " ", oligomer_backward_42[1]))
    # AB42 Transition rates
    Makie.scatter!(ax2, [17], [rates["k_O16_F17_fortytwo"]], 
        color=:green, markersize=6, label="Forward (Transition)")
    Makie.scatter!(ax2, [17], [rates["k_F17_O16_fortytwo"]], 
        color=:green, markersize=6, marker=:circle, label="Backward (Transition)")
    
    # AB42 Fibril forward rates
    fibril_forward_42 = [rates["k_F$(size-1)_F$(size)_fortytwo"] for size in fibril_sizes]
    lines!(ax2, fibril_sizes, fibril_forward_42, 
        color=:red, linewidth=2.5, label="Forward (Fibrils)")
    
    # AB42 Fibril backward rates
    fibril_backward_42 = [rates["k_F$(size)_F$(size-1)_fortytwo"] for size in fibril_sizes]
    lines!(ax2, fibril_sizes, fibril_backward_42, 
        color=:red, linewidth=2.5, linestyle=:dash, label="Backward (Fibrils)")
    
    # AB42 Transition line
    vlines!(ax2, [17], color=:black, linestyle=:dot, linewidth=1.5, label="Transition")
    
    # Add legends
    Legend(fig[1, 2], ax1, "AB40")
    Legend(fig[2, 2], ax2, "AB42")
    
    # Save and display
    save("rate_extrapolation.png", fig)
    display(fig)
end

main()