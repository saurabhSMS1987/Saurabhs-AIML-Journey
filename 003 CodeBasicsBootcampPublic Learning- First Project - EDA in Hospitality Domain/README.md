# AtliQ Grands: Hospitality Revenue & Occupancy Analysis

*Saurabh S · October 2026 · Python, pandas, Matplotlib, seaborn*

> [!NOTE]
> **Source:** This project is based on the **AtliQ Hotels Data Analysis project** from the **CodeBasics Python course**. AtliQ Grands and its data are fictional, created by CodeBasics for learning. The corrected analysis, extra KPIs, insights and recommendations in this repository are my own work.

## Why I built this

This is my first project in the hospitality domain. I've spent my career in audit and data analytics, where the first rule is simple: **reconcile before you report**. So before drawing any conclusions, I checked whether the numbers in the course notebook tied out.

They didn't. Two date-format issues meant the course's monthly revenue view was missing **31% of revenue**, and its occupancy figures quietly ignored the **1st to the 9th of every month**. Nothing crashed, and every chart looked reasonable. Finding and fixing that, then rebuilding the analysis on complete data, became the heart of this project.

## At a glance

| | |
| --- | --- |
| **Business** | AtliQ Grands: 25 hotels (16 luxury, 9 business) in Mumbai, Bangalore, Hyderabad and Delhi |
| **Period** | 1 May to 31 July 2022 (92 days), plus one day of August data appended |
| **Data** | 134,573 bookings after cleaning, and 9,194 daily occupancy records |
| **Question** | Where is AtliQ making and losing revenue, and where should it focus? |
| **Deliverables** | Corrected and executed notebook, charts, a slide deck and recommendations |

## Headline KPIs

