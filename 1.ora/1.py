from functools import cache
import json
# 1. feladat
def is_leap_year(x):
    return x % 400 == 0 or (x % 100 != 0 == x % 4)
print(list(map(is_leap_year, [1900, 1992, 1993, 1996, 2000, 2400])))
# 2. feladat
def ratio(points):
    return points["elert"] / points["max"]
percents = [0, 0.5, 0.6, 0.75, 0.85]
with open(r"C:\Users\X8B97C\Documents\results.json") as f:
    data = json.load(f)
achieved = (ratio(data["haziPont"]) + ratio(data["mininetPont"])) / 3
for i in range(1, 5):
    needed_percent = max(data["zhPont"]["minimum"], (percents[i] - achieved) * 3)
    if needed_percent > 1:
        print(f"{i+1} :  Remenytelen")
    else:
        needed_points = needed_percent * data["zhPont"]["max"]
        print(f"{i+1} :  {needed_points}")
# 3. feladat
@cache # ha ez a dekorátor nincs itt, az algoritmus négyzetes futási idejű, így csak lineáris n-ben
def fibonacci(n):
    return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)
print(fibonacci(100))