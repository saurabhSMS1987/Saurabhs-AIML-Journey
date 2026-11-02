"""
Creates every sample file used in 'reading-files-with-pandas-guide.md'.

All data is made up for practice. Run once:
    python make_sample_files.py
Files are written to a 'sample_data' folder next to this script.
"""
import gzip
import json
import sqlite3
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).parent / "sample_data"
OUT.mkdir(exist_ok=True)


def write(name, text, encoding="utf-8"):
    (OUT / name).write_text(text, encoding=encoding, newline="")


# 1. Semicolon-delimited bank statement, European number format
write("bank_statement_eu.csv",
      "Datum;Beschreibung;Betrag;Saldo\n"
      "01.09.2026;Gehalt;3.250,00;5.410,75\n"
      "03.09.2026;Miete;-1.200,00;4.210,75\n"
      "15.09.2026;Stromrechnung;-86,40;4.124,35\n")

# 2. Pipe-delimited claims extract (IDs with leading zeros)
write("claims_extract.txt",
      "CLAIM_ID|POLICY_NO|PATIENT_ID|SERVICE_DATE|AMOUNT|STATUS\n"
      "C-1001|000123|P-778|2026-08-01|1450.00|PAID\n"
      "C-1002|004567|P-312|2026-08-02|22800.50|PAID\n"
      "C-1003|000123|P-778|2026-08-01|1450.00|PENDING\n")

# 3. Tab-delimited lab results
write("lab_results.tsv",
      "patient_id\ttest\tresult\tunit\n"
      "P-778\tHbA1c\t6.9\t%\n"
      "P-312\tLDL\t3.4\tmmol/L\n"
      "P-455\tTSH\t2.1\tmIU/L\n")

# 4. Space-aligned meter report (variable spaces)
write("meter_report_aligned.txt",
      "METER_ID   REGION     KWH\n"
      "M001       North      420\n"
      "M002       North     3150\n"
      "M003       South    18200\n")

# 5. Unknown delimiter (it is ';' but we pretend not to know)
write("vendor_list.csv",
      "vendor_id;vendor_name;bank_account\n"
      "V01;Delta Traders;GB29NWBK60161331926819\n"
      "V02;Nova Logistics;GB94BARC10201530093459\n")

# 6. Multi-character delimiter from a legacy policy system
write("policies_legacy.txt",
      "POLICY~|~HOLDER~|~PREMIUM\n"
      "P101~|~Anita Rao~|~1200.50\n"
      "P102~|~Rahul Mehta~|~860.00\n")

# 7. Two delimiters mixed in one file (merged from two systems)
write("readings_mixed.txt",
      "meter_id,reading_date,kwh\n"
      "M001,2026-09-30,420\n"
      "M002;2026-09-30;3150\n"
      "M003,2026-09-30;2875\n")

# 8. Delimiter inside a quoted value
write("providers.csv",
      'provider_id,name,address\n'
      'PR01,City Hospital,"12, Main Street, Springfield"\n'
      'PR02,Lakeside Clinic,"4 Lake Road, Unit 2, Riverton"\n')

# 9. Report with title lines, a comment line and a trailer
write("claims_paid_report.csv",
      "ACME Health Insurance\n"
      "Claims Paid Report\n"
      "Run date: 30/10/2026\n"
      "\n"
      "claim_id,amount\n"
      "C1,1200.00\n"
      "# manual adjustment removed by ops\n"
      "C2,850.50\n"
      "C3,4300.00\n"
      "TOTAL,6350.50\n"
      "Record count: 3\n")

# 10. Legitimate line breaks inside quoted fields
write("adjuster_notes.csv",
      'claim_id,notes,amount\n'
      'C1,"Water damage in kitchen.\nInsured called twice for update.",5000\n'
      'C2,"Theft of laptop",1200\n')

# 11. Broken lines: a free-text field contains an unquoted line break
write("complaints_broken.txt",
      "complaint_id|customer|description|amount\n"
      "CP1|Anita|Bill too high|120.50\n"
      "CP2|Rahul|Meter reading wrong\n"
      "customer says an estimate was used|88.00\n"
      "CP3|Maria|Late payment fee|15.00\n")

# 12. Rows with too many fields (unquoted comma in an address)
write("patients_bad_rows.csv",
      "patient_id,name,city\n"
      "P1,Anita Rao,Pune\n"
      "P2,Rahul Mehta,Mumbai, Andheri East\n"
      "P3,Maria Gomez,Delhi\n")

# 13. Trailing delimiter on every line
write("trailing_delim.csv",
      "meter_id,kwh\n"
      "M001,420,\n"
      "M002,3150,\n")

# 14. Messy values: missing-value markers, currency text, accounting negatives
write("premium_register.csv",
      "policy_no,holder,premium,adjustment,paid_flag\n"
      "000123,Anita Rao,\"$1,200.00\",(150.00),Y\n"
      "004567,Rahul Mehta,\"$860.00\",N/A,N\n"
      "007788,Maria Gomez,-,NULL,Y\n")

