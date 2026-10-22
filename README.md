# RFM Customer Segmentation (Business Analysis)

Segments 1,500 e-commerce customers by **Recency, Frequency, Monetary value** and sizes each segment's revenue.
> Data is **synthetic** (seeded in `analysis.py`).

## Key findings
- **Champions** are 26% of customers but **56.5% of revenue**.
- Champions + Loyal = ~76% of revenue.
- *Lost* (376) and *At Risk* (131) customers are a win-back opportunity.

## Recommendations
- Reward Champions (early access, loyalty tiers).
- Run win-back campaigns for At Risk customers before they become Lost.
- Nurture New/Promising customers with a second-purchase offer.

## Run
`pip install -r requirements.txt && python analysis.py`

![](images/segments_revenue.png)
![](images/segments_customers.png)
