# 💰 Pricing Tier Recommendation Engine

**Context-aware recommendation system for optimizing free-to-paid conversions in freemium SaaS**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Production--Ready-success.svg)]()

---

## 📋 Business Problem

Freemium SaaS products face two critical challenges:

1. **Under-selling:** Recommending plans that don't meet user needs → friction, churn
2. **Over-selling:** Recommending expensive plans users don't need → low conversion

**The Balance:** Recommend the optimal tier that:
- ✅ Covers current usage
- ✅ Provides growth headroom
- ✅ Maximizes conversion probability

---

## 💡 Solution

**Multi-constraint recommendation engine** that analyzes:
1. **Projects created** (capacity need)
2. **Storage used** (data requirements)
3. **Team size** (collaboration need)
4. **Support tickets** (service level need)

Then maps to optimal pricing tier with clear reasoning and confidence level.

---

## 🎯 Pricing Tiers

| Plan | Price/Month | Limits | Target User |
|------|-------------|--------|-------------|
| **Free** | €0 | 5 projects, 1 GB, 1 user | Individual learners |
| **Starter** | €12 | 20 projects, 10 GB, 3 users | Small teams |
| **Pro** | €29 | Unlimited projects, 100 GB, 10 users | Growing teams |
| **Enterprise** | €99 | Unlimited everything + priority support | Large organizations |

---

## 📊 Decision Logic

```
┌─────────────────────────────────────────────────────────┐
│  RECOMMENDATION HIERARCHY (evaluated top to bottom)     │
├─────────────────────────────────────────────────────────┤
│  1. ENTERPRISE                                          │
│     └─ IF team > 10 OR support_tickets >= 5            │
│        → "Large team or high support needs"            │
│                                                          │
│  2. PRO                                                 │
│     └─ IF projects > 20 OR storage > 10 OR team > 3    │
│        → "Exceeds Starter limits"                      │
│                                                          │
│  3. STARTER                                            │
│     └─ IF projects > 5 OR storage > 1 OR team > 1      │
│        → "Exceeds Free limits"                         │
│                                                          │
│  4. FREE (default)                                     │
│     └─ IF all usage within free limits                 │
│        → "Current usage fits Free plan"                │
└─────────────────────────────────────────────────────────┘
```

**Key Design Principle:** Use `OR` conditions (not `AND`) so any single constraint triggers upgrade.

---

## 📊 Sample Output

### **Example 1: Starter Recommendation**
```python
from pricing import recommend_pricing_tier

result = recommend_pricing_tier(
    projects_created=15,
    storage_used_gb=8,
    team_members=2,
    support_tickets_last_month=0
)
```

**Output:**
```
Recommended Plan: Starter
Reasoning: Usage exceeds Free plan limits. Starter offers necessary growth margin.
Upsell Trigger: Starter plan trial or discount offer
Confidence: High

Current Usage:
  - Projects: 15 (vs. Free limit: 5)
  - Storage: 8 GB (vs. Free limit: 1 GB)
  - Team: 2 members (vs. Free limit: 1)
```

**Business Action:**
> Send email: "You've created 15 projects! Upgrade to Starter for 20 projects + 10 GB storage for just €12/month. First month free."

---

### **Example 2: Enterprise Recommendation**
```python
result = recommend_pricing_tier(
    projects_created=50,
    storage_used_gb=80,
    team_members=15,
    support_tickets_last_month=6
)
```

**Output:**
```
Recommended Plan: Enterprise
Reasoning: Large team or high support needs require Enterprise
Upsell Trigger: Offer dedicated account manager
Confidence: High

Current Usage:
  - Projects: 50 (needs unlimited)
  - Storage: 80 GB (needs unlimited)
  - Team: 15 members (exceeds Pro limit: 10)
  - Support: 6 tickets (high touch needed)
```

**Business Action:**
> Assign dedicated Account Manager. Schedule call to discuss priority support, SLA, and volume discounts.

---

### **Example 3: Pro Recommendation (Storage-Driven)**
```python
result = recommend_pricing_tier(
    projects_created=10,
    storage_used_gb=15,
    team_members=2,
    support_tickets_last_month=0
)
```

**Output:**
```
Recommended Plan: Pro
Reasoning: Usage exceeds Starter limits (storage). Pro offers more capacity.
Upsell Trigger: Pro plan benefits presentation & 1-month free trial
Confidence: Medium

Current Usage:
  - Projects: 10 (within Starter limit: 20)
  - Storage: 15 GB (EXCEEDS Starter limit: 10 GB) ← Trigger
  - Team: 2 members (within Starter limit: 3)
```

**Business Action:**
> "You're using 15 GB (Starter max: 10 GB). Upgrade to Pro for 100 GB storage + unlimited projects."

---

## 🔧 Technical Implementation

