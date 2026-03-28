# Product Funnel Analysis for an Investment App

This repository contains a portfolio-ready data analytics project focused on **product funnel analysis**.

## Project goal
Analyze how users move through the key stages of an investment app and identify:
- where the biggest drop-off happens
- which traffic sources convert best
- what product hypotheses and actions can improve conversion

## Business question
A product manager wants to understand why many users do not reach the first trade after installing the app and visiting the landing page.

## Funnel stages
1. Landing viewed
2. Signed up
3. KYC completed
4. Deposit made
5. First trade

## Stack
- Python
- pandas
- matplotlib
- SQL

## Repository structure
```bash
funnel_analytics_github_project/
├── data/
│   ├── events.csv
│   └── users.csv
├── outputs/
│   ├── funnel_overall.csv
│   ├── funnel_by_source.csv
│   ├── funnel_by_platform.csv
│   ├── time_to_stage_summary.csv
│   ├── recommendations.md
│   └── images/
│       ├── funnel_overall.png
│       └── deposit_rate_by_source.png
├── src/
│   ├── generate_data.py
│   └── analyze_funnel.py
├── sql/
│   └── funnel_analysis.sql
└── requirements.txt
```

## Dataset
The dataset is **synthetic** and was generated специально для портфолио.  
It imitates real product events for **5000 users** across:
- sources: organic, paid_search, social_ads, referral, email
- platforms: iOS, Android, web
- countries: RU, KZ, BY, UZ

### Main table: `events.csv`
Columns:
- `user_id`
- `event_name`
- `event_time`
- `source`
- `platform`
- `country`
- `value`

## Main results
Based on the generated dataset:
- the largest drop is between **KYC completed** and **Deposit made**
- **referral** and **organic** traffic show the best conversion to deposit
- **social_ads** performs the worst and needs review
- post-KYC activation is a likely weak point of the product flow

## Business recommendations
1. Simplify the KYC flow
2. Add stronger nudges after KYC
3. Revisit acquisition quality for social ads
4. Run an A/B test on onboarding and post-KYC communication

## How to run
```bash
pip install -r requirements.txt
python src/generate_data.py
python src/analyze_funnel.py
```

## Example visuals

### Overall funnel
![Overall funnel](outputs/images/funnel_overall.png)

### Landing → Deposit conversion by source
![Deposit conversion by source](outputs/images/deposit_rate_by_source.png)

## What to say about this project in an interview
- I analyzed a multi-step product funnel for an investment app
- I identified the biggest conversion losses and compared segments by traffic source and platform
- I translated the analysis into product hypotheses and business recommendations
- I used Python for data processing and visualization, and SQL for funnel aggregation logic

## Resume-ready bullet
**Analyzed a product funnel for an investment app using Python and SQL, identified the main drop-off between KYC and deposit, compared conversion by acquisition source, and proposed hypotheses to improve activation and first trade conversion.**
