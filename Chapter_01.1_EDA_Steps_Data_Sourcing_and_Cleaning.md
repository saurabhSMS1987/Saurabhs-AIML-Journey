# Chapter 1.1 — Steps in EDA: Data Sourcing & Data Cleaning

> **Course:** Data Science & AI Masters 2026 — From Python to Gen AI
> **Module:** Exploratory Data Analysis
> **Topics:** Step 1 — Data Sourcing · Step 2 — Data Cleaning

---

## Table of Contents

1. [Where These Steps Fit](#1-where-these-steps-fit)
2. [Step 1 — Data Sourcing](#2-step-1--data-sourcing)
3. [Step 2 — Data Cleaning](#3-step-2--data-cleaning)
4. [Key Takeaways](#4-key-takeaways)

---

## 1. Where These Steps Fit

```mermaid
flowchart LR
    A["Data Sourcing<br/>get the data"] --> B["Data Cleaning<br/>unclean → clean"]
    B --> C["EDA"]
    C --> D["ML Model Building"]
    B -. "sometimes skip EDA" .-> D
```

Data sourcing gets the data; data cleaning makes it usable. Whether you go to EDA first or straight to model building, **cleaning is always a prerequisite**.

---

## 2. Step 1 — Data Sourcing

**Data sourcing** is the process of gathering data from multiple sources, through **internal or external** data collection.

### Two kinds of data (by source)

```mermaid
flowchart TD
    D["Data Sources"] --> P["Public Data"]
    D --> R["Private Data"]
    P --> P1["No permission needed<br/>Made public for research"]
    P1 --> P2["Government sites · Public sector sites · E-commerce sites"]
    P2 --> P3["Get it by: download / extract / web scraping"]
    R --> R1["Not on public platforms<br/>Needs the organization's permission"]
    R1 --> R2["e.g., telecom or banking company data"]
    R2 --> R3["Request access from your DBA team<br/>(Database Administration)"]
    R3 --> R4["Get it by: download / create a connector"]
```

| | **Public Data** | **Private Data** |
|---|---|---|
| **Access** | Open — no permission required | Restricted — organization's permission required |
| **Why available** | Agencies publish it for research | Internal business data |
| **Examples** | Government, public sector, e-commerce websites | Telecom or banking company databases |
| **How to get it** | Download, extract, or web scrape | Get access from the DBA team, then download or build a connector |

> Choose your data source wisely based on the **use case** you are solving.

### Sourcing by company type

The data source depends heavily on the kind of company you work for.

```mermaid
flowchart TD
    Start{"What type of company?"}
    Start -->|"MNC"| M["Multiple databases<br/>Contact each relevant DBA for access"]
    Start -->|"Mid-level company"| ML["Fewer/smaller databases<br/>Same process: request access"]
    Start -->|"Small company / Startup"| S{"Does the startup<br/>have a database?"}
    S -->|"Yes (mid-level startup)"| SD["Get database access"]
    S -->|"No (completely new)"| C{"Does it have a client?"}
    C -->|"Yes"| CL["Take data from the client"]
    C -->|"No"| PU["Use public data<br/>Web scraping · Government / open public sector sites"]
    M --> E["Start EDA → Model Building"]
    ML --> E
    SD --> E
    CL --> E
    PU --> E
```

| Company type | Typical data source |
|---|---|
| **MNC** (multinational) | Many internal databases — talk to each database administrator for access |
| **Mid-level company** | Some internal databases — same access process |
| **Mid-level startup** | Its own database, if it has one |
| **New startup with a client** | Data provided by the client |
| **New startup with no client** | Public data via web scraping or government / open public-sector sites |

---

## 3. Step 2 — Data Cleaning

**Data cleaning** removes information that doesn't need to be there, improving **data quality** for further analysis and for building machine learning models.

### Why it matters

All **incorrect and irrelevant data is removed**, leaving good-quality data that **improves the accuracy of predictive / ML models**.

### Major steps in data cleaning

```mermaid
flowchart LR
    U["Unclean Data"] --> M["1. Handle<br/>Missing Values"]
    M --> F["2. Feature Scaling<br/>(Standardization)"]
    F --> O["3. Outlier<br/>Treatment"]
    O --> I["4. Handle Invalid<br/>Values / Data Types"]
    I --> C["Clean Data"]
```

> The order shown follows the lesson; each step will be covered in detail in later lessons.

#### 1. Missing values

```mermaid
flowchart TD
    MV["Missing Values"] --> W{"Why missing?"}
    W --> W1["Missing in the database / source itself"]
    W --> W2["Introduced by the script that pulled the data"]
    MV --> H{"How to handle?"}
    H --> H1["Delete the records"]
    H --> H2["Impute the values"]
```

Missing values must be dealt with before further analysis — either **delete** the affected records or **impute** them.

#### 2. Feature scaling

Also referred to as **standardization of the data**. Feature scaling has two techniques:
- **Standardization**
- **Normalization**

#### 3. Outlier treatment

**Outliers** are data points that lie far above or far below the range where most of the data sits. Most real datasets contain them. Treatment means either **removing them** or **dealing with them**.

#### 4. Invalid values / data types

Common examples:
- **Impossible values** — e.g., an age of -180.
- **Special characters** in columns where they don't belong.
- **Wrong data types** — e.g., a date column not stored in date format.

### Data cleaning at a glance

```mermaid
mindmap
  root(("Data Cleaning"))
    Missing Values
      Source gaps
      Script errors
      Delete or impute
    Feature Scaling
      Standardization
      Normalization
    Outliers
      Far above or below most data
      Remove or treat
    Invalid Values
      Impossible values
      Special characters
      Wrong data types e.g. dates
```

---

## 4. Key Takeaways

- **Data sourcing** = gathering data from internal or external sources; data is either **public** (open, for research) or **private** (needs organizational permission via the DBA team).
- **Your data source depends on the company type and the use case** — MNCs and mid-level firms use internal databases; new startups rely on clients or public data.
- **Data cleaning** turns unclean data into clean data and is a **prerequisite for both EDA and model building**.
- **Four major cleaning steps:** handle missing values (delete/impute) · feature scaling (standardization/normalization) · outlier treatment · invalid values and data types.
- **Clean data → better model accuracy.**

---

*Part of my Data Science & AI learning log.*
