from core.database import collection
import csv


def csv_to_mongo(filename):
    with open(filename, "r") as csvFile:
        reader = csv.DictReader(csvFile)
        for each in reader:
            row = {}
            for field in reader.fieldnames:
                row[field] = each[field]
            collection.insert_one(row)
