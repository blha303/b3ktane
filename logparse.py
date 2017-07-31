import tailer
import json

with open("settings.json") as f:
    opts = json.load(f)

_BOMB = {
        "seed": "",
        "time": "",
        "time_pretty": "",
        "strikes": "",
        "flip": "",
        "serial": "",
        "modules": [],
        "plates": 0,
        "holders": 0,
        "ports": [],
        "batts": [],
        "indicators": {"unlit": [], "lit": []},
        "rip": False
        }
BOMB = dict(_BOMB)

def hms(s):
    m,s = divmod(int(s), 60)
    h,m = divmod(m, 60)
    return h,m,s

def parse(line):
    global BOMB
    if line[:5] not in ["DEBUG", "INFO"]:
        return
    modid, info = line.strip().split(maxsplit=4)[3:]
    split = info.split()
    # disabled block, unnecessary
    if False and modid == "[BombGenerator]":
        # [BombGenerator] Generating bomb with seed 1022778702
        if "seed" in info:
            BOMB["seed"] = split[-1]
        # [BombGenerator] Generator settings: Time: 5520, NumStrikes: 3, FrontFaceOnly: False
        if info.startswith("Generator settings:"):
            BOMB["time"], BOMB["strikes"], BOMB["flip"] = \
                    [a.split(", ")[0] for a in info.split(": ")]
            BOMB["time_pretty"] = "{0}:{1:02d}:{2:02d}".format(*hms(BOMB["time"]))
        # [BombGenerator] Instantiated AdvancedMorse on face RearFace, spawn index 8
        if info.startswith("Instantiated "):
            BOMB["modules"].append({
                "module": split[1],
                "face": split[-4][:-1],
                "index": split[-1]
            })
    if modid == "[WidgetGenerator]":
        # [WidgetGenerator] Added widget: PortWidget at 0, 1
        if info.startswith("Added widget: PortWidget"):
            BOMB["plates"] += 1
        # [WidgetGenerator] Added widget: BatteryWidget at 0, 1
        if info.startswith("Added widget: BatteryWidget"):
            BOMB["holders"] += 1
    if modid == "[PortWidget]":
        # [PortWidget] Randomizing Port Widget: 0
        if split[-1] != "0":
        # [PortWidget] Randomizing Port Widget: RJ45
            BOMB["ports"].append(split[-1].replace("Stereo", "").lower())
    if modid == "[BatteryWidget]":
        # [BatteryWidget] Randomizing Battery Widget: 2
        # 1 = d, 2 = aa
        BOMB["batts"].append(split[-1])
    if modid == "[IndicatorWidget]":
        # [IndicatorWidget] Randomizing Indicator Widget: unlit IND
        BOMB["indicators"][split[-2]].append(split[-1])
    if modid == "[SerialNumber]":
        # [SerialNumber] Randomizing Serial Number: 9D3IQ9
        BOMB["serial"] = split[-1]
    if modid == "[Bomb]":
        if info == "Boom":
            BOMB["rip"] = True
            update_overlay()
            BOMB = dict(_BOMB)

def update_overlay(p=True):
    if p:
        print(json.dumps(BOMB, indent=4) + "\n-----------------------------------")
    with open(opts["overlay-output"], "w", encoding="utf-8") as f:
        if BOMB["rip"]:
            f.write("rip\n")
            return
        if any(k not in BOMB for k in ["serial", "ports", "indicators", "batts", "plates", "holders"]):
            return
        ports = (",".join(BOMB["ports"]) if BOMB["ports"] else "no ports") + " {}p".format(BOMB["plates"])
        inds = "\n".join("{} {}".format(k,",".join(v)) for k,v in BOMB["indicators"].items() if v) if BOMB["indicators"]["unlit"] or BOMB["indicators"]["lit"] else "no indicators"
        batts = ("{}aa".format(int(BOMB["batts"].count("2"))*2) if "2" in BOMB["batts"] else "") + \
                ("{}d".format(BOMB["batts"].count("1")) if "1" in BOMB["batts"] else "") + \
                ("{}h".format(BOMB["holders"]) if BOMB["holders"] > 0 else "no batteries")
        f.write("\n".join([BOMB["serial"], ports, inds, batts]) + "\n")

with open(opts["ktane-log"]) as f:
    curbomb = f.read().split("[State] Enter GameplayState\n")[-1].split("\n")
    print(curbomb[:3])
    for line in curbomb:
        parse(line)
        update_overlay(p=False)
    for line in tailer.follow(f):
        parse(line)
        update_overlay()
