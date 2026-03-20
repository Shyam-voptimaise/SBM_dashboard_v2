import os, json

def load_metadata(img):
    p = os.path.splitext(img)[0] + ".json"
    if os.path.exists(p):
        return json.load(open(p))
    return {"defects":[]}

def save_metadata(img,data):
    p = os.path.splitext(img)[0] + ".json"
    json.dump(data, open(p,"w"), indent=4)
