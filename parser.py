ID_INDEX = 0
DEVICES_INDEX = 5
SERVICES_GOOGLE_INDEX = 15
SERVICES_APPLE_INDEX = 16

GOOGLE_INDEX = 20
APPLE_INDEX = 114
AMAZON_INDEX = 45
#FACEBOOK_INDEX = 58
#LINKEDIN_INDEX = 74
#TWITTER_INDEX = 84


def parse_number(val):
    if val == "None":
        return 0
    elif val == "4 or more":
        return 4
    else:
        return int(val)


def parse_index(row):
    return row[ID_INDEX]


def parse_services(row):
    services = []
    if not row[SERVICES_GOOGLE_INDEX] == "":
        services.append("google")
    if not row[SERVICES_APPLE_INDEX] == "":
        services.append("apple")
    return services


def parse_devices(row):
    devices = []
    for i in range(10):
        if not row[DEVICES_INDEX+i] == "":
            devices.append(
                {"id": "d{}".format(i+1), "type": row[DEVICES_INDEX+i]})
    return devices


def parse_device_selection(row, start_index):
    offset = 2  # first two devices are possible access methods for password
    devices = []
    for i in range(10):
        if not row[start_index+i] == "":
            devices.append(i+offset)
    return devices


def parse_password_access(row, start_index):
    MEMORY_INDEX = start_index
    PASSWORD_MANAGER_INDEX = start_index+1
    DEVICE_STORE_INDEX = start_index+2
    PAPER_INDEX = start_index+3
    PASSWORD_MANAGER_DEVICES_INDEX = start_index+4
    DEVICE_STORE_DEVICES_INDEX = start_index+14

    password_access = []
    if not row[MEMORY_INDEX] == "":
        password_access.append({"type": "memory", "devices": []})
    if not row[PAPER_INDEX] == "":
        password_access.append({"type": "paper", "devices": []})

    if not row[PASSWORD_MANAGER_INDEX] == "":
        password_access.append({"type": "password_manager", "devices": parse_device_selection(
            row, PASSWORD_MANAGER_DEVICES_INDEX)})
    if not row[DEVICE_STORE_INDEX] == "":
        password_access.append({"type": "device_store", "devices": parse_device_selection(
            row, DEVICE_STORE_DEVICES_INDEX)})

    return password_access


def parse_Google_account(row):
    second_factor = False
    secondary_methods = []
    fallback_methods = []

    PASSWORD_ACCESS_INDEX = GOOGLE_INDEX+1
    SECOND_FACTOR_ENABLED_INDEX = GOOGLE_INDEX+25
    APP_PASSWORDS_ENABLED_INDEX = GOOGLE_INDEX+26
    APP_PASSWORDS_DEVICES_INDEX = GOOGLE_INDEX+27  # 5
    SECOND_FACTOR_METHODS_INDEX = GOOGLE_INDEX+37

    GOOGLE_PROMPTS_DEVICES_INDEX = GOOGLE_INDEX+42  # 0
    AUTHENTICATOR_APP_DEVICES_INDEX = GOOGLE_INDEX+52  # 1
    PHONE_DEVICES_INDEX = GOOGLE_INDEX+62  # 3
    SECURITY_KEY_DEVICES_INDEX = GOOGLE_INDEX+72  # 4

    RECOVERY_METHODS_INDEX = GOOGLE_INDEX+82
    RECOVERY_PHONE_DEVICES_INDEX = GOOGLE_INDEX+84

    password_access = parse_password_access(row, PASSWORD_ACCESS_INDEX)

    if row[SECOND_FACTOR_ENABLED_INDEX] == "1":
        second_factor = True

    if second_factor:
        for i in range(5):
            if not row[SECOND_FACTOR_METHODS_INDEX+i] == "":
                # parse devices
                devices = []
                if i == 0:
                    devices = parse_device_selection(
                        row, GOOGLE_PROMPTS_DEVICES_INDEX)
                elif i == 1:
                    devices = parse_device_selection(
                        row, AUTHENTICATOR_APP_DEVICES_INDEX)
                elif i == 3:
                    devices = parse_device_selection(
                        row, PHONE_DEVICES_INDEX)
                elif i == 4:
                    devices = parse_device_selection(
                        row, SECURITY_KEY_DEVICES_INDEX)
                secondary_methods.append({"id": i, "devices": devices})

        if row[APP_PASSWORDS_ENABLED_INDEX] == "1":
            # parse devices
            devices = []
            devices = parse_device_selection(
                row, APP_PASSWORDS_DEVICES_INDEX)
            secondary_methods.append({"id": 5, "devices": devices})

    for i in range(2):
        if not row[RECOVERY_METHODS_INDEX+i] == "":
            devices = []
            if i == 0:
                devices = parse_device_selection(
                    row, RECOVERY_PHONE_DEVICES_INDEX)

            fallback_methods.append({"id": i, "devices": devices})

    return {"password_access": password_access, "secondary_methods": secondary_methods, "fallback_methods": fallback_methods}


