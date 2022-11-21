import csv
import json
import parser
import models


def writeJSON(file, data):
    with open(file, "w") as outfile:
        json.dump(data, outfile, indent=4)


def devices_to_list(devices):
    l = ["Memory", "Paper"]
    # for i in range(devices["phone_numbers"]):
    num_mobile = 0
    num_computer = 0
    num_security_key = 0

    for v in devices:
        if v["type"] == "mobile_device":
            l.append("Mobile {0}".format(num_mobile))
            num_mobile += 1
        elif v["type"] == "computer_device":
            l.append("Computer {0}".format(num_computer))
            num_computer += 1
        elif v["type"] == "sec_key_device":
            l.append("SecKey {0}".format(num_security_key))
            num_security_key += 1
    return l


def processRow(row):
    id = parser.parse_index(row)
    devices = parser.parse_devices(row)
    devicesList = devices_to_list(devices)
    services = parser.parse_services(row)
    print("\nParticipant", id, devices, services)

    for i in range(len(services)):
        if services[i] == "google":
            account_setup = parser.parse_Google_account(row)
            print(id, "Google", account_setup["password_access"])
            d = models.model_from_file(
                "models/google.json", account_setup["password_access"], account_setup["secondary_methods"], account_setup["fallback_methods"], devicesList)
            writeJSON("results/" + id + "-google.json", d)

        elif services[i] == "apple":
            account_setup = parser.parse_Apple_account(row)
            print(id, "Apple", account_setup["password_access"])
            d = models.model_from_file(
                "models/apple.json", account_setup["password_access"], account_setup["secondary_methods"], account_setup["fallback_methods"], devicesList)
            writeJSON("results/" + id + "-apple.json", d)
        """
        elif services[i] == 2:
            account_setup = parser.parse_Amazon_account(row)
            d = models.model_from_file(
                "models/amazon.json", account_setup["secondary_methods"], account_setup["fallback_methods"], devicesList)
            writeJSON("results/" + id + "-amazon.json", d)
        elif services[i] == 3:
            account_setup = parser.parse_Facebook_account(row)
            d = models.model_from_file(
                "models/facebook.json", account_setup["secondary_methods"], account_setup["fallback_methods"], devicesList)
            writeJSON("results/" + id + "-facebook.json", d)
        elif services[i] == 4:
            account_setup = parser.parse_LinkedIn_account(row)
            d = models.model_from_file(
                "models/linkedin.json", account_setup["secondary_methods"], account_setup["fallback_methods"], devicesList)
            writeJSON("results/" + id + "-linkedin.json", d)
        """


with open('data/study-refactored-alpha.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            processRow(row)
            line_count += 1
