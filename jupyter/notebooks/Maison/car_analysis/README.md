# Vehicle Purchase Decision Analysis
## VW ID.4 Pro AWD Comprehensive Comparison Tool

This Jupyter notebook provides a detailed analysis to help you decide whether to purchase a Volkswagen ID.4 Pro AWD, comparing it against plugin hybrid, gasoline, and keeping your current vehicle options.

## 🚗 What This Analyzes

### Vehicle Options Compared:
1. **VW ID.4 Pro AWD with V2H (Vehicle-to-Home)**
2. **VW ID.4 Pro AWD without V2H**
3. **Plugin Hybrid SUV** (similar size/capacity)
4. **Gasoline SUV** (similar size/capacity)
5. **Keep Current Vehicle** (Toyota Prius V 2017)

### Key Features:
- ✅ Real Hydro-Quebec consumption data integration
- ✅ Solar panel system ROI analysis ($7,000 investment)
- ✅ V2H backup power calculations (hours of backup per month)
- ✅ Rate arbitrage savings with V2H and Flex D rates
- ✅ Government incentives (Federal + Quebec)
- ✅ Monthly energy consumption and cost projections
- ✅ Interactive sliders for km/year and solar cost
- ✅ 10-year total cost of ownership
- ✅ Environmental impact comparison

## 📋 Prerequisites

### System Requirements:
- Python 3.8 or higher
- JupyterLab or Jupyter Notebook
- Internet connection (for API access)

### Required Python Packages:
```bash
pip install jupyter ipywidgets matplotlib pandas numpy requests python-dotenv
pip install hydroqc  # For Hydro-Quebec API
```

Or install all at once:
```bash
pip install -r requirements.txt
```

## 🔧 Setup Instructions

### 1. Install Dependencies
```bash
# Using pip
pip install jupyter ipywidgets matplotlib pandas numpy requests python-dotenv hydroqc

# Or create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install jupyter ipywidgets matplotlib pandas numpy requests python-dotenv hydroqc
```

### 2. Configure Hydro-Quebec Credentials

**IMPORTANT**: Your credentials will be stored locally and should NEVER be committed to version control.

1. Copy the template file:
   ```bash
   cp .env_template .env
   ```

2. Edit `.env` with your credentials (only username and password are required):
   ```bash
   # Required
   HYDRO_USERNAME=your_actual_username
   HYDRO_PASSWORD=your_actual_password
   
   # Optional - hydroqc can retrieve these automatically
   # Only uncomment if you have multiple accounts or auto-retrieval fails
   # HYDRO_CONTRACT_ID=your_contract_id
   # HYDRO_CUSTOMER_ID=your_customer_id
   ```

3. Verify the file is in `.gitignore`:
   ```bash
   cat .gitignore | grep "^\.env$"
   ```

**Note**: The `hydroqc` library typically only needs your username and password. After logging in, it can automatically retrieve your customer and contract IDs. You only need to specify these manually if you have multiple accounts or if automatic retrieval fails.

