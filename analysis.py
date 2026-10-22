"""RFM Customer Segmentation - segment e-commerce customers by Recency, Frequency, Monetary value (synthetic data)."""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns
sns.set_theme(style="whitegrid"); rng = np.random.default_rng(11)

n_c = 1500; rows = []
for cid in range(1, n_c + 1):
    k = rng.choice([1, 2, 4, 8, 15], p=[.3, .25, .2, .15, .1]); aov = rng.lognormal(4, .5)
    for d in pd.to_datetime("2025-11-01") + pd.to_timedelta(rng.integers(0, 365, k), unit="D"):
        rows.append((cid, d, round(aov * rng.lognormal(0, .3), 2)))
tx = pd.DataFrame(rows, columns=["customer_id", "order_date", "amount"]); tx.to_csv("data/transactions.csv", index=False)

snap = tx.order_date.max() + pd.Timedelta(days=1)
rfm = tx.groupby("customer_id").agg(recency=("order_date", lambda s: (snap - s.max()).days),
                                     frequency=("order_date", "count"), monetary=("amount", "sum"))
rfm["R"] = pd.qcut(rfm.recency, 5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm["F"] = pd.qcut(rfm.frequency.rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["M"] = pd.qcut(rfm.monetary, 5, labels=[1, 2, 3, 4, 5]).astype(int)
def seg(r):
    if r.R >= 4 and r.F >= 4: return "Champions"
    if r.F >= 4: return "Loyal"
    if r.R >= 4 and r.F <= 2: return "New / Promising"
    if r.R <= 2 and r.F >= 3: return "At Risk"
    if r.R <= 2: return "Lost"
    return "Needs Attention"
rfm["segment"] = rfm.apply(seg, axis=1); rfm.to_csv("data/rfm_segments.csv")
s = rfm.groupby("segment").agg(customers=("R", "size"), avg_recency=("recency", "mean"), avg_orders=("frequency", "mean"),
                               revenue=("monetary", "sum")).round(1)
s["revenue_share_%"] = (s.revenue / s.revenue.sum() * 100).round(1); s = s.sort_values("revenue", ascending=False); print(s)
s.to_csv("segment_summary.csv")
s.customers.plot.pie(figsize=(6, 6), autopct="%1.0f%%", title="Customers by Segment", ylabel=""); plt.tight_layout(); plt.savefig("images/segments_customers.png", dpi=130); plt.close()
s["revenue_share_%"].plot.bar(figsize=(9, 4), title="Revenue Share (%) by Segment", rot=20, color="seagreen"); plt.tight_layout(); plt.savefig("images/segments_revenue.png", dpi=130); plt.close()
sns.scatterplot(data=rfm, x="frequency", y="monetary", hue="segment", alpha=.6); plt.title("Frequency vs Monetary"); plt.tight_layout(); plt.savefig("images/scatter.png", dpi=130); plt.close()
