import json


def loadJSON(file):
    f = open(file)
    data = json.load(f)
    f.close()
    return data


def model_from_file(file, secondary_methods_indices=[], fallback_methods_indices=[]):
    modelData = loadJSON(file)

    # Expected model structure:
    #
    #                      root
    #                       |
    #            &                 (*Fallback)
    #   Password   (*Secondary)
    #

    # Extract secondary methods from original model
    rootName = modelData["graph"]["label"]

    modelDataSecondaryList = []
    if modelData["graph"]["children"][0]["children"][0]["type"] == "operator" and modelData["graph"]["children"][0]["children"][0]["value"] == "&":
        # Multiple secondary options
        if modelData["graph"]["children"][0]["children"][0]["children"][1]["type"] == "operator" and modelData["graph"]["children"][0]["children"][0]["children"][1]["value"] == "|":
            modelDataSecondaryList = modelData["graph"]["children"][0]["children"][0]["children"][1]["children"]
        # One secondary option
        else:
            modelDataSecondaryList = [
                modelData["graph"]["children"][0]["children"][0]["children"][1]
            ]

    # Extract fallback methods from original model
    modelDataFallbackList = []
    if modelData["graph"]["children"][0]["children"][1]["type"] == "operator" and modelData["graph"]["children"][0]["children"][1]["value"] == "|":
        modelDataFallbackList = modelData["graph"]["children"][0]["children"][1]["children"]
    else:
        modelDataFallbackList = [modelData["graph"]["children"][0]["children"][1]]

    secondary_methods = []
    # Generate list of second factors
    for index in secondary_methods_indices:
        secondary_methods.append(modelDataSecondaryList[index])

    # Generate list of fallback methods
    fallback_methods = []
    for index in fallback_methods_indices:
        fallback_methods.append(modelDataFallbackList[index])

    authentication = {
        "type": "operator",
        "value": "&",
        "children": [{
            "type": "authentication",
            "value": "knowledge",
            "score": 1,
            "devices": [],
            "label": "Password"
        },
            {
            "type": "operator",
            "value": "|",
            "children": secondary_methods if len(secondary_methods) > 0 else []
        } if len(secondary_methods) > 1 else secondary_methods[0]
        ]
    } if len(secondary_methods) > 0 else {
        "type": "authentication",
        "value": "knowledge",
        "score": 1,
        "devices": [],
        "label": "Password"
    }

    if len(fallback_methods) > 0:
        fallback = {
            "type": "operator",
            "value": "|",
            "children":  fallback_methods
        } if len(fallback_methods) > 1 else fallback_methods[0]

    return {
        "graph": {
            "type": "account",
            "label": rootName,
            "children": [{
                "type": "operator",
                "value": "|",
                "children": [
                    authentication,
                    fallback
                ]
            } if len(fallback_methods) > 0 else authentication
            ]
        }
    }
