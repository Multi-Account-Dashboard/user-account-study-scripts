import csv
import json
import result_parser
import models
import sys


def writeJSON(file, data):
    with open(file, "w") as outfile:
        json.dump(data, outfile, indent=2)


def devices_to_list(devices):
    l = []
    num_mobile = 0
    num_computer = 0
    num_tablet = 0
    num_security_key = 0

    for v in devices:
        label = ""
        if v["type"] == "phone":
            label = "Phone {0}".format(num_mobile+1)
            num_mobile += 1
        elif v["type"] == "computer":
            label = "Computer {0}".format(num_computer+1)
            num_computer += 1
        elif v["type"] == "tablet":
            label = "Tablet {0}".format(num_tablet+1)
            num_tablet += 1
        elif v["type"] == "security_key":
            label = "SecKey {0}".format(num_security_key+1)
            num_security_key += 1
        l.append({"id": v["id"], "label": label})
    return l


def processRow(row):
    id = result_parser.parse_index(row)
    services = result_parser.parse_services(row)

    graph_google = None
    graph_apple = None

    for i in range(len(services)):
        if services[i] == "google":
            account_setup = result_parser.parse_Google_account(row)
            graph_google = models.graph_from_file(
                "models/graph-google.json", account_setup["auth_nodes"], account_setup["devices"])
            writeJSON("results/" + id + "-google.json", graph_google)
            graph_google["id"] = id
        elif services[i] == "apple":
            account_setup = result_parser.parse_Apple_account(row)
            account_setup["id"] = id
            graph_apple = models.graph_from_file(
                "models/graph-apple.json", account_setup["auth_nodes"], account_setup["devices"])
            writeJSON("results/" + id + "-apple.json", graph_apple)
            graph_apple["id"] = id
    return {"google": graph_google, "apple": graph_apple}

with open(sys.argv[1]) as csv_file:
    graphs_google = []
    graphs_apple = []

    # Read CSV file with study results
    csv_reader = csv.reader(csv_file, delimiter=',')

    # Iterate over table rows
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            result = processRow(row)
            if not result["google"] == None:
                graphs_google.append(result["google"])
            if not result["apple"] == None:
                graphs_apple.append(result["apple"])
            line_count += 1

    writeJSON("results/results_google.json", graphs_google)
    writeJSON("results/results_apple.json", graphs_apple)