### 3. Enable Jupyter Widgets
```bash
jupyter nbextension enable --py widgetsnbextension
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

## 🚀 Running the Notebook

### Option 1: JupyterLab (Recommended)
```bash
jupyter lab
```
Then open `car_analysis.ipynb`

### Option 2: Jupyter Notebook
```bash
jupyter notebook car_analysis.ipynb
```

### Quick Start:
1. Open the notebook
2. Run all cells: **Cell → Run All**
3. Use the interactive sliders at the bottom to adjust:
   - Annual kilometers driven (default: 20,000 km)
   - Solar installation cost (default: $7,000)

## 📊 What You'll Get

### Visualizations:
1. **Total Cost of Ownership** - 10-year cumulative cost comparison
2. **Cost Breakdown** - Upfront vs operating costs
3. **Annual Operating Costs** - Year 1 expenses per option
4. **Payback Analysis** - Cost difference vs keeping current vehicle
5. **Monthly Energy Analysis** - Grid consumption and solar production
6. **V2H Backup Power** - Available backup hours per month
7. **Solar Production** - Monthly generation estimates for Montreal

### Data Tables:
- Detailed cost breakdown per scenario
- Monthly electricity consumption and costs
- V2H backup power duration by month
- Government incentives applied
- Environmental impact (CO₂ reduction)

### Key Metrics:
- Total 10-year cost of ownership
- Upfront cost (net of incentives)
- Annual operating costs
- Payback periods
- Rate arbitrage savings (V2H)
- Backup power capacity (hours/month)

## 🔍 Customization

### Adjust Your Parameters:

The notebook uses default values based on your location (4250 rue Belanger, Montreal):

**Current Settings:**
- Annual driving: 20,000 km
- Solar investment: $7,000 CAD
- Location: Montreal, QC
- Current vehicle: Toyota Prius V 2017 (6.5 L/100km)

**To Change:**
1. **In the notebook**: Use the interactive sliders
2. **In the code**: Edit the constants in Section 2

### Key Variables to Customize:
```python
# In Section 2 - Define Constants
annual_km = 20000  # Your annual driving
SOLAR_PARAMS['installation_cost'] = 7000  # Your solar budget
GASOLINE_PRICE = 1.65  # Current gas price in your area
```

## 📈 Understanding the Results

### Best Case Scenarios:

**VW ID.4 with V2H is best if:**
- You value backup power capability
- You drive significant kilometers annually
- You can install solar panels
- You're on or can switch to Hydro-Quebec Flex D rate

**VW ID.4 without V2H is best if:**
- You want EV benefits without V2H premium
- You have solar panels or plan to install them
- Backup power is not a priority

**Plugin Hybrid is best if:**
- You want electric for daily driving
- You need gas for long trips
- You're not ready for full EV

**Keep Prius V is best if:**
- Your current vehicle is in good condition
- Upfront cost is a major concern
- Your annual driving is relatively low

## ⚡ V2H (Vehicle-to-Home) Insights

### What V2H Provides:
- **Backup Power**: 25-60 hours depending on season
- **Rate Arbitrage**: Save by using battery during peak rates
- **Solar Storage**: Store excess solar for later use
- **Grid Independence**: Partial energy independence

### V2H Economics:
- Equipment cost: ~$8,500
- Annual savings: ~$300-500 (rate arbitrage)
- Payback: 15-20 years on savings alone
- **Value**: Backup power capability is the main benefit

## 🌞 Solar System Details

### System Specifications:
- Size: 5 kW (realistic for $7,000 budget)
- Annual production: ~5,750 kWh (Montreal)
- Installation cost: $7,000
- Net cost after incentives: ~$200
- Degradation: 0.5% per year

### Government Incentives:
- Federal (Canada Greener Homes): $5,000
- Quebec: $0.37/W (up to $1,850 for 5kW system)

## 💰 Government Incentives (2024/2025)

### Electric Vehicles:
- **Federal iZEV**: $5,000 (vehicles under $55,000)
- **Quebec Roulez vert (BEV)**: $7,000
- **Quebec Roulez vert (PHEV)**: $3,500
- **Home charger (Quebec)**: $600

### Solar:
- **Federal Greener Homes Grant**: $5,000
- **Quebec**: $0.37/W (5,000W = $1,850)

**Total potential incentives for ID.4 + Solar + Charger:**
- BEV: $12,000 (vehicle) + $6,850 (solar) = $18,850
- PHEV: $4,100 (vehicle) + $6,850 (solar) = $10,950

## 🌍 Environmental Impact

### Annual CO₂ Reduction (vs Gasoline SUV):
- **VW ID.4**: ~99% reduction (~4,370 kg CO₂/year)
- **Plugin Hybrid**: ~70% reduction (~3,059 kg CO₂/year)
- Based on Quebec's hydroelectric grid (~0.001 kg CO₂/kWh)

## 📝 Important Notes

### Assumptions:
- Electricity rates based on Hydro-Quebec Rate D (2024)
- Gasoline price: $1.65/L (Montreal average)
- Vehicle efficiency includes real-world winter impact
- Solar production based on Montreal climate data
- Maintenance costs from industry averages
- 10-year analysis period

### Limitations:
- Does not include vehicle depreciation/resale value
- Insurance costs not included (minimal difference)
- Assumes stable electricity rates (2% annual increase)
- V2H arbitrage assumes manual optimization

## 🔒 Security & Privacy

### Protecting Your Credentials:
- ✅ `.env` file is in `.gitignore`
- ✅ Never commit credentials to Git
- ✅ Store `.env` file securely
- ✅ Don't share notebook with credentials visible

### Before Sharing:
1. Remove or clear output cells with personal data
2. Verify no credentials in code cells
3. Use "Kernel → Restart & Clear Output" before sharing
4. Ensure `.env` file is not included when sharing

## 🐛 Troubleshooting

### "Module not found: hydroqc"
```bash
pip install hydroqc
```

### "No module named 'ipywidgets'"
```bash
pip install ipywidgets
jupyter nbextension enable --py widgetsnbextension
```

### Widgets not interactive in JupyterLab:
```bash
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

### Hydro-Quebec API errors:
- Verify credentials are correct in `.env` file
- Check internet connection
- Ensure Hydro-Quebec account is active
- API may have rate limits - wait and retry

### "Using sample data" message:
- This means `.env` file was not found or username/password are missing
- The notebook will use representative sample data
- Create `.env` file from template with at minimum your username and password
- Contract and Customer IDs are optional and can be auto-retrieved

## 📚 Additional Resources

### Hydro-Quebec:
- Rate D: https://www.hydroquebec.com/residential/customer-space/rates/rate-d.html
- Flex D: https://www.hydroquebec.com/residential/customer-space/rates/flex-d.html

### Government Programs:
- iZEV: https://tc.canada.ca/en/road-transportation/innovative-technologies/zero-emission-vehicles/medium-heavy-duty-zero-emission-vehicles/izev-program
- Roulez vert: https://www.quebec.ca/en/transports/electric-vehicles/financial-assistance
- Greener Homes: https://www.nrcan.gc.ca/energy-efficiency/homes/canada-greener-homes-grant/23441

### Vehicle Information:
- VW ID.4: https://www.vw.ca/en/models/id-4.html
- EPA ratings: https://www.fueleconomy.gov/

## 🤝 Contributing

If you find bugs or have suggestions:
1. Create an issue with details
2. Describe expected vs actual behavior
3. Include your Python/Jupyter version

## 📄 License

This notebook is provided as-is for personal use. Modify as needed for your analysis.

## ✅ Checklist Before First Run

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] JupyterLab or Jupyter Notebook installed
- [ ] `.env` file created from template with your credentials
- [ ] `.env` file is in `.gitignore`
- [ ] Jupyter widgets enabled
- [ ] Internet connection available

## 🎯 Quick Start Commands

```bash
# 1. Install everything
pip install jupyter ipywidgets matplotlib pandas numpy requests python-dotenv hydroqc

# 2. Setup credentials
cp .env_template .env
# Edit .env with your Hydro-Quebec username and password
# (Contract/Customer IDs are optional - hydroqc can auto-retrieve them)

# 3. Run notebook
jupyter lab car_analysis.ipynb

# 4. In notebook: Cell → Run All
# 5. Adjust sliders and explore results
```

---

**Need Help?** Check the troubleshooting section or create an issue with your question.

**Ready to analyze?** Open `car_analysis.ipynb` and run all cells! 🚀
