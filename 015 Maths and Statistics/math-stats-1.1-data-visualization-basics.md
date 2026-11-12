# Takeaways: Math & Statistics: Data and Visualisation Basics

*Nov 11, 2026 · Saurabh S*

> [!NOTE]
> **Source:** *Key Takeaways: Data & Visualization Basics* from the **[Codebasics.io](https://codebasics.io) Math & Statistics course**. It covers five lectures: types of data, pie and bar charts, histograms and line charts, scatter and bubble plots, and univariate vs bivariate vs multivariate analysis.

My one-page recap of the chapter, with a journal entry example for each idea.

## 1. Types of data

| Type | Meaning | Journal entry example |
| --- | --- | --- |
| **Structured** | Organised in a clear format, and easy to work with (tables, JSON, XML) | The GL extract |
| **Unstructured** | No fixed structure; needs specialised tools (audio, video, free-form text) | Scanned invoices, email approvals |
| **Categorical: nominal** | Labels with **no order** | Entity, source system, preparer |
| **Categorical: ordinal** | Labels **with an order** | Risk rating (Low < Medium < High) |
| **Numeric: continuous** | Any value in a range, often with decimals | Amount |
| **Numeric: discrete** | Distinct, countable values | Number of lines per entry |

> JSON and XML are often described as **semi-structured**: they follow a format, but not a fixed table layout.

## 2. Choosing a chart

| Chart | Use it when | Journal entry example |
| --- | --- | --- |
| **Bar chart** | Comparing against benchmark values | Manual entry value by entity vs materiality |
| **Horizontal bar** | Labels are long, **or** there are more than 5 categories (instead of a pie) | Top 10 accounts by manual value |
| **Pie chart** | Showing parts of a whole, with **5 or fewer** categories | Manual vs automated share |
| **Vertical bar** | Showing time series data | Entries posted per month |
| **Clustered column** | Comparing several series within each category | Manual vs automated, per month |
| **Stacked column** | Showing the parts of each total, plus the total itself | Monthly entries split by source |
| **Histogram** | Showing the frequency distribution, using **equal-sized bins** | The distribution of entry amounts |
| **Line chart** | Showing a trend or change over time | Daily posting volume around month-end |
| **Scatter plot** | Showing the relationship between **two** variables, and spotting outliers | Amount vs approval delay |
| **Bubble chart** | A scatter plot where bubble **size** adds a third variable | Entity revenue vs margin, sized by volume |

## 3. Univariate, bivariate and multivariate analysis

| Analysis | Variables | Typical charts | Example question |
| --- | --- | --- | --- |
| **Univariate** | One | Histogram, bar chart | How are entry amounts distributed? |
| **Bivariate** | Two | Scatter plot, clustered column | Do larger entries take longer to approve? |
| **Multivariate** | More than two | Bubble chart, heatmap | How do amount, approval delay and preparer interact? |

**The thread through the chapter:** the **type of data** decides which **chart** fits, and the number of variables decides how deep the **analysis** goes.
