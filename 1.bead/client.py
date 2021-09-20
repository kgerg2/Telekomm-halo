import csv
import json
import platform
import subprocess
import sys
from datetime import date
from itertools import islice

csv_path = sys.argv[1]
commands = (["tracert", "-h", "30"], ["ping", "-n", "10"])
thread_count = 20

with open(csv_path) as f:
    urls = [url for _, url in csv.reader(f)]
    urls = urls[:10] + urls[-10:]

ps = ((cmd[0], url, subprocess.Popen([*cmd, url], stdout=subprocess.PIPE)) for cmd in commands for url in urls)

finished = {"ping": [], "tracert": []}
running = list(islice(ps, thread_count))

while running:
    still_running = []
    for cmd, url, p in running:
        if p.poll() is not None:
            finished[cmd].append({"target": url, "output": p.communicate()[0].decode()})
        else:
            still_running.append((cmd, url, p))

    running = still_running
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
