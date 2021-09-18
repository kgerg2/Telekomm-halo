import csv
import platform
import subprocess
import sys
import json
from datetime import date
from itertools import islice

# csv_path = sys.argv[1]
csv_path = "2.ora/top-1m.csv"

thread_count = 20

with open(csv_path) as f:
    reader = csv.reader(f)
    urls = [url for _, url in reader][:10]

# trs = [subprocess.Popen(["tracert", "-h", "30", url],
#                         stdout=subprocess.PIPE, stderr=subprocess.PIPE) for url in urls]
# trs = [subprocess.Popen(["echo", f"tracert {url} - start", "1>&2", "&&", "tracert", "-h", "30", url, "&&", "echo", f"tracert {url} - end", "1>&2"],
#                         stdout=subprocess.PIPE, shell=True) for url in urls]
# ps = [subprocess.Popen(["echo", f"ping {url} - start", "1>&2", "&&", "ping", "-n", "10", url, "&&", "echo", f"ping {url} - end", "1>&2"],
#                        stdout=subprocess.PIPE, shell=True) for url in urls]

ps = ((cmd[0], url, subprocess.Popen(["echo", f"{cmd[0]} {url} - start", "1>&2", "&&", *cmd, url, "&&", "echo", f"{cmd[0]} {url} - end", "1>&2"],
                                     stdout=subprocess.PIPE, shell=True)) for cmd in (["tracert", "-h", "30"], ["ping", "-n", "10"]) for url in urls)

finished = {"ping": [], "tracert": []}
running = list(islice(ps, thread_count))

while running:
    still_runnung = []
    for cmd, url, p in running:
        if p.poll() is not None:
            finished[cmd].append(
                {"target": url, "output": p.communicate()[0].decode()})
        else:
            still_runnung.append((cmd, url, p))

    running = still_runnung[:]
    # running = list(filter(lambda x: x[2].poll() is None, running))
    running.extend(islice(ps, thread_count - len(running)))


def write_to_file(path, **kwargs):
    d = {
        "date": date.today().strftime("%Y%m%d"),
        "system": platform.system().lower()
    }
    d.update(kwargs)

    with open(path, "w") as f:
        json.dump(d, f)

write_to_file("traceroute.json", traces=finished["tracert"])
write_to_file("ping.json", pings=finished["ping"])

# with open("traceroute.json", "w") as f:
#     json.dump({
#         "date": today,
#         "system": system,
#         "traces": finished["tracert"]
#     }, f)


# with open("ping.json", "w") as f:
#     json.dump({
#         "date": today,
#         "system": system,
#         "pings": finished["ping"]
#     }, f)
