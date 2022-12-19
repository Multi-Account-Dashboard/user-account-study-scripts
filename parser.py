ID_INDEX = 0
DEVICES_INDEX = 6
SERVICES_GOOGLE_INDEX = 16
SERVICES_APPLE_INDEX = 17

GOOGLE_INDEX = 21
APPLE_INDEX = 83
#AMAZON_INDEX = 46
#FACEBOOK_INDEX = 58
#LINKEDIN_INDEX = 74
#TWITTER_INDEX = 84

DEVICES = ["p1", "p2", "p3", "c1", "c2", "c3", "t1", "t2", "s1", "s2"]


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
            device_type = ""
            if row[DEVICES_INDEX+i][0] == "p":
                device_type = "phone"
            elif row[DEVICES_INDEX+i][0] == "c":
                device_type = "computer"
            elif row[DEVICES_INDEX+i][0] == "t":
                device_type = "tablet"
            elif row[DEVICES_INDEX+i][0] == "s":
                device_type = "security_key"

            devices.append(
                {"id": row[DEVICES_INDEX+i], "type": device_type})
    return devices


def parse_device_selection(row, start_index, num):
    offset = 2  # first two devices are possible access methods for password
    devices = []
    for i in range(num):
        if not row[start_index+i] == "":
            devices.append(row[start_index+i])
    return devices


def parse_password_access(row, start_index):
    MEMORY_INDEX = start_index
    PASSWORD_MANAGER_INDEX = start_index+1
    DEVICE_STORE_INDEX = start_index+2
    PAPER_INDEX = start_index+3
    PASSWORD_MANAGER_DEVICES_INDEX = start_index+4
    DEVICE_STORE_DEVICES_INDEX = start_index+12

    password_access = []
    if not row[MEMORY_INDEX] == "":
        password_access.append({"type": "memory", "devices": []})
    if not row[PAPER_INDEX] == "":
        password_access.append({"type": "paper", "devices": []})

    if not row[PASSWORD_MANAGER_INDEX] == "":
        password_access.append({"type": "password_manager", "devices": parse_device_selection(
            row, PASSWORD_MANAGER_DEVICES_INDEX, 8)})
    if not row[DEVICE_STORE_INDEX] == "":
        password_access.append({"type": "device_store", "devices": parse_device_selection(
            row, DEVICE_STORE_DEVICES_INDEX, 8)})

    return password_access


def parse_Google_account(row):
    second_factor = False
    secondary_methods = []
    fallback_methods = []

    PASSWORD_ACCESS_INDEX = GOOGLE_INDEX+1
    SECOND_FACTOR_ENABLED_INDEX = GOOGLE_INDEX+21
    APP_PASSWORDS_ENABLED_INDEX = GOOGLE_INDEX+22
    APP_PASSWORDS_DEVICES_INDEX = GOOGLE_INDEX+23  # 5
    SECOND_FACTOR_METHODS_INDEX = GOOGLE_INDEX+31

    GOOGLE_PROMPTS_DEVICES_INDEX = GOOGLE_INDEX+36  # 0
    AUTHENTICATOR_APP_DEVICES_INDEX = GOOGLE_INDEX+44  # 1
    PHONE_DEVICES_INDEX = GOOGLE_INDEX+52  # 3
    SECURITY_KEY_DEVICES_INDEX = GOOGLE_INDEX+55  # 4

    RECOVERY_METHODS_INDEX = GOOGLE_INDEX+57
    RECOVERY_PHONE_DEVICES_INDEX = GOOGLE_INDEX+59

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
                        row, GOOGLE_PROMPTS_DEVICES_INDEX, 8)
                elif i == 1:
                    devices = parse_device_selection(
                        row, AUTHENTICATOR_APP_DEVICES_INDEX, 8)
                elif i == 3:
                    devices = parse_device_selection(
                        row, PHONE_DEVICES_INDEX, 3)
                elif i == 4:
                    devices = parse_device_selection(
                        row, SECURITY_KEY_DEVICES_INDEX, 2)
                secondary_methods.append({"id": i, "devices": devices})

        if row[APP_PASSWORDS_ENABLED_INDEX] == "1":
            # parse devices
            devices = []
            devices = parse_device_selection(
                row, APP_PASSWORDS_DEVICES_INDEX, 8)
            secondary_methods.append({"id": 5, "devices": devices})

    for i in range(2):
        if not row[RECOVERY_METHODS_INDEX+i] == "":
            devices = []
            if i == 0:
                devices = parse_device_selection(
                    row, RECOVERY_PHONE_DEVICES_INDEX, 3)

            fallback_methods.append({"id": i, "devices": devices})

    return {"password_access": password_access, "secondary_methods": secondary_methods, "fallback_methods": fallback_methods}


def parse_Apple_account(row):
    secondary_methods = []
    fallback_methods = []

    PASSWORD_ACCESS_INDEX = APPLE_INDEX+1
    TRUSTED_PHONE_NUMBERS_INDEX = APPLE_INDEX+21
    TRUSTED_DEVICES_INDEX = APPLE_INDEX+24
    RECOVERY_METHODS_INDEX = APPLE_INDEX+32

    password_access = parse_password_access(row, PASSWORD_ACCESS_INDEX)
    

    trusted_devices = parse_device_selection(
        row, TRUSTED_DEVICES_INDEX, 8)
    if len(trusted_devices) > 0:
        secondary_methods.append({"id": 0, "devices": trusted_devices})

    trusted_phones = parse_device_selection(
        row, TRUSTED_PHONE_NUMBERS_INDEX, 3)
    if len(trusted_phones) > 0:
        secondary_methods.append({"id": 1, "devices": trusted_phones})
    
    if not row[RECOVERY_METHODS_INDEX+1] == "":
        #devices = []
        fallback_methods.append({"id": 1, "devices": "pap2"})
    else:
        fallback_methods.append({"id": 0, "devices": trusted_devices})
    
    return {"password_access": password_access, "secondary_methods": secondary_methods, "fallback_methods": fallback_methods}
