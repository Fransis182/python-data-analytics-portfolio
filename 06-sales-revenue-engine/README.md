📈 Sales Revenue Analysis Engine

End-to-end sales analytics system for KPI monitoring, anomaly detection, and revenue forecasting




🧩 Business Problem

Commercial teams often lack a clear, automated way to monitor revenue performance:

Which products are generating the most revenue?

Are sales increasing or decreasing week to week?

Which segments or regions are underperforming?

Are there anomalies or unexpected sales spikes?

Can we estimate next week’s revenue?

Manual Excel-based reporting is slow and error-prone.
Companies need a simple but powerful Python engine that transforms raw sales data into business insights.

🎯 Project Goals

This engine processes daily sales transactions and produces:

✔️ Key Performance Indicators

Total revenue

Number of units sold

Average order value (AOV)

Avg. price per unit

Revenue by product

Revenue by region

Top 5 products

Low performers

✔️ Week-over-week performance

Revenue growth %

Units sold growth %

AOV growth %

✔️ Anomaly Detection

Detects unusual revenue spikes or drops using a simple statistical rule:

If revenue_today > mean + 2×std  → spike alert
If revenue_today < mean - 2×std  → drop alert

✔️ Simple Forecast

A lightweight next-week forecast using rolling averages.

📊 Example Insights (Auto-Generated)

Below is a sample of what the engine produces:

Total Revenue: €42,890  
Units Sold: 3,921  
Average Order Value: €24.10  
Top Product: “Product A” (€12,500 revenue)  
Region at Risk: “South Europe” (-12% WoW)
Revenue spike detected on 2025-06-14 → +48% above normal
Next week expected revenue: €43,500 – €45,200

🛠️ How the Engine Works
1. Load Sales Data

From CSV (included in this folder):

date,product,units_sold,unit_price,region
2025-06-01,Product A,120,12.90,South
2025-06-01,Product B,80,19.99,North
...

2. Calculate Daily KPIs

Python computes totals, averages, and breakdowns:

df["revenue"] = df["units_sold"] * df["unit_price"]
daily_summary = df.groupby("date")["revenue"].sum()

3. Generate Weekly Comparison

Compare this week vs last week:

weekly = df.resample("W", on="date").revenue.sum()
growth = (weekly[-1] - weekly[-2]) / weekly[-2] * 100

4. Detect Anomalies

Using standard deviation thresholds:

mean = daily_summary.mean()
std = daily_summary.std()

if today_revenue > mean + 2 * std:
    alert = "Spike detected"

5. Forecast Revenue

Simple moving average forecast:

forecast = daily_summary.tail(7).mean() * 7

📂 Project Structure
06-sales-revenue-engine/
│
├── sales_data.csv          # Example dataset (synthetic)
├── sales_dashboard.py      # Main analysis & KPI engine
└── README.md               # Project documentation

🚀 Skills Demonstrated

Python (Pandas, datetime, stats)

KPI computation & business analytics

Time-series grouping & resampling

Anomaly detection with thresholds

Forecasting using rolling averages

Clean, well-structured code

Storytelling with data

Real business context (Sales + Revenue)

🧪 Next Improvements (Future Work)

Add product margin data → profit insights

Add customer segmentation → repeat vs new customers

Upgrade forecast to ARIMA/Prophet

Build BI dashboard (Power BI / Looker Studio)

Add SQL data ingestion (PostgreSQL)

👤 Author

Francesc Cebrián Ruiz
Junior Data Analyst (Python + SQL)
LinkedIn
 | GitHub

📄 License

MIT – Free to use, modify, and learn from.