import string

ID_INDEX = 0
SERVICES_INDEX = 11

GOOGLE_INDEX = 17
APPLE_INDEX = 35
AMAZON_INDEX = 45
FACEBOOK_INDEX = 58
LINKEDIN_INDEX = 74
TWITTER_INDEX = 84


def parse_index(row):
    return row[ID_INDEX]


def parse_services(row):
    services = []
    for i in range(6):
        if not row[SERVICES_INDEX+i] == "":
            services.append(i)
    return services


def parse_Google_account(row):
    second_factor = False
    secondary_methods_indices = []
    fallback_methods_indices = []

    SECOND_FACTOR_ENABLED_INDEX = GOOGLE_INDEX+5
    APP_PASSWORDS_ENABLED_INDEX = GOOGLE_INDEX+6
    SECOND_FACTOR_METHODS_INDEX = GOOGLE_INDEX+8
    RECOVERY_METHODS_INDEX = GOOGLE_INDEX+16

    if row[SECOND_FACTOR_ENABLED_INDEX] == "Yes":
        second_factor = True

    if second_factor:
        for i in range(5):
            if not row[SECOND_FACTOR_METHODS_INDEX+i] == "":
                secondary_methods_indices.append(i)

        if row[APP_PASSWORDS_ENABLED_INDEX] == "Yes":
            secondary_methods_indices.append(5)

    for i in range(2):
        if not row[RECOVERY_METHODS_INDEX+i] == "":
            fallback_methods_indices.append(i)

    return {"secondary_methods_indices": secondary_methods_indices, "fallback_methods_indices": fallback_methods_indices}


def parse_Apple_account(row):
    secondary_methods_indices = []
    fallback_methods_indices = []

    TRUSTED_PHONE_NUMBERS_INDEX = APPLE_INDEX+5
    TRUSTED_DEVICES_INDEX = APPLE_INDEX+6
    RECOVERY_METHODS_INDEX = APPLE_INDEX+7

    if int(row[TRUSTED_DEVICES_INDEX]) > 0:
        secondary_methods_indices.append(0)

    if int(row[TRUSTED_PHONE_NUMBERS_INDEX]) > 0:
        secondary_methods_indices.append(1)

    if not row[RECOVERY_METHODS_INDEX+2] == "":
        fallback_methods_indices.append(1)
    else:
        fallback_methods_indices.append(0)

    return {"secondary_methods_indices": secondary_methods_indices, "fallback_methods_indices": fallback_methods_indices}

def parse_Amazon_account(row):
    second_factor = False
    secondary_methods_indices = []
    fallback_methods_indices = []

    SECOND_FACTOR_ENABLED_INDEX = AMAZON_INDEX+7
    SECOND_FACTOR_METHODS_INDEX = AMAZON_INDEX+8
    LOGIN_OPTIONS_INDEX = AMAZON_INDEX+5

    if row[SECOND_FACTOR_ENABLED_INDEX] == "Yes":
        second_factor = True

    if second_factor:
        for i in range(2):
            if not row[SECOND_FACTOR_METHODS_INDEX+i] == "":
                secondary_methods_indices.append(i)

    for i in range(2):
        if not row[LOGIN_OPTIONS_INDEX+i] == "":
            fallback_methods_indices.append(i)

    return {"secondary_methods_indices": secondary_methods_indices, "fallback_methods_indices": fallback_methods_indices}


def parse_Facebook_account(row):
    second_factor = False
    secondary_methods_indices = []
    fallback_methods_indices = []

    SECOND_FACTOR_ENABLED_INDEX = FACEBOOK_INDEX+7
    SECOND_FACTOR_METHODS_INDEX = FACEBOOK_INDEX+8
    LOGIN_OPTIONS_INDEX = FACEBOOK_INDEX+5

    if row[SECOND_FACTOR_ENABLED_INDEX] == "Yes":
        second_factor = True

    if second_factor:
        for i in range(4):
            if not row[SECOND_FACTOR_METHODS_INDEX+i] == "":
                secondary_methods_indices.append(i)

    for i in range(2):
        if not row[LOGIN_OPTIONS_INDEX+i] == "" and not row[LOGIN_OPTIONS_INDEX+i] == "None":
            fallback_methods_indices.append(i)

    return {"secondary_methods_indices": secondary_methods_indices, "fallback_methods_indices": fallback_methods_indices}


def parse_LinkedIn_account(row):
    second_factor = False
    secondary_methods_indices = []
    fallback_methods_indices = []

    SECOND_FACTOR_ENABLED_INDEX = LINKEDIN_INDEX+8
    SECOND_FACTOR_METHODS_INDEX = LINKEDIN_INDEX+9
    LOGIN_OPTIONS_INDEX = LINKEDIN_INDEX+5


    if row[SECOND_FACTOR_ENABLED_INDEX] == "Yes":
        second_factor = True
    
    if second_factor:
        for i in range(2):
            if not row[SECOND_FACTOR_METHODS_INDEX+i] == "":
                secondary_methods_indices.append(i)

    for i in range(2):
        if not row[LOGIN_OPTIONS_INDEX+i] == "" and not row[LOGIN_OPTIONS_INDEX+i] == "None":
            fallback_methods_indices.append(i)

    return {"secondary_methods_indices": secondary_methods_indices, "fallback_methods_indices": fallback_methods_indices}

def parse_Twitter_account(row):
    secondary_methods_indices = []
    fallback_methods_indices = []

    SECOND_FACTOR_METHODS_INDEX = TWITTER_INDEX+6
    LOGIN_OPTIONS_INDEX = TWITTER_INDEX+14

    
    for i in range(4):
        if not row[SECOND_FACTOR_METHODS_INDEX+i] == "":
            secondary_methods_indices.append(i)

    for i in range(2):
        if not row[LOGIN_OPTIONS_INDEX+i] == "" and not row[LOGIN_OPTIONS_INDEX+i] == "None":
            fallback_methods_indices.append(i)

    return {"secondary_methods_indices": secondary_methods_indices, "fallback_methods_indices": fallback_methods_indices}