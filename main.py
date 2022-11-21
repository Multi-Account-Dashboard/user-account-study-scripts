import csv
import json
import parser
import models


def writeJSON(file, data):
    with open(file, "w") as outfile:
        json.dump(data, outfile, indent=4)


def devices_to_list(devices):
    l = []
    # for i in range(devices["phone_numbers"]):
    for i in range(devices["mobile_devices"]):
        l.append("Mobile {0}".format(i+1))
    for i in range(devices["computers"]):
        l.append("Computer {0}".format(i+1))
    for i in range(devices["security_keys"]):
        l.append("SecKey {0}".format(i+1))
    for i in range(devices["password_managers"]):
        l.append("PWM {0}".format(i+1))
    for i in range(devices["authenticator_apps"]):
        l.append("AuthApp {0}".format(i+1))
    return l


def processRow(row):
    id = parser.parse_index(row)
    devices = parser.parse_devices(row)
    devicesList = devices_to_list(devices)
    services = parser.parse_services(row)
    print(id, devices)
    for i in range(len(services)):
        if services[i] == 0:
            account_setup = parser.parse_Google_account(row)
            d = models.model_from_file(
                "models/google.json", account_setup["secondary_methods_indices"], account_setup["fallback_methods_indices"], devicesList)
            writeJSON("results/" + id + "-google.json", d)
        elif services[i] == 1:
            account_setup = parser.parse_Apple_account(row)
            d = models.model_from_file(
                "models/apple.json", account_setup["secondary_methods_indices"], account_setup["fallback_methods_indices"], devicesList)
            writeJSON("results/" + id + "-apple.json", d)
        elif services[i] == 2:
            account_setup = parser.parse_Amazon_account(row)
            d = models.model_from_file(
                "models/amazon.json", account_setup["secondary_methods_indices"], account_setup["fallback_methods_indices"], devicesList)
            writeJSON("results/" + id + "-amazon.json", d)
        elif services[i] == 3:
            account_setup = parser.parse_Facebook_account(row)
            d = models.model_from_file(
                "models/facebook.json", account_setup["secondary_methods_indices"], account_setup["fallback_methods_indices"], devicesList)
            writeJSON("results/" + id + "-facebook.json", d)
        elif services[i] == 4:
            account_setup = parser.parse_LinkedIn_account(row)
            d = models.model_from_file(
                "models/linkedin.json", account_setup["secondary_methods_indices"], account_setup["fallback_methods_indices"], devicesList)
            writeJSON("results/" + id + "-linkedin.json", d)
        # elif services[i] == 5:
        #    account_setup = parser.parse_Twitter_account(row)
        #    d = models.model_from_file(
        #        "models/twitter.json", account_setup["secondary_methods_indices"], account_setup["fallback_methods_indices"],devicesList)
        #    writeJSON("results/" + id + "-twitter.json", d)


with open('data/alpha-pilot.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            processRow(row)
            line_count += 1