# 15. Day-first dates, with one impossible date
write("admissions.csv",
      "admission_id,admit_date,discharge_date\n"
      "A1,05/09/2026,08/09/2026\n"
      "A2,28/09/2026,30/09/2026\n"
      "A3,30/09/2026,31/02/2026\n")

# 16. Encodings: Windows-1252 file, and a UTF-8 file with a BOM
write("suppliers_cp1252.csv",
      "supplier,city\nCafé Müller,München\nSociété Générale,Paris\n",
      encoding="cp1252")
write("export_with_bom.csv", "id,amount\n1,100\n2,250\n", encoding="utf-8-sig")

# 17. Fixed-width mainframe policy file (premium has 2 implied decimals)
write("policies_fixed_width.txt",
      "P0001234ANITA RAO           20260115000120050\n"
      "P0005678RAHUL MEHTA         20260201000086000\n"
      "P0009012MARIA GOMEZ         20260310001500075\n")

# 18. Excel workbook: title rows above the header, one sheet per quarter
with pd.ExcelWriter(OUT / "premiums_2026.xlsx") as xw:
    for sheet, rows in {"Q1": [["P101", 1200.5], ["P102", 860.0]],
                        "Q2": [["P101", 1250.0], ["P103", 1500.75]]}.items():
        title = pd.DataFrame([[f"Premium register {sheet} 2026", None], [None, None]])
        title.to_excel(xw, sheet_name=sheet, index=False, header=False)
        pd.DataFrame(rows, columns=["policy", "premium"]).to_excel(
            xw, sheet_name=sheet, index=False, startrow=2)

# 19. Nested JSON from a smart-meter API, plus JSON Lines events
meters = [
    {"meter_id": "M001", "customer": {"id": "C101", "region": "North"},
     "readings": [{"date": "2026-09-29", "kwh": 14.2}, {"date": "2026-09-30", "kwh": 13.8}]},
    {"meter_id": "M002", "customer": {"id": "C102", "region": "South"},
     "readings": [{"date": "2026-09-29", "kwh": 0.0}, {"date": "2026-09-30", "kwh": 0.0}]},
]
write("smart_meters.json", json.dumps(meters, indent=2))
write("outage_events.jsonl",
      '{"event_id": 1, "region": "North", "minutes": 45}\n'
      '{"event_id": 2, "region": "South", "minutes": 210}\n'
      '{"event_id": 3, "region": "North", "minutes": 12}\n')

# 20. XML claims file
write("claims.xml",
      '<?xml version="1.0"?>\n<claims>\n'
      '  <claim id="C1"><patient>P-778</patient><amount>1450.00</amount></claim>\n'
      '  <claim id="C2"><patient>P-312</patient><amount>22800.50</amount></claim>\n'
      '</claims>\n')

# 21. Parquet file
pd.DataFrame({"claim_id": ["C1", "C2", "C3"], "line": ["motor", "property", "health"],
              "paid": [42000.0, 260000.0, 18500.0], "notes": ["", "", ""]}
             ).to_parquet(OUT / "claims.parquet", index=False)

# 22. SQLite database
with sqlite3.connect(OUT / "billing.db") as con:
    pd.DataFrame({"invoice_id": ["I1", "I2", "I3"], "region": ["North", "South", "North"],
                  "amount": [58.80, 2184.00, 441.00]}
                 ).to_sql("invoices", con, if_exists="replace", index=False)

# 23. HTML page with a tariff table
write("tariffs.html",
      "<html><body><h1>Tariffs</h1><table>"
      "<tr><th>Tariff</th><th>Rate per kWh</th></tr>"
      "<tr><td>Residential</td><td>0.14</td></tr>"
      "<tr><td>Commercial</td><td>0.14</td></tr>"
      "<tr><td>Industrial</td><td>0.12</td></tr>"
      "</table></body></html>")

# 24. Compressed copies of the claims extract
src = (OUT / "claims_extract.txt").read_bytes()
with gzip.open(OUT / "claims_extract.txt.gz", "wb") as g:
    g.write(src)
with zipfile.ZipFile(OUT / "claims_extract.zip", "w") as z:
    z.writestr("claims_extract.txt", src)

# 25. One file per month
(OUT / "monthly").mkdir(exist_ok=True)
for month, kwh in {"2026_07": [400, 3020], "2026_08": [410, 3100], "2026_09": [420, 3150]}.items():
    write(f"monthly/meter_{month}.csv", "meter_id,kwh\n" + "".join(
        f"M00{i + 1},{k}\n" for i, k in enumerate(kwh)))

# 26. A larger file for chunked reading (100,000 claims)
rng = np.random.default_rng(7)
pd.DataFrame({
    "claim_id": [f"C{i:06d}" for i in range(100_000)],
    "status": rng.choice(["PAID", "PENDING", "DENIED"], 100_000, p=[0.7, 0.2, 0.1]),
    "amount": rng.gamma(2.0, 1500.0, 100_000).round(2),
    "free_text": ["n/a"] * 100_000,
}).to_csv(OUT / "big_claims.csv", index=False)

print(f"Sample files written to {OUT}")
