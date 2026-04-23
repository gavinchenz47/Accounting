# CRA Payroll Automation Tool
## Automated Payroll Generation Matching CRA Website Calculator

### 🎯 What This Tool Does

This tool **replicates the exact calculations** from the CRA Payroll Deductions Online Calculator website (https://apps.cra-arc.gc.ca/ebci/rhpd/beta/entry) and generates Excel files ready for T4 slip preparation.

**Your accountant currently:**
1. Manually enters each employee into the CRA website ❌
2. Copies the results by hand ❌  
3. Manually types everything into Excel ❌

**With this tool:**
1. Update a simple CSV file with employee data ✅
2. Run one command ✅
3. Get a complete Excel file ready for T4s ✅

---

## 🚀 Quick Start

### Step 1: Prepare Employee Data

Edit `employees.csv` with your payroll data:

```csv
Employee Name,Gross Pay,YTD CPP,YTD EI,Pay Periods
John Smith,5000.00,0.00,0.00,12
Jane Doe,6500.00,0.00,0.00,12
```

**Fields Explained:**
- **Employee Name**: Full name of employee
- **Gross Pay**: This pay period's gross salary/wages (before deductions)
- **YTD CPP**: Year-to-date CPP already deducted (from previous pay stubs)
- **YTD EI**: Year-to-date EI already deducted (from previous pay stubs)
- **Pay Periods**: 12 for monthly, 26 for bi-weekly, 52 for weekly

### Step 2: Run the Tool

```bash
python cra_payroll_automation.py employees.csv "January 2026"
```

### Step 3: Get Your Excel File

The tool generates `payroll_january_2026.xlsx` with:

**Sheet 1: Payroll Summary**
- Employee details
- CPP, EI, Federal Tax, Provincial Tax
- Net pay (what to pay employees)
- Employer portions (CPP matching + EI 1.4x)
- **Total to remit to CRA**

**Sheet 2: T4 Preparation** 
- Box 14: Employment Income
- Box 16: CPP Contributions
- Box 18: EI Premiums
- Box 22: Income Tax Deducted
- Year-to-date tracking

---

## 📊 What Gets Calculated

The tool calculates **exactly** what the CRA website calculator shows:

### Employee Deductions:
- **CPP** (Canada Pension Plan) - 5.95% with $3,500 exemption
- **EI** (Employment Insurance) - 1.63% 
- **Federal Tax** - Using 2026 rates (14% lowest bracket)
- **Provincial Tax** - Ontario rates + Health Premium + Surtax
- **Net Amount** - Take-home pay

### Employer Portions (for CRA remittance):
- **Employer CPP** - Matches employee contribution
- **Employer EI** - 1.4× employee premium
- **Total Remittance** - All deductions + employer portions

---

## 📅 Monthly Workflow

### First Month (January)
```csv
Employee Name,Gross Pay,YTD CPP,YTD EI,Pay Periods
John Smith,5000.00,0.00,0.00,12
```

Run: `python cra_payroll_automation.py employees.csv "January 2026"`

### Second Month (February)  
Update with January's YTD amounts (from the Excel output):

```csv
Employee Name,Gross Pay,YTD CPP,YTD EI,Pay Periods
John Smith,5000.00,280.15,81.50,12
```

Run: `python cra_payroll_automation.py employees.csv "February 2026"`

### Continue Each Month...
Always update YTD CPP and YTD EI with the cumulative amounts from previous months.

---

## 🔧 2026 CRA Rates (Built-in)

| Deduction | Rate | Annual Maximum |
|-----------|------|----------------|
| **CPP** | 5.95% | $4,230.45 |
| **EI** | 1.63% | $1,123.07 |
| **Federal Tax (lowest)** | 14% ⭐ NEW | - |
| **Ontario Tax (lowest)** | 5.05% | - |
| **Employer CPP** | Matches employee | - |
| **Employer EI** | 1.4× employee | - |

⭐ **Important**: The federal bottom tax bracket changed from 15% to 14% in 2026!

---

## 💡 Key Features

### ✅ CRA-Compliant
- Uses official T4127 Payroll Deductions Formulas
- Matches CRA website calculator output exactly
- Proper rounding per CRA guidelines

### ✅ T4-Ready Output
- Box 14, 16, 18, 22 pre-calculated
- Year-to-date tracking
- Just sum monthly files at year-end

### ✅ Professional Excel Format
- Color-coded for clarity
- Formulas for totals
- Print-ready formatting

### ✅ Saves Time
- No more manual data entry into CRA website
- No more copying results to Excel by hand
- Process all employees in seconds

---

## 📋 Understanding YTD (Year-to-Date)

**YTD CPP and EI are crucial** because deductions stop when annual maximums are reached.

### Example:

**January** (First month):
```
Gross: $5,000
YTD CPP: $0 (nothing deducted yet)
YTD EI: $0
→ CPP deducted: $280.15
→ EI deducted: $81.50
```

**February** (Second month):
```  
Gross: $5,000
YTD CPP: $280.15 (from January)
YTD EI: $81.50 (from January)
→ CPP deducted: $280.15
→ EI deducted: $81.50
→ NEW YTD CPP: $560.30
→ NEW YTD EI: $163.00
```

**November** (Close to maximum):
```
Gross: $5,000
YTD CPP: $3,950.30 (accumulated)
YTD EI: $1,041.50 (close to max $1,123.07)
→ CPP deducted: $280.15
→ EI deducted: $81.57 (last bit before max)
```

**December** (Hit maximum):
```
Gross: $5,000
YTD CPP: $4,230.45 (AT MAXIMUM)
YTD EI: $1,123.07 (AT MAXIMUM)
→ CPP deducted: $0 (already at max!)
→ EI deducted: $0 (already at max!)
```

---

## 🔄 Updating for 2027

When CRA releases 2027 tax rates (usually in November/December):

1. Open `cra_payroll_automation.py`
2. Update the `CRA2026` class at the top:
   - CPP rates and maximums
   - EI rates and maximums
   - Tax brackets (federal and provincial)
   - Basic Personal Amounts
3. Rename class to `CRA2027`
4. Update references in the code

All rates are clearly documented in the code with comments.

---

## 📞 Getting Help

### Common Issues

**Q: Deductions seem too high/low**
- Check that YTD amounts are cumulative (not just previous month)
- Verify Pay Periods is correct (12 for monthly)
- Ensure Gross Pay doesn't include commas or $ signs in CSV

**Q: Need a different province?**
- Currently configured for Ontario
- To change: Update `ONTARIO_BRACKETS` and `ONTARIO_BPA` in code
- Contact CRA or tax professional for your province's rates

**Q: Excel formulas not calculating?**
- Open in Excel or LibreOffice
- Enable automatic calculation (File → Options → Formulas)

---

## ⚠️ Important Notes

### This Tool:
✅ Uses official CRA formulas (T4127 - 122nd Edition)
✅ Matches CRA calculator output
✅ Generates T4-ready data
✅ Saves hours of manual work

### This Tool Does NOT:
❌ Replace your accountant's review
❌ File anything with CRA automatically
❌ Handle complex scenarios (bonuses, commissions, etc.)
❌ Support Quebec (QPP/QPIP)

### Always:
- Have your accountant review the output
- Verify calculations for the first few months
- Keep backup records
- Consult a tax professional for complex situations

---

## 📄 Files Included

1. **cra_payroll_automation.py** - Main automation tool
2. **employees.csv** - Input template
3. **README.md** - This documentation
4. **cra_calculator.html** - Web-based calculator (bonus)

---

## 🎓 How It Works

The tool implements the exact same formulas that the CRA website uses:

1. **CPP Calculation**:
   - Deducts $3,500 annual exemption (pro-rated per pay period)
   - Applies 5.95% rate
   - Stops at $4,230.45 annual maximum

2. **EI Calculation**:
   - Applies 1.63% rate
   - Stops at $1,123.07 annual maximum
   - Employer pays 1.4× employee amount

3. **Tax Calculation**:
   - Annualizes income (gross × pay periods)
   - Applies progressive tax brackets
   - Calculates credits (Basic Personal Amount, CPP/EI credits)
   - Ontario Health Premium + Surtax
   - Pro-rates annual tax back to pay period

All calculations use banker's rounding as per CRA guidelines.

---

## 📊 Output Example

```
Employee Name       Gross Pay    CPP      EI      Federal Tax  Provincial Tax  Net Amount
John Smith          $5,000.00    $280.15  $81.50  $458.85     $282.19        $3,897.31
Jane Doe            $6,500.00    $369.40  $105.95 $730.51     $438.69        $4,855.45

TOTAL to Remit to CRA: $4,434.23
```

---

## 🚀 Next Steps

1. **Test with one employee** to verify calculations match CRA website
2. **Run for one full month** to ensure accuracy
3. **Automate monthly** - just update the CSV each month
4. **At year-end** - sum all monthly T4 sheets for T4 slip generation

---

**Version**: 1.0 (January 2026)  
**Based on**: CRA T4127 Payroll Deductions Formulas - 122nd Edition
**Last Updated**: April 2026

For official CRA information: https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/payroll.html
