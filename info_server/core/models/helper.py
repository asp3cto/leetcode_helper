from core.database import problems_collection
import csv


def csv_to_mongo(filename):
    with open(filename, "r") as csvFile:
        reader = csv.DictReader(csvFile)
        for each in reader:
            row = {}
            for field in reader.fieldnames:
                if each[field] != '':
                    row[field] = each[field]
            problems_collection.insert_one(row)
