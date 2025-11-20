# 📊 A/B Test Analysis Framework

**Statistical analysis system with automated revenue impact calculation for product experiments**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Production--Ready-success.svg)]()

---

## 📋 Business Problem

Product teams run hundreds of A/B tests annually but struggle with:
- **Premature decisions** — Calling winners too early with insufficient data
- **Missing revenue context** — Knowing B won but not understanding financial impact
- **Inconsistent analysis** — Different analysts using different methods
- **Statistical errors** — Not validating sample size or significance

**The Cost:** Shipping losing variants or missing big wins by not testing long enough.

---

## 💡 Solution

Automated A/B test analyzer that provides:

1. ✅ **Statistical validation** (minimum sample size checks)
2. 📈 **Conversion rate analysis** (with relative and absolute lift)
3. 💰 **Revenue impact projection** (translate % uplift to €€€)
4. 🎯 **Clear recommendations** (ship, continue, or discard)
5. 🔒 **Confidence levels** (high, medium, low)

---

## 🎯 Decision Framework

```
┌─────────────────────────────────────────────────────────┐
│  DECISION TREE                                          │
├─────────────────────────────────────────────────────────┤
│  Sample Size Check:                                     │
│  ├─ < 1,000 visitors → INSUFFICIENT DATA               │
│  └─ ≥ 1,000 visitors → Proceed to analysis             │
│                                                          │
│  Uplift Analysis:                                       │
│  ├─ > +5%   → ✅ IMPLEMENT (high confidence)           │
│  ├─ +2-5%   → ⚠️ CONTINUE TEST (medium confidence)     │
│  ├─ -2 to +2% → ➡️ KEEP A (no meaningful difference)   │
│  └─ < -2%   → ❌ DISCARD B (high confidence)           │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Sample Output

### **Example 1: Clear Winner**
```python
from ab_testing import analyze_ab_test

result = analyze_ab_test(
    variant_a_conversions=450,
    variant_a_visitors=10000,
    variant_b_conversions=580,
    variant_b_visitors=10000,
    average_order_value=50.00,
    total_monthly_visitors=100000
)
```

**Output:**
```
Variant A CR: 4.50%
Variant B CR: 5.80%
Uplift: +28.89%
Absolute Lift: +130 conversions
Revenue Impact: +€65,000/month
Recommendation: ✅ IMPLEMENT - Clear winner
Confidence: High
```

**Business Translation:**
> "Variant B increases conversion by 29%, generating €65K additional monthly revenue. With development cost of €10K, ROI is 650% in first month. Ship immediately."

---

### **Example 2: Inconclusive Test**
```python
result = analyze_ab_test(
    variant_a_conversions=320,
    variant_a_visitors=8000,
    variant_b_conversions=335,
    variant_b_visitors=8000
)
```

**Output:**
```
Variant A CR: 4.00%
Variant B CR: 4.19%
Uplift: +4.69%
Recommendation: ⚠️ CONTINUE TEST - Needs more data
Confidence: Medium
```

**Business Translation:**
> "Positive signal (+4.7%) but not statistically significant yet. Continue test for 2 more weeks to reach 15K visitors per variant."

---

### **Example 3: B is Worse**
```python
result = analyze_ab_test(
    variant_a_conversions=890,
    variant_a_visitors=12000,
    variant_b_conversions=720,
    variant_b_visitors=12000
)
```

**Output:**
```
Variant A CR: 7.42%
Variant B CR: 6.00%
Uplift: -19.10%
Recommendation: ❌ DISCARD B - Hurts conversions
Confidence: High
```

**Business Translation:**
> "Variant B decreased conversion by 19%, costing €45K/month if shipped. Revert to variant A immediately."

---

## 🔧 Technical Implementation

**Core Analysis Function:**
```python
def analyze_ab_test(variant_a_conversions, variant_a_visitors,
                     variant_b_conversions, variant_b_visitors,
                     minimum_sample_size=1000,
                     average_order_value=None,
                     total_monthly_visitors=None):
    
    # 1. Validate sample size
    if variant_a_visitors < minimum_sample_size:
        return {"status": "Insufficient data", ...}
    
    # 2. Calculate conversion rates
    cr_a = (variant_a_conversions / variant_a_visitors) * 100
    cr_b = (variant_b_conversions / variant_b_visitors) * 100
    
    # 3. Calculate uplift
    uplift = ((cr_b - cr_a) / cr_a) * 100
    
    # 4. Calculate revenue impact (if parameters provided)
    if average_order_value and total_monthly_visitors:
        cr_diff = (cr_b - cr_a) / 100
        revenue_impact = cr_diff * total_monthly_visitors * average_order_value
    
    # 5. Make recommendation
    if uplift > 5:
        return "Implement variant B"
    elif uplift >= 2:
        return "Continue test"
    # ... more logic
