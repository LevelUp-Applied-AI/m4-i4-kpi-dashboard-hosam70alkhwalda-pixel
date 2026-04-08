# Executive Summary - Amman Digital Market Analytics

## Top Findings

1. Revenue performance is largely flat over time, averaging 2,400-2,600 JOD per month, with growth driven by isolated spikes such as the jump to 5,086 JOD in June 2025 rather than sustained momentum.

2. Product category has a clear impact on customer spending, with high-value categories like Books (~70 JOD per order) generating more than double the average of lower-value categories such as Food & Beverage (~27 JOD).

3. Amman accounts for the majority of revenue (15,719 JOD), yet customer spending behavior is consistent across cities, with no statistically significant difference in order value between Amman and Irbid (p ~ 0.53).

## Supporting Data

Finding 1 is supported by the Monthly Revenue KPI, which shows stable baseline performance with a sharp peak at 5,086 JOD, and the Weekly Order Volume KPI, where order counts rise from a typical 5-7 orders to peaks of 21. Evidence is shown in monthly_revenue.png and weekly_orders.png.

Finding 2 is supported by the Average Order Value by Category KPI, where Books lead with ~70 JOD compared to ~27 JOD in lower categories. This difference is statistically significant (ANOVA p < 0.001, effect size ~ 0.21), confirming that category is a meaningful driver of revenue. See aov_by_category.png and aov_boxplot.png.

Finding 3 is supported by the Revenue by City KPI, where Amman leads with 15,719 JOD. However, the t-test result (p ~ 0.53, very small effect size) shows that average order values are similar across cities, as shown in revenue_by_city.png.

## Recommendations

1. Shift focus toward high-value categories by increasing visibility, promotions, or inventory in segments such as Books and Electronics, where each order contributes more to revenue.

2. Systematically replicate high-performing periods by identifying what drove demand spikes (e.g., campaigns or timing) and turning them into recurring initiatives instead of one-off events.

3. Improve the completeness of customer location data, as the presence of "Unknown" limits the ability to accurately assess geographic performance and make targeted market decisions.
