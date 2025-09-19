# Music Store Data Analysis Report

**Generated on:** September 19, 2025  
**Analysis Period:** January 3, 2017 to December 30, 2020  
**Analyst:** Junior Data Analyst  

---

## Executive Summary

This report presents a comprehensive analysis of the online music store's sales data, covering 4 years of business operations. The analysis examines customer demographics, spending patterns, product performance, and revenue trends to provide actionable insights for marketing and product decisions.

### Key Business Metrics
- **Total Customers:** 59
- **Total Orders:** 614  
- **Total Revenue:** $4,709.43
- **Average Order Value:** $7.67
- **Analysis Period:** 4 years (2017-2020)

---

## Business Questions & Answers

### 1. Which country has the most customers?

**Answer: USA** 🇺🇸

- **USA:** 13 customers (22% of total)
- **Canada:** 8 customers (14% of total)  
- **France:** 5 customers (8% of total)
- **Brazil:** 5 customers (8% of total)

**Business Insight:** The USA represents our largest customer base, followed by Canada. Together, North American customers account for 36% of our customer base.

### 2. Which customer has spent the most money?

**Answer: František Wichterlová from Czech Republic - $144.54**

**Top 5 Highest Spending Customers:**
1. František Wichterlová (Czech Republic): $144.54
2. Helena Holý (Czech Republic): $128.70  
3. Hugh O'Reilly (Ireland): $114.84
4. Manoj Pareek (India): $111.87
5. Luís Gonçalves (Brazil): $108.90

**Business Insight:** Our highest-value customers are geographically diverse, with Czech Republic customers leading in total spending despite the USA having more customers overall.

### 3. How much revenue was generated from each music genre?

**Answer: Rock music generated the most revenue - $2,608.65**

**Top 5 Revenue-Generating Genres:**
1. **Rock:** $2,608.65 (55% of total revenue)
2. **Metal:** $612.81 (13% of total revenue)
3. **Alternative & Punk:** $487.08 (10% of total revenue)
4. **Latin:** $165.33 (4% of total revenue)
5. **R&B/Soul:** $157.41 (3% of total revenue)

**Business Insight:** Rock music dominates our sales, generating more than half of total revenue. The top 3 genres (Rock, Metal, Alternative & Punk) account for 78% of total revenue.

### 4. What is the average transaction value per customer?

**Answer: $7.67 overall average transaction value**

**Key Statistics:**
- **Overall Average Transaction Value:** $7.67
- **Median Customer Average:** $7.92
- **Highest Individual Customer Average:** François Tremblay (Canada) - $11.11

**Business Insight:** Transaction values are relatively consistent across customers, with most customers having average transaction values between $7-$10.

### 5. What is the total revenue for each year?

**Answer: 2019 had the highest revenue - $1,221.66**

**Yearly Revenue Breakdown:**
- **2017:** $1,201.86 (baseline year)
- **2018:** $1,147.41 (-4.5% vs 2017)
- **2019:** $1,221.66 (+6.5% vs 2018) 🏆
- **2020:** $1,138.50 (-6.8% vs 2019)

**Business Insight:** Revenue peaked in 2019 but declined in 2020. The business shows volatility with alternating years of growth and decline.

---

## Strategic Recommendations

### 1. Geographic Expansion & Marketing
- **Focus on North America:** USA and Canada represent 36% of customers - invest in targeted marketing campaigns
- **European Opportunity:** Czech Republic customers show highest spending - explore similar European markets
- **Emerging Markets:** Consider expansion in India and Brazil based on high-value customer presence

### 2. Product & Inventory Strategy
- **Rock Music Priority:** Maintain strong rock music inventory (55% of revenue)
- **Genre Diversification:** Expand metal and alternative punk offerings (combined 23% of revenue)
- **Niche Genres:** Consider reducing inventory in low-performing genres (TV Shows, Drama, Heavy Metal)

### 3. Customer Retention & Growth
- **VIP Program:** Create loyalty program for customers spending >$100 (top 10 customers)
- **Average Order Value:** Implement bundling strategies to increase the $7.67 average transaction
- **Geographic Targeting:** Focus acquisition efforts in countries with proven high-value customers

### 4. Revenue Optimization
- **Seasonal Analysis:** Investigate 2019 success factors to replicate growth
- **2020 Recovery:** Analyze 2020 decline causes (possibly COVID-19 impact) and develop recovery strategies
- **Pricing Strategy:** Consider premium pricing for rock music given its dominance

---

## Data Quality Notes

During analysis, the following data quality issues were identified:
- **Missing Values:** 130 missing values in customer data, 359 in invoice data
- **No Duplicates:** Data integrity is good with no duplicate records found
- **Date Range:** Complete 4-year dataset from 2017-2020
- **Price Range:** Transaction values range from $0.99 to $23.76

---

## Conclusion

The music store shows a solid foundation with consistent customer spending patterns and strong performance in rock music genres. The business would benefit from focusing on its core strengths (rock music, North American market) while exploring opportunities in high-value international markets. The revenue volatility suggests need for more consistent growth strategies and deeper analysis of external factors affecting performance.

**Next Steps:**
1. Implement recommended marketing strategies for top-performing regions
2. Optimize inventory based on genre performance analysis  
3. Develop customer retention programs for high-value customers
4. Conduct deeper analysis of 2020 revenue decline factors
5. Set up regular monitoring of key metrics identified in this analysis

---

*This analysis was completed using Python pandas for data processing and analysis. All calculations and insights are based on the complete dataset of 614 invoices and 4,757 line items across 59 customers.*
