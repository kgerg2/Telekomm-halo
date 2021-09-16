import csv
import platform
import subprocess
import sys
import json
from datetime import date

# csv_path = sys.argv[1]
csv_path = "2.ora/top-1m.csv"

trs = []
ps = []

with open(csv_path) as f:
    reader = csv.reader(f)
    urls = [url for _, url in reader][:50]

trs = [subprocess.Popen(["tracert", "-h", "30", url], stdout=subprocess.PIPE, stderr=subprocess.PIPE) for url in urls]
ps = [subprocess.Popen(["ping", "-n", "10", url], stdout=subprocess.PIPE, stderr=subprocess.PIPE) for url in urls]

print(platform.system())

traces = [{"target": url, "output": tr.communicate()} for url, tr in zip(urls, trs)]
pings = [{"target": url, "output": ping.communicate()} for url, ping in zip(urls, ps)]

tr = {
    "date": date.today().strftime("%Y%m%d"),
    "system": platform.system().lower(),
    "traces": traces
}

with open("traceroute.json", "w") as f:
    json.dump(tr, f)