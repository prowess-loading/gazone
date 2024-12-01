import random

proxy_config = {
    "host": "pr.7vfi6pj1.lunaproxy.net",
    "port": 12233,
    "username": "prowess_B6vvA",
    "password": "VU7mRaafTWhwd",

    "region": {
        "us": "us",
        "na": ["us", "ca", "mx", "br"],
        "au": ["au", "nz"],
        "as": ["jp", "sg", "hk", "kr"],
        "eu": [
            "gb", "de", "fr", "it", "se", "be", "at", "es", "ie", "fi", "pt", "lv", "pl",
            "hu", "nl", "ch", "cz", "no", "is", "gr", "ua", "hr"
        ]
    }
}

# rd, us, na, au, as, eu


def generate_proxy_with_region(region):
    regions = proxy_config["region"]
    selected_regions = []

    if region == "rd":
        selected_regions = [random.choice(
            sum([v if isinstance(v, list) else [v] for v in regions.values()], []))]

    else:
        region_keys = region.split(", ")
        for key in region_keys:
            if key in regions:
                selected_regions.extend(regions[key] if isinstance(
                    regions[key], list) else [regions[key]])

    selected_region = random.choice(selected_regions)

    proxy_string = f"https://user-{proxy_config['username']}-region-{selected_region}:{proxy_config['password']}@{proxy_config['host']}:{proxy_config['port']}"

    return proxy_string
