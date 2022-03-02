import csv

COMPANY_LOOKUP = {}

"""
for row in company_identifiers.csv,
row[0] = company_id (decimal)
row[1] = company_id (hex)
row[2] = company name
"""

with open("companyidentifiers.csv", mode='r', encoding="UTF-8") as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        COMPANY_LOOKUP[row[0]] = row[2]
