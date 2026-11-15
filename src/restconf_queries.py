import json
import requests
import urllib3
from common import DATA, log

urllib3.disable_warnings()

HOST = "devnetsandboxiosxec8k.cisco.com"
USER, PASSWORD = "s3807777", "R%q$75vVN6z2n"
BASE = f"https://{HOST}/restconf/data/"
HEADERS = {"Accept": "application/yang-data+json"}

ENDPOINTS = {
    1: "Cisco-IOS-XE-native:native/hostname",
    2: "Cisco-IOS-XE-native:native/version",
    3: "ietf-interfaces:interfaces-state",
}

connected = False
for n, path in ENDPOINTS.items():
    try:
        r = requests.get(BASE + path, auth=(USER, PASSWORD),
                         headers=HEADERS, timeout=10, verify=False)
        print(r.status_code, r.headers.get("Content-Type"))
        print(r.text[:300])
        r.raise_for_status()
        data = r.json()
    except (requests.RequestException, ValueError) as e:
        log(f"RESTCONF_REQ_FAIL:{n} ({e})")
        continue
    if not connected:
        log("CONNECT_OK: RESTCONF")
        connected = True
    log(f"RESTCONF_REQ_OK:{n}")

    with open(DATA / f"restconf_{n}.json", "w") as f:
        json.dump(data, f, indent=2)
    log(f"RAW_SAVED=restconf_{n}.json")
