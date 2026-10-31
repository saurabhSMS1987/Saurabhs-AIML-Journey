# Datasets

The CSV files aren't stored in this repository. To run the notebooks, place these files in this `datasets/` folder:

| File | Rows | Grain | Columns |
| --- | --- | --- | --- |
| `fact_bookings.csv` | 134,590 | One row per booking | `booking_id`, `property_id`, `booking_date`, `check_in_date`, `checkout_date`, `no_guests`, `room_category`, `booking_platform`, `ratings_given`, `booking_status`, `revenue_generated`, `revenue_realized` |
| `fact_aggregated_bookings.csv` | 9,200 | One row per property, room category and day | `property_id`, `check_in_date`, `room_category`, `successful_bookings`, `capacity` |
| `dim_hotels.csv` | 25 | One row per property | `property_id`, `property_name`, `category`, `city` |
| `dim_rooms.csv` | 4 | One row per room category | `room_id`, `room_class` |
| `dim_date.csv` | 92 | One row per day, 1 May to 31 July 2022 | `date`, `mmm yy`, `week no`, `day_type` |
| `new_data_august.csv` | 7 | Extra occupancy rows for 1 August 2022 | Aggregated columns plus hotel, room and date attributes, and `occ%` |

**Source:** the fictional AtliQ Grands dataset from the CodeBasics Python course's hospitality project.

**Quirks to know before using the data:**

- `fact_bookings` mixes two date formats (`19-06-22` and `2/5/2022`). Both are **day first**.
- `fact_aggregated_bookings` writes dates as `1-May-22`, while `dim_date` writes `01-May-22`. Parse both to dates before merging.
- `dim_date` spells weekday as `weekeday`.
- `booking_status` is `Checked Out`, `Cancelled` or `No Show`. Cancelled bookings realize 40% of their value, and no-shows are charged in full.
- `ratings_given` is blank for 58% of bookings.
