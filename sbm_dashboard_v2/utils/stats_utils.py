import os, json

def calculate_shift_stats(tunnels):
    stats = {"A":0,"B":0,"C":0}
    for t in tunnels.values():
        for f in os.listdir(t["image_dir"]):
            if f.endswith(".json"):
                d = json.load(open(os.path.join(t["image_dir"],f)))
                s = d.get("shift")
                if s in stats:
                    stats[s]+=1
    return stats