**Core Recommendation Logic:**
```python
def recommend_pricing_tier(projects_created, storage_used_gb, 
                          team_members, support_tickets_last_month):
    
    # Priority 1: Enterprise (most valuable, check first)
    if team_members > 10 or support_tickets_last_month >= 5:
        return {
            "recommended_plan": "Enterprise",
            "reasoning": "Large team or high support needs require Enterprise",
            "upsell_trigger": "Offer dedicated account manager",
            "confidence": "High"
        }
    
    # Priority 2: Pro (exceeds Starter capacity)
    elif projects_created > 20 or storage_used_gb > 10 or team_members > 3:
        return {
            "recommended_plan": "Pro",
            "reasoning": "Usage exceeds Starter limits",
            "confidence": "Medium"
        }
    
    # Priority 3: Starter (exceeds Free capacity)
    elif projects_created > 5 or storage_used_gb > 1 or team_members > 1:
        return {
            "recommended_plan": "Starter",
            "reasoning": "Usage exceeds Free plan limits",
            "confidence": "High"
        }
    
    # Default: Free
    else:
        return {
            "recommended_plan": "Free",
            "reasoning": "Current usage fits Free plan limits",
            "confidence": "High"
        }
```

**Why This Works:**
- **Hierarchical evaluation** — Most valuable tiers checked first
- **Multi-constraint OR logic** — Any limit trigger = upgrade
- **Clear reasoning** — Explains WHY this plan was chosen
- **Upsell triggers** — Actionable next steps for sales team

---

## 📈 Business Impact

### **Scenario:** 10,000 free users analyzed

| Current Plan | Count | Recommended | Expected Conversion | New MRR |
|--------------|-------|-------------|---------------------|---------|
| Free → Free | 6,000 | Free | — | €0 |
| Free → Starter | 2,500 | Starter | 25% (625 users) | €7,500 |
| Free → Pro | 1,200 | Pro | 15% (180 users) | €5,220 |
| Free → Enterprise | 300 | Enterprise | 30% (90 users) | €8,910 |

**Total Impact:**
- **New MRR:** €21,630/month
- **Annual increase:** €259,560
- **Average LTV per converted user:** €348

### **Conversion Optimization**

**Without Smart Recommendations:**
- Offer Pro to all free users
- 5% conversion rate (too expensive for most)
- 500 conversions × €29 = €14,500 MRR

**With Smart Recommendations:**
- Match tier to usage pattern
- 895 total conversions (weighted by tier)
- €21,630 MRR (**+49% improvement**)

---

## 🎯 Key Insights

### **1. Multi-Constraint is Better Than Single**

❌ **Bad:** `if projects_created > 20 AND storage > 10 AND team > 3`  
- User needs Pro but only 1 condition is met → Stuck on wrong plan

✅ **Good:** `if projects_created > 20 OR storage > 10 OR team > 3`  
- User needs Pro if ANY limit is exceeded → Correct recommendation

### **2. Hierarchy Prevents Under-Selling**

**Example without hierarchy:**
```python
# User: 25 projects, 15 team members
if projects_created > 5:
    return "Starter"  # WRONG! (evaluated first, returned immediately)
```

**With hierarchy:**
```python
# Check Enterprise first (team > 10)
# → Returns "Enterprise" (CORRECT)
```

### **3. Confidence Levels Enable Automation**

| Confidence | Action | Example |
|------------|--------|---------|
| **High** | Automated email | Free → Starter (clear need) |
| **Medium** | Sales review | Starter → Pro (borderline) |
| **Low** | Manual analysis | Edge cases |

---

## 🚀 Extensions (Future Work)

### **1. Headroom Analysis**
```python
# Calculate % of limit used
project_usage_pct = (projects_created / limit) * 100

if project_usage_pct > 80:
    urgency = "URGENT - Will hit limit soon"
elif project_usage_pct > 60:
    urgency = "Medium - Proactive upgrade"
```

### **2. Growth Prediction**
```python
# Estimate time to hit limit
growth_rate = 3  # projects per month
months_to_limit = (20 - projects_created) / growth_rate
# "Will hit Starter limit in 2 months"
```

### **3. Revenue Impact Calculation**
```python
# What's the financial value of this upsell?
current_plan_mrr = 0  # Free
recommended_plan_mrr = 12  # Starter
monthly_increase = recommended_plan_mrr - current_plan_mrr
annual_increase = monthly_increase * 12
# "Upselling generates €144/year from this user"
```

### **4. Feature Unlock Value**
```python
# Show value of premium features
if recommended_plan == "Pro":
    unlocked_features = [
        "Unlimited projects",
        "Advanced analytics dashboard",
        "API access",
        "Priority email support"
    ]
    # "Upgrade to unlock: Unlimited projects + Advanced analytics"
```

---

## 📂 Files

- `pricing.py` — Core recommendation engine
- `tests.py` — 11 comprehensive test cases
- `demo.ipynb` — Interactive examples with business scenarios

---

## 🎓 Learning Focus

**Skills Demonstrated:**
- Multi-constraint decision logic (OR conditions)
- Hierarchical evaluation (priority-based)
- Context-aware recommendations (confidence levels)
- Clear business reasoning (explainable AI)
- Revenue optimization strategy

**Real-World Application:**
This system mirrors pricing recommendation engines used by Notion (workspace tiers), Canva (design tiers), and Loom (video tiers). Core principles:
- Analyze multiple usage dimensions
- Recommend tier that fits + provides headroom
- Balance conversion vs. revenue maximization
- Provide clear reasoning for transparency

---

## 👤 Author

**Francesc Cebrián**  
Transitioning from F&B Operations to Data Analytics  
[LinkedIn](https://linkedin.com/in/franc-cebrian-91337a113) | [GitHub](https://github.com/Fransis182)

---

## 📄 License

MIT License - Feel free to use and adapt for your own projects
