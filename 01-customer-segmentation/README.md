# 👥 Customer Segmentation Engine

**Automated user classification system for churn prevention in SaaS products**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Production--Ready-success.svg)]()

---

## 📋 Business Problem

SaaS companies face a critical challenge: **15-30% annual churn rate** among free users. Without proactive engagement strategies, valuable users slip away unnoticed.

**Key Questions:**
- Which users are at risk of churning?
- When should we trigger re-engagement campaigns?
- Who are our power users ready for upsell?

---

## 💡 Solution

Automated classification system that segments users into four actionable categories based on login recency:

| Segment | Definition | Action | Business Impact |
|---------|-----------|--------|-----------------|
| **Highly Active** | < 1 day since login | Offer special promotion | Upsell opportunity |
| **Active** | 1-7 days since login | No action needed | Healthy engagement |
| **At Risk** | 7-30 days since login | Send re-engagement email | Churn prevention |
| **Churned** | 30+ days since login | Add to win-back campaign | Recovery effort |

---

## 🎯 Key Features

✅ **Simple, interpretable logic** — Easy to explain to non-technical stakeholders  
✅ **Actionable segments** — Each segment has a clear business action  
✅ **Scalable architecture** — Can process thousands of users in batch  
✅ **Edge case handling** — Validates inputs and handles boundary conditions  

---

## 📊 Sample Output

```python
from segmentation import classify_user_status

# Example: User who logged in 15 days ago
status, action = classify_user_status(15)

print(f"Status: {status}")  # "At Risk"
print(f"Action: {action}")  # "Send re-engagement email"
```

**Batch Processing:**
```python
users = [
    ("user_001", 3),
    ("user_002", 15),
    ("user_003", 45)
]

for user_id, days in users:
    status, action = classify_user_status(days)
    print(f"{user_id}: {status} → {action}")
```

**Output:**
```
user_001: Active → No action needed
user_002: At Risk → Send re-engagement email
user_003: Churned → Add to win-back campaign
```

---

## 🔧 Technical Implementation

**Core Logic:**
```python
def classify_user_status(days_since_last_login):
    if days_since_last_login < 1:
        return "Highly Active", "Offer special promotion"
    elif days_since_last_login < 7:
        return "Active", "No action needed"
    elif days_since_last_login <= 30:
        return "At Risk", "Send re-engagement email"
    else:
        return "Churned", "Add to win-back campaign"
```

**Why this approach works:**
- Uses **recency** as primary indicator (strongest churn predictor)
- Clear threshold boundaries (no gray areas)
- Returns both **status** and **action** (ready for automation)

---

## 📈 Business Impact

**Scenario:** 10,000 user base

| Segment | Count | % | Monthly Revenue Impact |
|---------|-------|---|----------------------|
| Highly Active | 500 | 5% | €6,000 (upsell opportunity) |
| Active | 6,500 | 65% | €78,000 (retained) |
| At Risk | 2,000 | 20% | €24,000 (at risk) |
| Churned | 1,000 | 10% | €12,000 (lost) |

**Action Plan:**
- **At Risk (2,000 users):** Launch email campaign → 30% recovery = €7,200 saved/month
- **Highly Active (500 users):** Upsell promotion → 15% conversion = €900 new MRR

---

## 🚀 Extensions (Future Work)

1. **Add RFM model** (Recency + Frequency + Monetary value)
2. **Feature importance analysis** (which features predict churn best?)
3. **Predictive scoring** (ML model to predict churn probability)
4. **Cohort analysis** (compare segments over time)

---

## 📂 Files

- `segmentation.py` — Core classification logic
- `tests.py` — Unit tests for edge cases
- `demo.ipynb` — Interactive Jupyter notebook with examples

---

## 🎓 Learning Focus

**Skills Demonstrated:**
- Conditional logic and control flow
- Function design with multiple return values
- Edge case handling
- Business logic implementation
- Scalable batch processing

**From Tutorial to Production:**
This project evolved from a Kaggle exercise on conditional statements into a production-ready system by adding:
- Input validation
- Batch processing capability
- Clear documentation
- Business context

---

## 👤 Author

**Francesc Cebrián**  
Transitioning from F&B Operations to Data Analytics  
[LinkedIn](https://linkedin.com/in/franc-cebrian-91337a113) | [GitHub](https://github.com/Fransis182)

---

## 📄 License

MIT License - Feel free to use and adapt for your own projects