def parse_Apple_account(row):
    secondary_methods = []
    fallback_methods = []

    PASSWORD_ACCESS_INDEX = APPLE_INDEX+1
    TRUSTED_PHONE_NUMBERS_INDEX = APPLE_INDEX+25
    TRUSTED_DEVICES_INDEX = APPLE_INDEX+35
    RECOVERY_METHODS_INDEX = APPLE_INDEX+45

    password_access = parse_password_access(row, PASSWORD_ACCESS_INDEX)

    devices = parse_device_selection(
        row, TRUSTED_DEVICES_INDEX)
    if len(devices) > 0:
        secondary_methods.append({"id": 0, "devices": devices})

    devices = parse_device_selection(
        row, TRUSTED_PHONE_NUMBERS_INDEX)
    if len(devices) > 0:
        secondary_methods.append({"id": 1, "devices": devices})

    if not row[RECOVERY_METHODS_INDEX+2] == "":
        devices = []
        fallback_methods.append({"id": 1, "devices": devices})
    else:
        devices = []
        fallback_methods.append({"id": 0, "devices": devices})

    return {"password_access": password_access, "secondary_methods": secondary_methods, "fallback_methods": fallback_methods}


def parse_Amazon_account(row):
    second_factor = False
    secondary_methods = []
    fallback_methods = []

    SECOND_FACTOR_ENABLED_INDEX = AMAZON_INDEX+7
    SECOND_FACTOR_METHODS_INDEX = AMAZON_INDEX+8
    LOGIN_OPTIONS_INDEX = AMAZON_INDEX+5

    if row[SECOND_FACTOR_ENABLED_INDEX] == "Yes":
        second_factor = True

    if second_factor:
        for i in range(2):
            if not row[SECOND_FACTOR_METHODS_INDEX+i] == "":
                secondary_methods.append(i)

    for i in range(2):
        if not row[LOGIN_OPTIONS_INDEX+i] == "":
            fallback_methods.append(i)

    return {"secondary_methods": secondary_methods, "fallback_methods": fallback_methods}


def parse_Facebook_account(row):
    second_factor = False
    secondary_methods = []
    fallback_methods = []

    SECOND_FACTOR_ENABLED_INDEX = FACEBOOK_INDEX+7
    SECOND_FACTOR_METHODS_INDEX = FACEBOOK_INDEX+8
    LOGIN_OPTIONS_INDEX = FACEBOOK_INDEX+5

    if row[SECOND_FACTOR_ENABLED_INDEX] == "Yes":
        second_factor = True

    if second_factor:
        for i in range(4):
            if not row[SECOND_FACTOR_METHODS_INDEX+i] == "":
                secondary_methods.append(i)

    for i in range(2):
        if not row[LOGIN_OPTIONS_INDEX+i] == "" and not row[LOGIN_OPTIONS_INDEX+i] == "None":
            fallback_methods.append(i)

    return {"secondary_methods": secondary_methods, "fallback_methods": fallback_methods}


def parse_LinkedIn_account(row):
    second_factor = False
    secondary_methods = []
    fallback_methods = []

    SECOND_FACTOR_ENABLED_INDEX = LINKEDIN_INDEX+8
    SECOND_FACTOR_METHODS_INDEX = LINKEDIN_INDEX+9
    LOGIN_OPTIONS_INDEX = LINKEDIN_INDEX+5

    if row[SECOND_FACTOR_ENABLED_INDEX] == "Yes":
        second_factor = True

    if second_factor:
        for i in range(2):
            if not row[SECOND_FACTOR_METHODS_INDEX+i] == "":
                secondary_methods.append(i)

    for i in range(2):
        if not row[LOGIN_OPTIONS_INDEX+i] == "" and not row[LOGIN_OPTIONS_INDEX+i] == "None":
            fallback_methods.append(i)

    return {"secondary_methods": secondary_methods, "fallback_methods": fallback_methods}


# def parse_Twitter_account(row):
#    secondary_methods = []
#    fallback_methods = []
#
#    SECOND_FACTOR_METHODS_INDEX = TWITTER_INDEX+6
#    LOGIN_OPTIONS_INDEX = TWITTER_INDEX+14
#
#    for i in range(4):
#        if not row[SECOND_FACTOR_METHODS_INDEX+i] == "":
#            secondary_methods.append(i)
#
#    for i in range(2):
#        if not row[LOGIN_OPTIONS_INDEX+i] == "" and not row[LOGIN_OPTIONS_INDEX+i] == "None":
#            fallback_methods.append(i)
#
#    return {"secondary_methods": secondary_methods, "fallback_methods": fallback_methods}
