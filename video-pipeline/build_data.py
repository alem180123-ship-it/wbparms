"""Scenes (image + mood) and subtitle lines -> work/data.json for stage.html."""
import json
import re

words = json.load(open("work/words.json"))
en = json.load(open("work/energy.json"))
DUR = 79.25
U = "img/"
A, B, C, D = U + "staff.jpg", U + "desk.jpg", U + "hug.jpg", U + "dark.jpg"


def face(z0, z1, fx, fy, w=768, h=1028, pan=(0, 0)):
    """Ken Burns that centres a point (fx, fy as image fractions) while zooming."""
    dx, dy = (fx - .5) * w, (fy - .5) * h
    return {"from": [z0, -dx * z0 * .6, -dy * z0 * .6], "to": [z1, -dx * z1 + pan[0], -dy * z1 + pan[1]]}


# start, mode, image, enter, kb, tag, numeral, extra
S = [
    (0.0, "hard", A, "bottom", face(1.05, 1.25, .45, .35), "вопрос", "I", {"rot": -2}),
    (4.45, "soft", B, "left", {"from": [1.04, 0, 40], "to": [1.14, 0, -10]}, "отличие", "II", {"rot": 1.5}),
    (11.65, "hard", D, "right", face(1.15, 1.45, .5, .42), "первая версия", "III", {"rot": 2, "pos": "50% 40%"}),
    (21.5, "soft", C, "bottom", {"from": [1.04, 10, 30], "to": [1.16, -20, 0]}, "второй шанс", "IV", {"rot": -1.5}),
    (31.65, "soft", A, "left", face(1.3, 1.7, .33, .27), "рост", "V", {"rot": 1}),
    (42.45, "soft", B, "right", face(1.25, 1.5, .5, .28, pan=(0, 40)), "мир", "VI", {"rot": -1}),
    (51.3, "hard", D, "left", face(1.9, 2.4, .47, .36), "минус", "VII", {"rot": -2.5, "pos": "50% 40%"}),
    (62.9, "soft", C, "bottom", face(1.15, 1.5, .55, .42), "фанаты", "VIII", {"rot": 1.5}),
    (73.8, "soft", B, "top", face(1.2, 1.75, .55, .24), "взросление", "IX", {"rot": -1}),
]
OVER = 0.35  # outgoing card lingers under the incoming one
scenes = []
for i, (st, mode, img, enter, kb, tag, num, extra) in enumerate(S):
    nxt = S[i + 1][0] if i + 1 < len(S) else DUR
    sc = {"start": st, "end": min(DUR, nxt + (OVER if i + 1 < len(S) else 0)), "mode": mode, "img": img,
          "enter": enter, "kb": kb, "tag": tag, "num": num, "exit": "fade" if mode == "soft" else None}
    sc.update(extra)
    if sc["exit"] is None:
        del sc["exit"]
    scenes.append(sc)


def mode_at(t):
    m = "soft"
    for s in S:
        if t >= s[0] - 0.05:
            m = s[1]
    return m


# subtitle chunks: break after punctuation, cap by characters / words
lines, cur = [], []
for k, w in enumerate(words):
    cur.append(w)
    m = mode_at(cur[0]["s"])
    cap = 18 if m == "hard" else 24
    chars = sum(len(x["w"]) + 1 for x in cur)
    nxt = words[k + 1] if k + 1 < len(words) else None
    brk = (re.search(r"[.,?!…:—»]$", w["w"]) and chars > 6) or len(cur) >= (3 if m == "hard" else 4)
    if nxt and chars + len(nxt["w"]) > cap:
        brk = True
    if nxt and mode_at(nxt["s"]) != m:
        brk = True
    if nxt and nxt["s"] - w["e"] > 0.6:
        brk = True
    STOP = {"в", "и", "не", "про", "о", "с", "к", "а", "но", "на", "из-за", "эту", "свою", "всей", "его", "как", "что", "это", "одна", "самых", "очень", "либо"}
    if brk and nxt and mode_at(nxt["s"]) == m and w["w"].lower() in STOP and len(cur) > 1:
        cur.pop()
        lines.append({"mode": m, "words": cur})
        cur = [w]
        continue
    if brk or not nxt:
        lines.append({"mode": m, "words": cur})
        cur = []
for i, L in enumerate(lines):
    L["start"] = L["words"][0]["s"] - 0.06
    nxt = lines[i + 1]["words"][0]["s"] - 0.1 if i + 1 < len(lines) else DUR
    L["end"] = min(nxt, L["words"][-1]["e"] + 0.5)
    if L["mode"] == "hard":
        for w in L["words"]:
            w["w"] = w["w"].rstrip(",")

json.dump({"duration": DUR, "fps": en["fps"], "energy": en["energy"], "onset": en["onset"],
           "scenes": scenes, "lines": lines}, open("work/data.json", "w"), ensure_ascii=False)
for L in lines:
    print(f"{L['start']:6.2f} {L['mode']:4} {' '.join(w['w'] for w in L['words'])}")
