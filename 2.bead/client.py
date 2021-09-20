import json
import sys

json_path = sys.argv[1]

with open(json_path) as f:
    data = json.load(f)

possible_circuits = sorted(data["possible-circuits"], key=len)
capacities = {tuple(sorted(l["points"])): l["capacity"] for l in data["links"]}
reservations = [None] * len(data["simulation"]["demands"])

event_num = 0
res_format = "{event_num}. igény foglalás: {start}<->{end} st:{t} - {succ}"
fr_format = "{event_num}. igény felszabadítás: {start}<->{end} st:{t}"


def get_links(circuit):
    return (tuple(sorted(link)) for link in zip(circuit, circuit[1:]))

def reserve(start, end, demand):
    for i, c in enumerate(possible_circuits):
        if {start, end} == {c[0], c[-1]} and all(capacities[link] >= demand for link in get_links(c)):
            for link in get_links(c):
                capacities[link] -= demand

            return i
    return None


for t in range(1, data["simulation"]["duration"]+1):
    for i, d in enumerate(data["simulation"]["demands"]):
        if d["end-time"] == t and reservations[i] is not None:
            start, end = d['end-points']
            for link in get_links(possible_circuits[reservations[i]]):
                capacities[link] += d["demand"]

            event_num += 1
            print(fr_format.format(**vars()))

    for i, d in enumerate(data["simulation"]["demands"]):
        if d["start-time"] == t:
            start, end = d['end-points']

            reservations[i] = reserve(start, end, d["demand"])
            succ = "sikertelen" if reservations[i] is None else "sikeres"

            event_num += 1
            print(res_format.format(**vars()))