| KPI | Value | What it means |
| --- | --- | --- |
| Revenue realized | **₹170.9 Cr** | What the hotels actually collected |
| Occupancy | **57.9%** | Rooms booked ÷ rooms available |
| RevPAR | **₹7,351** | Revenue per available room |
| ADR | **₹12,696** | Revenue per booking (the course's simplified definition) |
| Realisation | **85.1%** | Share of booked value actually collected |
| Cancellation rate | **24.8%** | One booking in four is cancelled |
| No-show rate | **5.0%** | Charged in full |
| Average rating | **3.62 / 5** | Only 42% of bookings leave a rating |

*1 crore (Cr) = 10 million rupees.*

## Key insights

### 1. Weekends are full; weekdays are half empty

![Weekday vs weekend occupancy](images/01_weekday_weekend.png)

Occupancy is **73.6% at weekends but 51.3% on weekdays**, a 22-point gap. Weekdays hold 71% of all available room-nights, so that's where the empty rooms are. Each 5-point lift in weekday occupancy is worth roughly **8,200 bookings, about ₹10 Cr a quarter**.

### 2. Mumbai earns the most; Delhi fills the best

![Revenue and occupancy by city](images/02_city_revenue_occupancy.png)

| City | Hotels | Revenue | Share | Occupancy | RevPAR | Rating |
| --- | --- | --- | --- | --- | --- | --- |
| Mumbai | 8 | ₹66.9 Cr | 39.1% | 57.9% | ₹8,908 | 3.65 |
| Bangalore | 6 | ₹42.0 Cr | 24.6% | 55.8% | ₹7,334 | 3.41 |
| Hyderabad | 6 | ₹32.5 Cr | 19.0% | 58.1% | ₹5,414 | 3.66 |
| Delhi | 5 | ₹29.4 Cr | 17.2% | **60.5%** | ₹7,364 | **3.78** |

Delhi has the fewest hotels but the **highest occupancy and ratings**, which points to unmet demand. Hyderabad has the weakest RevPAR, and Bangalore the lowest ratings.

### 3. Guest ratings move almost perfectly with occupancy

![Rating vs occupancy by property](images/03_rating_vs_occupancy.png)

Across the 25 properties, average rating and occupancy are almost perfectly correlated (**r = 0.998**). The hotels fall into three clear tiers:

| Tier | Hotels | Average rating | Occupancy |
| --- | --- | --- | --- |
| High | 12 | 4.28 | 66.0% |
| Mid | 9 | 3.05 | 53.4% |
| Low | 4 | 2.34 | 44.6% |

The four low-tier hotels are **Atliq Seasons and Atliq Bay (Mumbai), Atliq Exotica (Hyderabad) and Atliq Grands (Bangalore)**. Correlation doesn't prove that ratings cause occupancy, but lifting these four to mid-tier occupancy would be worth roughly **3,400 bookings, about ₹4.3 Cr a quarter**.

### 4. Cancellations are the biggest revenue leak

![Revenue generated vs realized by booking status](images/04_revenue_leakage.png)

A quarter of bookings are cancelled, and a cancelled booking keeps exactly **40%** of its value. That leaves **₹29.9 Cr (14.9%) of booked value** never realized. No-shows are charged in full.

### 5. Only 15% of bookings come direct

![Booking platform mix](images/05_platform_mix.png)

Third-party platforms bring 85% of bookings, and "others" alone brings 41%. **Cancellation rates (about 25%) and ratings (3.62) are the same on every platform**, so moving bookings to direct channels mainly saves commission. It doesn't change guest behaviour.

### 6. More findings

- **Room classes:** Elite rooms earn the most revenue (32.8%). Presidential suites have the highest occupancy (59.2%).
- **Luxury vs business:** the 16 luxury hotels bring 61.6% of revenue, but business hotels fill slightly better (58.2% vs 57.7%).
- **Months:** revenue is steady: ₹58.2 Cr in May, ₹55.4 Cr in June and ₹57.3 Cr in July.
- **Booking behaviour:** guests book a median of **3 days** before arrival and stay **2.37 nights** on average, so most demand is short-notice.

## Recommendations

| Priority | Action | Estimated impact |
| --- | --- | --- |
| 1 | **Fill weekdays** with corporate rates, weekday packages and events | ≈ ₹10 Cr a quarter per 5-point lift |
| 2 | **Fix the four low-rated hotels**: review guest feedback, service and condition | ≈ ₹4.3 Cr a quarter at mid-tier occupancy |
| 3 | **Reduce cancellations** with prepaid non-refundable rates, pre-arrival reminders and smarter overbooking | Part of the ₹29.9 Cr leak |
| 4 | **Grow direct bookings** with loyalty perks and best-rate guarantees | Commission savings (rates not in the data) |
| 5 | **Invest where demand is proven:** Delhi has the highest occupancy and ratings, with the fewest hotels | Expansion case to explore |
| 6 | **Ask more guests to rate**: only 42% do, yet ratings track occupancy closely | Better early warning |

Impact figures are rough estimates: extra bookings × average realized revenue per booking (₹12,696).

## Data quality: what the course notebook missed

| Check | Course notebook | Corrected |
| --- | --- | --- |
| Revenue in the monthly view | ₹117.6 Cr (**31% missing**) | ₹170.9 Cr |
| Days used for occupancy | 10th–31st of each month (**29% of rows dropped**) | All 92 days |
| Weekday / weekend occupancy | 50.9% / 72.3% | 51.3% / 73.6% |
| Missing capacity filled with | Overall median: 25 | The property's own capacity: 26 and 20 |
| Occupancy method | Average of daily percentages (58.3%) | Rooms booked ÷ rooms available (57.9%) |
| August data appended | 15 columns, `occ%` not matched to `occ_pct` | 13 aligned columns |

**Root causes:**

1. **Dates that never matched.** The aggregated file writes `1-May-22`, but the date table writes `01-May-22`. Merging these as text dropped every day from the 1st to the 9th.
2. **Day-first dates read as month-first.** `1/5/2022` means 1 May, but `pd.to_datetime()` read it as 5 January, so those bookings fell outside the date table.

**Other cleaning:** I removed 12 bookings with zero, negative or missing guests, 5 extreme revenue outliers (up to ₹2.86 Cr for a single booking) and 6 days where bookings exceeded capacity, such as 123 bookings for 26 rooms. Missing ratings were left blank rather than filled, because most guests simply don't rate.

## Repository structure

```text
atliq-hotels-analysis/
├── README.md                                   <- you are here
├── requirements.txt                            <- Python packages
├── .gitignore                                  <- keeps the CSV files out of Git
├── datasets/
│   └── README.md                               <- data dictionary; place the CSV files here
├── notebooks/
│   ├── atliq_hotels_analysis_corrected.ipynb   <- my corrected and extended analysis (executed)
│   └── course_exercise_solution.ipynb          <- the original course notebook, for reference
├── images/                                     <- charts used in this README
└── presentation/
    ├── AtliQ_Hotels_Insights.pptx              <- 11-slide deck with speaker notes
    └── AtliQ_Hotels_Insights.pdf               <- the same deck, viewable on GitHub
```

The corrected notebook is saved **with its outputs**, so every table and chart can be read on GitHub without the data.

## How to run it

```bash
git clone <this-repository-url>
cd atliq-hotels-analysis
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# copy the six CSV files into datasets/ (see datasets/README.md)
jupyter lab notebooks/atliq_hotels_analysis_corrected.ipynb
```

## Skills demonstrated

- **Data cleaning:** invalid values, statistical outliers, missing values and impossible records.
- **Data validation:** reconciling totals and catching silent row loss in merges, using `validate=` in `pd.merge`.
- **Date handling:** parsing mixed formats explicitly, with `format="mixed", dayfirst=True` and `format="%d-%b-%y"`.
- **Analysis:** `groupby`, `merge` and `concat`, plus hospitality KPIs (occupancy, RevPAR, ADR, realisation and DSRN).
- **Visualisation:** Matplotlib and seaborn charts, and a native-chart PowerPoint deck.
- **Communication:** turning numbers into sized, prioritised recommendations.

## What I learned

- **Reconcile before you report.** A tidy chart can hide a third of the data. Agreeing the total revenue before slicing it is now the first step in my workflow.
- **Dates are the most common silent failure.** Two formats and one month-first guess dropped thousands of rows without any warning.
- **Weight your averages.** Averaging daily percentages gives small and large rooms equal say. Dividing totals gives the true occupancy.
- **Audit habits transfer.** Profiling data, checking completeness and documenting every cleaning decision worked just as well on hotel bookings as on a general ledger.

## Credits

- Project concept, notebook structure and fictional dataset: **CodeBasics Python course**, AtliQ Hotels Data Analysis project.
- Corrections, extended analysis, charts, deck and recommendations: Saurabh S.