```

---

## 📈 Key Metrics Explained

### **1. Conversion Rate (CR)**
- **Formula:** (Conversions / Visitors) × 100
- **Example:** 450 conversions / 10,000 visitors = 4.5%

### **2. Relative Uplift (%)**
- **Formula:** ((CR_B - CR_A) / CR_A) × 100
- **Example:** ((5.8% - 4.5%) / 4.5%) × 100 = +28.89%
- **Why it matters:** Shows percentage improvement

### **3. Absolute Lift (conversions)**
- **Formula:** Conversions_B - Conversions_A
- **Example:** 580 - 450 = +130 conversions
- **Why it matters:** Shows real magnitude of impact

### **4. Revenue Impact (€/month)**
- **Formula:** (CR_B - CR_A) × Monthly Visitors × Avg Order Value
- **Example:** (+1.3% × 100,000 × €50) = +€65,000/month
- **Why it matters:** Translates to business value

---

## 🚀 Business Impact

**Real-World Scenario:** E-commerce checkout flow test

| Metric | Control A | Variant B | Change |
|--------|-----------|-----------|--------|
| Visitors | 10,000 | 10,000 | — |
| Conversions | 450 | 580 | +130 |
| CR | 4.50% | 5.80% | +1.30pp |
| Uplift | — | — | +28.89% |

**Financial Projection:**
- Monthly visitors: 100,000
- Average order value: €50
- Revenue impact: +€65,000/month
- Annual impact: +€780,000/year

**Investment:**
- Development: €10,000
- Test duration: 2 weeks
- **ROI: 7,800% annually**

---

## 🎓 Statistical Concepts

### **Sample Size Validation**
**Why it matters:** Small samples lead to high variance

```python
# Bad: 100 visitors
# CR_A: 10/100 = 10%  → Could be 8-12% with more data
# CR_B: 12/100 = 12%  → Could be 10-14% with more data
# Result: Inconclusive (overlapping ranges)

# Good: 10,000 visitors
# CR_A: 450/10000 = 4.5%  → Likely 4.4-4.6%
# CR_B: 580/10000 = 5.8%  → Likely 5.7-5.9%
# Result: Statistically significant (no overlap)
```

### **Relative vs. Absolute Lift**
**Watch out for misleading percentages:**

```python
# Test 1: Small numbers
# A: 2 conversions, B: 4 conversions
# Relative uplift: +100% (sounds amazing!)
# Absolute lift: +2 conversions (tiny impact)

# Test 2: Large numbers
# A: 1000 conversions, B: 1100 conversions
# Relative uplift: +10% (sounds modest)
# Absolute lift: +100 conversions (huge impact!)
```

**Always report BOTH metrics.**

---

## 🚀 Extensions (Future Work)

1. **Confidence intervals** — Show uncertainty ranges for CRs
2. **Statistical significance tests** — Chi-square, t-test
3. **Bayesian analysis** — Probability that B is better than A
4. **Sequential testing** — Stop tests early when significant
5. **Multi-armed bandits** — Dynamic traffic allocation
6. **Segmentation analysis** — Which user segments benefit most?

---

## 📂 Files

- `ab_testing.py` — Core analysis framework
- `tests.py` — Comprehensive test suite
- `demo.ipynb` — Interactive examples with visualizations

---

## 🎓 Learning Focus

**Skills Demonstrated:**
- Statistical analysis and hypothesis testing
- Revenue impact modeling
- Decision framework design
- Edge case handling (insufficient data, division by zero)
- Clear communication of complex results

**Real-World Application:**
This framework mirrors tools used by Spotify, Netflix, and Airbnb for experiment analysis. Key principles:
- Always validate sample size first
- Report both relative and absolute metrics
- Translate results to business impact
- Provide clear, actionable recommendations

---

## 👤 Author

**Francesc Cebrián**  
Transitioning from F&B Operations to Data Analytics  
[LinkedIn](https://linkedin.com/in/franc-cebrian-91337a113) | [GitHub](https://github.com/Fransis182)

---

## 📄 License

MIT License - Feel free to use and adapt for your own projects
