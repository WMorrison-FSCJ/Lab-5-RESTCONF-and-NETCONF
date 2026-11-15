import json
import xmltodict
from common import DATA, log

def as_list(x):
    return x if isinstance(x, list) else [x]

# RESTCONF (JSON -> dict)
r_host = json.load(open(DATA / "restconf_1.json"))["Cisco-IOS-XE-native:hostname"]
log("PARSE_JSON_OK:1")
r_ver = json.load(open(DATA / "restconf_2.json"))["Cisco-IOS-XE-native:version"]
log("PARSE_JSON_OK:2")
r_ifs = json.load(open(DATA / "restconf_3.json"))["ietf-interfaces:interfaces-state"]["interface"]
r_up = sum(1 for i in as_list(r_ifs) if i["oper-status"] == "up")

# NETCONF (XML -> dict)
x1 = xmltodict.parse(open(DATA / "netconf_1.xml").read())
native = x1["rpc-reply"]["data"]["native"]
n_host, n_ver = native["hostname"], native["version"]
log("PARSE_XML_OK:1")

x2 = xmltodict.parse(open(DATA / "netconf_2.xml").read())
n_ifs = x2["rpc-reply"]["data"]["interfaces-state"]["interface"]
n_up = sum(1 for i in as_list(n_ifs) if i["oper-status"] == "up")
log("PARSE_XML_OK:2")

report = f"""LAB 5 REPORT: RESTCONF vs NETCONF

Field          RESTCONF (JSON)   NETCONF (XML)
Hostname       {r_host:<17} {n_host}
Version        {r_ver:<17} {n_ver}
Interfaces up  {r_up:<17} {n_up}

Both protocols read the same YANG data; RESTCONF delivered JSON over HTTPS,
NETCONF delivered XML over SSH.
"""

(DATA / "reports" / "lab5_report.txt").write_text(report)
print(report)
log("REPORT_SAVED=lab5_report.txt")
