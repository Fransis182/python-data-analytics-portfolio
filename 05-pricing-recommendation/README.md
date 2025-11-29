💰 Pricing Tier Recommendation Engine

Context-aware recommendation system for optimizing free-to-paid conversions in a SaaS product.




📋 Business Problem

Freemium SaaS companies often struggle with:

Under-selling: Recommending plans that don’t meet the user’s needs

Over-selling: Offering expensive plans that the user doesn’t need

Low conversion rates due to lack of personalization

Churn risks when users hit limits unexpectedly

Goal: Recommend the optimal paid tier for each free user based on real usage.

💡 Solution

A multi-constraint recommendation engine that evaluates four key usage signals:

Projects created — productivity needs

Storage used — data intensity

Team members — collaboration needs

Support tickets — service level requirements

The engine returns:

Recommended plan

Why that plan was chosen

Upsell trigger message

Confidence level of the recommendation

🎯 Pricing Tiers
Plan	Price	Limits	Best For
Free	€0	5 projects, 1 GB, 1 user	Individuals
Starter	€12	20 projects, 10 GB, 3 users	Small teams
Pro	€29	Unlimited projects, 100 GB, 10 users	Growing teams
Enterprise	€99	Unlimited everything + priority support	Large orgs
🔍 Decision Logic
IF team_members > 10 OR support_tickets >= 5
    → Enterprise

ELIF projects > 20 OR storage > 10 OR team_members > 3
    → Pro

ELIF projects > 5 OR storage > 1 OR team_members > 1
    → Starter

ELSE
    → Free


Design principle:
Use OR for each tier → any limit exceeded triggers an upgrade.

📊 Sample Output
Example: Pro Recommendation (Storage-driven)
from pricing_recommendation import recommend_pricing_tier

recommend_pricing_tier(
    projects_created=10,
    storage_used_gb=15,
    team_members=2,
    support_tickets_last_month=0
)


Output

Recommended Plan: Pro
Reasoning: Usage exceeds Starter limits (storage). Pro offers more capacity.
Upsell Trigger: Pro plan benefits presentation & 1-month free trial
Confidence: Medium

🔧 Core Implementation
def recommend_pricing_tier(projects_created, storage_used_gb, team_members,
                           support_tickets_last_month):
    
    if team_members > 10 or support_tickets_last_month >= 5:
        return {
            "recommended_plan": "Enterprise",
            "reasoning": "Large team or high support needs require Enterprise",
            "upsell_trigger": "Offer dedicated account manager",
            "confidence": "High"
        }

    elif projects_created > 20 or storage_used_gb > 10 or team_members > 3:
        return {
            "recommended_plan": "Pro",
            "reasoning": "Usage exceeds Starter limits",
            "upsell_trigger": "Present Pro benefits & free trial",
            "confidence": "Medium"
        }

    elif projects_created > 5 or storage_used_gb > 1 or team_members > 1:
        return {
            "recommended_plan": "Starter",
            "reasoning": "Usage exceeds Free plan limits",
            "upsell_trigger": "Starter plan trial or discount",
            "confidence": "High"
        }

    else:
        return {
            "recommended_plan": "Free",
            "reasoning": "Current usage fits Free plan limits",
            "upsell_trigger": "No action needed",
            "confidence": "High"
        }

📈 Business Impact

Scenario: 10,000 free users

Recommendation	Users	Expected Conversion	New MRR
Free	6,000	—	€0
Starter	2,500	25%	€7,500
Pro	1,200	15%	€5,220
Enterprise	300	30%	€8,910

Total new MRR: €21,630/month
Annual impact: €259,560

🎯 Key Learnings

Multi-constraint logic prevents wrong recommendations

Hierarchical evaluation avoids under-selling

High-confidence recommendations can be automated

Clear reasoning supports transparency with users and sales teams

🚀 Extensions (Future Work)

Headroom forecasting (time to hit next limit)

Upsell probability model (ML-based)

LTV uplift estimation

Feature unlock previews (“upgrade to unlock X and Y”)

📂 Files

pricing_recommendation.py — Core engine

tests.py — 11 validation test cases

demo.ipynb — Jupyter demo with scenarios

👤 Author

Francesc Cebrián
Transitioning from F&B Operations to Data Analytics
LinkedIn
 | GitHub

📄 License

MIT License — free to use and modify.
