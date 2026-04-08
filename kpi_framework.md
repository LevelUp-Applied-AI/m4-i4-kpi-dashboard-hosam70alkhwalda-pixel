# KPI Framework - Amman Digital Market

Define 5 KPIs for the Amman Digital Market. At least 2 must be time-based and 1 must be cohort-based.

---

## KPI 1

- **Name:*Monthly Revenue Trend*
- **Definition:*Total revenue generated per month*
- **Formula:*SUM(quantity * unit_price) grouped by month*
- **Data Source (tables/columns):*orders.order_date (time dimension), order_items.quantity, products.unit_price*

- **Baseline Value:*~2,400-2,600 JOD per month (with peaks up to 5,086 JOD)*
- **Interpretation:*Revenue mostly stays within the 2,400-2,600 JOD range across months, with a few noticeable spikes. This shows that performance is generally stable rather than consistently increasing.

The sharp increase in June 2025 (5,086 JOD) is much higher than the usual range, which could be linked to a promotion, campaign, or seasonal factor that needs further investigation.*

---

## KPI 2

- **Name:*Weekly Order Volume*
- **Definition:*Number of orders placed per week*
- **Formula:*COUNT(order_id) grouped by week*
- **Data Source (tables/columns):*orders (order_date, status)*
- **Baseline Value:*~5-7 orders per week, with peaks up to 21 orders*
- **Interpretation:*Weekly orders are generally stable, averaging around 5-7 orders most of the time. However, there are clear spikes in certain periods, especially in March and June 2025.

The peak of 21 orders in late June 2025 is significantly higher than the normal range, showing a short-term increase in demand.

These spikes happen at the same time as increases in monthly revenue, which suggests that the higher revenue during these periods is mainly driven by more orders rather than gradual growth*

---

## KPI 3

- **Name:*Revenue by City*
- **Definition:*Total revenue generated per city*
- **Formula:*SUM(quantity * unit_price) grouped by city*
- **Data Source (tables/columns):*customers (city), orders, order_items, products*
- **Baseline Value:*Amman: 15,719 JOD (highest), followed by Irbid: 7,250 JOD*
- **Interpretation:*Amman clearly generates the highest revenue, more than double that of Irbid, which comes second. This indicates that most of the business activity is concentrated in Amman.

A noticeable portion of revenue (7,554 JOD) is grouped under "Unknown", which means some customer location data is missing and may affect the accuracy of this analysis.

The rest of the cities show relatively similar revenue levels, suggesting that demand outside Amman is more spread out but at a lower level. Improving location data quality would help provide more reliable insights.*

---

## KPI 4

- **Name:*Average Order Value by Product Category*
- **Definition:*Average value of customer orders within each product category*
- **Formula:*AVG(SUM(quantity * unit_price) per order per category*
- **Data Source (tables/columns):*products (category), order_items (quantity), products (unit_price), orders*

- **Baseline Value:*Books: 70.46 JOD (highest), Food & Beverage: 27.26 JOD (lowest)*
- **Interpretation:*There is a clear difference in average order value across categories. Books have the highest value (70.46 JOD), followed by Electronics and Clothing.

Categories like Food & Beverage and Sports are much lower, around 27 JOD, which shows that purchases in these categories tend to be smaller.

This gap suggests that customer spending behavior changes depending on the product type. Focusing on higher-value categories could help increase revenue, while lower-value ones may benefit from bundling or promotional strategies.*

---

## KPI 5

- **Name:*Customer Purchase Frequency*
- **Definition:*Average number of orders per customer*
- **Formula:*AVG(COUNT(order_id) per customer)*
- **Data Source (tables/columns):*orders (customer_id, order_id, status)*
- **Baseline Value:*4.43 orders per customer*
- **Interpretation:*Customers place an average of 4.43 orders, which shows that many users return and make multiple purchases.

This indicates a relatively strong level of customer retention and engagement.

When looking at this alongside revenue and order spikes, it suggests that performance is driven by both repeat customers and occasional increases in demand. Strengthening loyalty programs or personalized offers could help improve this further.*

---

KPI 3 - Statistical Validation

Test: Independent Samples t-test

Why this test: Used to compare the average order revenue between two independent groups (Amman vs Irbid)

Hypothesis:
H0: There is no difference in average order revenue between Amman and Irbid  
H1: There is a difference in average order revenue between Amman and Irbid  

Result:
t-statistic: 0.63  
p-value: 0.527  

Interpretation:
Since the p-value is greater than 0.05, the difference in average order revenue between Amman and Irbid is not statistically significant and could be due to random variation.

This means that although Amman generates higher total revenue, this is likely driven by a higher number of orders rather than higher spending per order.

Effect Size (Cohen’s d):
Value: 0.09

Effect Size Interpretation:
This represents a very small (negligible) effect size, indicating that the difference between the two cities has minimal practical impact on customer spending behavior.

---

KPI 4 - Statistical Validation

Test: One-way ANOVA

Why this test: Used to compare average order values across multiple product categories

Hypothesis:
H0: All product categories have the same average order value  
H1: At least one category has a different average order value  

Result:
F-statistic: 56.78  
p-value: 2.11e-52  

Interpretation:
Since the p-value is far below 0.05, the differences in average order value across product categories are statistically significant.

This confirms that customer spending behavior varies depending on the type of product, and that category is a key factor influencing order value.

Effect Size (Eta Squared):
Value: 0.21

Effect Size Interpretation:
This indicates a moderate-to-strong effect size, meaning that product category has a meaningful impact on how much customers spend per order.