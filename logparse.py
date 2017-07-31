import tailer
import json

with open("settings.json") as f:
    opts = json.load(f)

def reset_bomb():
    print("RESETTING")
    with open("template.json") as f:
        return json.load(f)
BOMB = reset_bomb()

def hms(s):
    m,s = divmod(int(s), 60)
    h,m = divmod(m, 60)
    return h,m,s

def parse(line):
    global BOMB
    if "[Assets.Scripts." in line:
        return
    try:
        modid, *split = line.strip().split()[3:]
        if not modid or modid[0] != "[":
            raise ValueError
    except ValueError:
        return
    info = " ".join(split)
    if modid == "[BombGenerator]":
        # [BombGenerator] Generating bomb with seed 1022778702
        if "Generating bomb with seed" in info:
            BOMB["seed"] = split[-1]
        # [BombGenerator] Generator settings: Time: 5520, NumStrikes: 3, FrontFaceOnly: False
        elif info.startswith("Generator settings:"):
            BOMB["time"], BOMB["strikes"], BOMB["flip"] = \
                    [a.split(", ")[0] for a in info.split(": ")[2:]]
            BOMB["time_pretty"] = "{0}:{1:02d}:{2:02d}".format(*hms(BOMB["time"]))
            with open("initial-time.txt", "w") as f:
                f.write(BOMB["time_pretty"])
        # disabled
        # [BombGenerator] Instantiated AdvancedMorse on face RearFace, spawn index 8
        elif False and info.startswith("Instantiated "):
            BOMB["modules"].append({
                "module": split[1],
                "face": split[-4][:-1],
                "index": split[-1]
            })
    elif modid == "[WidgetGenerator]":
        # [WidgetGenerator] Added widget: PortWidget at 0, 1
        if info.startswith("Added widget: PortWidget"):
            BOMB["plates"] += 1
        # [WidgetGenerator] Added widget: BatteryWidget at 0, 1
        elif info.startswith("Added widget: BatteryWidget"):
            BOMB["holders"] += 1
    elif modid == "[PortWidget]":
        # [PortWidget] Randomizing Port Widget: 0
        if split[-1] != "0":
        # [PortWidget] Randomizing Port Widget: RJ45
            BOMB["ports"].append([a.lower().replace(",", "").replace("stereo", "") for a in split[3:]])
        else:
            BOMB["ports"].append(["blank"])
    elif modid == "[BatteryWidget]":
        # [BatteryWidget] Randomizing Battery Widget: 2
        # 1 = d, 2 = aa
        BOMB["batts"].append(split[-1])
    elif modid == "[IndicatorWidget]":
        # [IndicatorWidget] Randomizing Indicator Widget: unlit IND
        BOMB["indicators"][split[-2]].append(split[-1])
    elif modid == "[SerialNumber]":
        # [SerialNumber] Randomizing Serial Number: 9D3IQ9
        BOMB["serial"] = split[-1]
    elif modid == "[Bomb]":
        if "Boom" in info or "A winner is you" in info:
            BOMB["rip"] = True
            if split[-1] != "Boom":
                BOMB["win"] = True
    else:
        return
    print(line)

def update_overlay(p=True):
    global BOMB
    if p:
        print(json.dumps(BOMB, indent=4) + "\n-----------------------------------")
    with open(opts["overlay-output"], "w+", encoding="utf-8") as f:
        if BOMB["rip"]:
            if not BOMB["win"]:
                f.write("rip\nwaiting for\nnext bomb")
            else:
                f.write("grats")
            BOMB = reset_bomb()
            return
        if not all(BOMB[k] for k in ["serial", "ports", "batts", "holders"]):
            return
        ports = (";".join(",".join(p) for p in BOMB["ports"]) if BOMB["ports"] else "no ports") + " {}p".format(BOMB["plates"])
        inds = "; ".join("{} {}".format(k,",".join(v)) for k,v in BOMB["indicators"].items() if v) if BOMB["indicators"]["unlit"] or BOMB["indicators"]["lit"] else "no indicators"
        batts = ("{}aa".format(int(BOMB["batts"].count("2"))*2) if "2" in BOMB["batts"] else "") + \
                ("{}d".format(BOMB["batts"].count("1")) if "1" in BOMB["batts"] else "") + \
                ("{}h".format(BOMB["holders"]) if BOMB["holders"] > 0 else "no batteries")
        out = " | ".join([BOMB["serial"], ports, inds, batts])
        if f.read() != out:
            f.seek(0)
            f.write(out)

with open(opts["ktane-log"]) as f1:
    curbomb = f1.read()
    if not "[State] Enter GameplayState\n" in curbomb:
        try:
            with open(opts["ktane-log"] + ".1") as f2:
                curbomb = f2.read() + curbomb
        except FileNotFoundError:
            pass
    for line in curbomb.split("[State] Enter GameplayState\n")[-1].split("\n"):
        parse(line)
        update_overlay(p=False)
    for line in tailer.follow(f1):
        parse(line)
        update_overlay()
