import twpy
from lightcycle import LightCycle

info = {}
memory = {}

def _usage(data, usage):
    if not " " in data["message"] or not data["message"].split()[1]:
        twpy.send("Usage: {}".format(usage))
        return False
    return True

def mod_reset(data):
    if " " in data["message"]:
        split = data["message"].split()
        if split[1] == "memory":
            if len(split) > 1:
                if split[2].isdigit() and int(split[2]) in memory:
                    del memory[int(split[2])]
                    return "Memory #{} reset".format(split[2])
                else:
                    return "No memory of that module"
            else:
                return "Usage: !reset memory <TP number of module to be forgotten>"
        elif split[1] == "info":
            info = {}
            return "Bomb info reset"
        elif split[1] == "all":
            info = {}
            memory = {}
            return "All reset"
    else:
        return "Usage: !reset [info|memory|all]"

def mod_serial(data):
    if " " in data["message"]:
        s = data["message"].split()[1]
        if len(s) != 6:
            return "Invalid serial: " + s
        info["serial"] = s.upper()
        return "Serial confirmed: {}".format(info["serial"])
    return info["serial"] or "Not set"

def mod_lightcycle(data):
    if not info["serial"]:
        return "Provide serial with !serial first"
    colors = "".join(data["message"].split()[1:])
    if len(colors) != 6:
        return "Invalid colors"
    lc = LightCycle(info["serial"], colors)
    return " ".join(lc.colors)

def mod_sqr_button(data):
    cmd,*split = data["message"].split()
    if len(split) != 2:
        return "Invalid input"
    status,color = split
    def isprime(s):
        for i in range(3,s):
            if s % i == 0:
                return False
        return True
    def seconds_sum(s):
        if len(str(s)) == 2:
            return sum(map(int, str(s)))
        return s
    results = []
    for n in range(0, 60):
        if status == "flashing":
            if color == "cyan" and n%7 == 0:
                results.append(n)
            if color == "orange" and isprime(n):
                results.append(n)
            if color == "other" and seconds_sum(n)%4 == 0:
                results.append(n-1)
        elif status == "solid":
            if color == "cyan" and seconds_sum(n) == 7:
                results.append(n)
            if color == "orange" and seconds_sum(n) in [3,13]:
                results.append(n)
            if color == "other" and seconds_sum(n) == 5:
                results.append(n)
    if len(results) >= 1:
        return ", ".join("{:02d}".format(r) for r in results)
    return "No available results...."

def mod_memory(data):
    return "Not currently working"
    try:
        n,*opts = map(int,data["message"].split()[1:])
        if len(opts) != 5:
            raise ValueError
    except ValueError:
        return "memory: Invalid input"
    if not n in memory:
        memory[n] = []
    if len(memory[n]) == 0:
        memory[n].append({"opts": opts})
        cur = memory[n][0]
        if opts[0] in [1,2]:
            cur.update({"pos": 1, "label": opts[1]})
            return "memory: pos 2"
        elif opts[0] == 3:
            cur.update({"pos": 2, "label": opts[2]})
            return "memory: pos 3"
        elif opts[0] == 4:
            cur.update({"pos": 3, "label": opts[3]})
            return "memory: pos 4"
    if len(memory[n]) == 1:
        memory[n].append({"opts": opts})
        cur = memory[n][1]
        if opts[0] == 1:
            cur.update({"pos": opts.index(4), "label": 4})
            return "memory: label 4"
        if opts[0] in [2,4]:
            pos = memory[n][0]["pos"]
            cur.update({"pos": pos, "label": opts[pos]})
            return "memory: pos {}".format(pos+1)
        if opts[0] == 3:
            cur.update({"pos": 0, "label": opts[0]})
            return "memory: pos 1"
    if len(memory[n]) == 2:
        memory[n].append({"opts": opts})
        cur = memory[n][2]
        if opts[0] == 1:
            label = memory[n][1]["label"]
            cur.update({"pos": opts.index(label), "label": label})
            return "memory: label {}".format(label)
        if opts[0] == 2:
            label = memory[n][0]["label"]
            cur.update({"pos": opts.index(label), "label": label})
            return "memory: label {}".format(label)
        if opts[0] == 3:
            cur.update({"pos": 2, "label": opts[2]})
            return "memory: pos 3"
        if opts[0] == 4:
            cur.update({"pos": opts.index(4), "label": 4})
            return "memory: label 4"
    if len(memory[n]) == 3:
        memory[n].append({"opts": opts})
        cur = memory[n][3]
        if opts[0] == 1:
            pos = memory[n][0]["pos"]
            cur.update({"pos": pos, "label": opts[pos]})
            return "memory: pos {}".format(pos+1)
        if opts[0] == 2:
            cur.update({"pos": 0, "label": opts[0]})
            return "memory: pos 1"
        if opts[0] in [3,4]:
            pos = memory[n][1]["pos"]
            cur.update({"pos": pos, "label": opts[pos]})
            return "memory: pos {}".format(pos+1)
    if len(memory[n]) == 4:
        if opts[0] == 1:
            label = memory[n][0]["label"]
        if opts[0] == 2:
            label = memory[n][1]["label"]
        if opts[0] == 3:
            label = memory[n][3]["label"]
        if opts[0] == 4:
            label = memory[n][2]["label"]
        return "memory: label {}".format(label)

if __name__ == "__main__":
    response = twpy.chat()
    for data in response:
        if data["message"].startswith("!reset") and data["mod"] != 0:
            twpy.send("reset: " + mod_reset(data))
        if data["message"].startswith("!serial"):
            if not _usage(data, "!serial <serial number, case insensitive>"):
                continue
            twpy.send("serial: " + mod_serial(data))
        if data["message"].startswith("!lightcycle"):
            if not _usage(data, "!lightcycle <colors, spaces optional, e.g rgbymw>"):
                continue
            twpy.send("lightcycle: " + mod_lightcycle(data))
        if data["message"].startswith("!memory"):
            if not _usage(data, "!memory <unique module number> <display> <buttons separated by spaces>"):
                continue
            twpy.send("memory: " + mod_memory(data))
        if data["message"].startswith("!squarebutton"):
            if not _usage(data, "!squarebutton [solid|flashing] [cyan|orange|other]"):
                continue
            twpy.send("squarebutton: " + mod_sqr_button(data))
