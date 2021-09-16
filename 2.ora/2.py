import subprocess

p = subprocess.run(["echo", "hello world"], stdout=subprocess.PIPE, shell=True)

print(p.stdout)

ps = []

for _ in range(5):
    ps.append(subprocess.Popen(["ping", "xkcd.com"], stdout=subprocess.PIPE, stderr=subprocess.PIPE))

for p in ps:
    print(p.communicate())

# tracert -h
# ping -n