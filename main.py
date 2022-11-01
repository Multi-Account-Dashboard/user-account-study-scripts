import csv
import json
import parser
import models


def writeJSON(file, data):
    with open(file, "w") as outfile:
        json.dump(data, outfile, indent=4)


def processRow(row):
    id = parser.parse_index(row)
    services = parser.parse_services(row)
    for i in range(len(services)):
        if services[i] == 0:
            account_setup = parser.parse_Google_account(row)
            d = models.model_from_file("models/google.json", account_setup["secondary_methods_indices"],account_setup["fallback_methods_indices"])
            writeJSON("results/" + id + "-google.json", d)
        elif services[i] == 1:
            account_setup= parser.parse_Apple_account(row)
            d= models.model_from_file("models/apple.json", account_setup["secondary_methods_indices"],account_setup["fallback_methods_indices"])
            writeJSON("results/" + id + "-apple.json", d)
        elif services[i] == 2:
            account_setup= parser.parse_Amazon_account(row)
            d= models.model_from_file("models/amazon.json", account_setup["secondary_methods_indices"],account_setup["fallback_methods_indices"])
            writeJSON("results/" + id + "-amazon.json", d)
        elif services[i] == 3:
            account_setup= parser.parse_Facebook_account(row)
            d= models.model_from_file("models/facebook.json", account_setup["secondary_methods_indices"],account_setup["fallback_methods_indices"])
            writeJSON("results/" + id + "-facebook.json", d)
        elif services[i] == 4:
            account_setup= parser.parse_LinkedIn_account(row)
            d= models.model_from_file("models/linkedin.json", account_setup["secondary_methods_indices"],account_setup["fallback_methods_indices"])
            writeJSON("results/" + id + "-linkedin.json", d)
        elif services[i] == 5:
            account_setup= parser.parse_Twitter_account(row)
            d= models.model_from_file("models/twitter.json", account_setup["secondary_methods_indices"],account_setup["fallback_methods_indices"])
            writeJSON("results/" + id + "-twitter.json", d)

with open('data/alpha-pilot.csv') as csv_file:
    csv_reader= csv.reader(csv_file, delimiter=',')
    line_count= 0
    for row in csv_reader:
        if line_count == 0:
            # print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            processRow(row)
            line_count += 1
