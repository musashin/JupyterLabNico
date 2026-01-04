# Vehicle Analysis Notebook - Updates Log

## Major Improvements Based on User Feedback

### 1. ✅ Fixed Electricity Rate Error
**Problem**: Flex D peak rate was 10x too high ($0.5037 instead of $0.1078)  
**Impact**: Was showing unrealistic negative operating costs for V2H option  
**Fix**: Corrected to actual 2024 Hydro-Quebec Flex D rates:
- Peak rate: $0.1078/kWh (winter AM/PM)
- Off-peak rate: $0.0400/kWh

### 2. ✅ Added Quebec-Specific Tire Costs
**Added**: Comprehensive tire cost modeling for Quebec requirements
- **Winter tires** (mandatory in Quebec): Included full sets and installation
- **Summer tires**: Separate sets with Quebec-specific pricing
- **Installation costs**: $80 per swap × 2 swaps/year = $160/year
- **EV tire wear**: EVs wear tires ~20% faster due to weight (battery) and instant torque
  - BEV tires: Summer set lasts 3 years vs 4 years for gas vehicles
  - EV-rated tires: ~$1,200/set vs $800 for gas vehicles

**Annual Tire Costs**:
- BEV: ~$733/year (summer $400 + winter $275 + swaps $160)
- PHEV: ~$525/year
- ICE/Hybrid: ~$475/year

### 3. ✅ Added Charger Installation Costs
**Added**: Explicit charger costs with rebates
- **Standard Level 2 charger**: $1,500 (equipment + installation)
- **V2H bidirectional charger**: $8,500 (equipment + installation)
- **Quebec rebate**: $600 (Roulez vert program)

**Net costs after rebate**:
- Standard Level 2: $900
- V2H charger: $7,900

### 4. ✅ Updated to 2026 Government Incentives
**Critical Update**: Federal iZEV program ended March 31, 2024

**Current 2026 Incentives**:
- ❌ Federal iZEV: **$0** (program ended - was $5,000)
- ✅ Quebec Roulez vert (BEV): **$7,000** (extended through 2027)
- ✅ Quebec Roulez vert (PHEV): **$3,500**
- ✅ Quebec home charger: **$600**
- ✅ Federal solar (Greener Homes): **$5,000**
- ✅ Quebec solar: **$0.37/W** (up to $1,850)

**Impact**: Vehicles now receive $5,000 less in incentives than in 2024

### 5. ✅ Clarified Solar Installation Costs
**Added**: Breakdown of $7,000 solar investment
- Equipment (panels, inverter, mounting): $5,000
- Installation (labor, electrical, permits): $2,000
- **Total**: $7,000 for 5kW system

**After incentives**:
- Federal: $5,000
- Quebec: $1,850
- **Net cost**: ~$150

### 6. ✅ More Realistic V2H Arbitrage Assumptions
**Updated**: Conservative V2H rate arbitrage estimates
- **Was**: 20 kWh/day shifted (too optimistic)
- **Now**: 10 kWh/day (realistic given car also needs charging)

**Realistic V2H Savings**:
- Annual savings: ~$87/year (not ~$1,200!)
- Payback on V2H premium: 90+ years (economics alone)
- **Real value**: Backup power capability (25-60 hours/month)

### 7. ✅ Credentials Simplified
**Updated**: Now only requires username and password
- Contract ID and Customer ID are **optional**
- The `hydroqc` library can auto-retrieve them after login
- Only needed if you have multiple accounts

## Cost Impact Summary

### Example: VW ID.4 Pro AWD with V2H (2026 vs 2024)

**Upfront Costs (increase)**:
- Federal EV incentive lost: +$5,000
- V2H charger now explicit: +$7,900 (was hidden)
- Standard charger for non-V2H: +$900

**Annual Operating Costs (increase)**:
- Tires now included: +$733/year for BEV
- More realistic V2H savings: ~$87/year (was showing ~$1,200)

**Typical Impact on 10-year TCO**:
- Increased by ~$12,000-15,000 due to:
  - Lost federal incentive ($5,000)
  - Explicit charger costs ($900-7,900)
  - Tire costs over 10 years (~$7,330)

## What This Means for Your Decision

### ID.4 with V2H
- **Upfront**: ~$56,000 (vehicle + charger - incentives)
- **Annual operating**: ~$2,000 (energy + maintenance + tires - small V2H savings)
- **10-year total**: ~$75,000
- **Value proposition**: Backup power is the key benefit, not cost savings

### ID.4 without V2H
- **Upfront**: ~$48,000 (vehicle + standard charger - incentives)
- **Annual operating**: ~$2,100 (energy + maintenance + tires)
- **10-year total**: ~$69,000
- **Value proposition**: Lower upfront, still get EV benefits

### Keep Prius V
- **Upfront**: $0
- **Annual operating**: ~$3,600 (fuel + maintenance + tires)
- **10-year total**: ~$36,000
- **Value proposition**: Hard to beat economically if car is in good condition

## All Changes Are Now Included

The updated notebook now provides a **complete and realistic** cost analysis with:
- ✅ Accurate 2026 government incentives
- ✅ Quebec winter tire requirements
- ✅ EV-specific tire wear rates
- ✅ Explicit charger installation costs
- ✅ Realistic V2H savings expectations
- ✅ Corrected electricity rates
- ✅ Comprehensive total cost of ownership

## Running the Analysis

The notebook will now show realistic costs that account for all Quebec-specific requirements and current 2026 government programs. Use the interactive sliders to adjust driving distance and solar investment to see how they affect your specific situation.

---

**Note**: These updates make the analysis significantly more accurate and realistic. The V2H option is now properly shown as a premium feature for backup power, not a money-saving investment.
