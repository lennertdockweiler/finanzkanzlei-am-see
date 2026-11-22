"""Statische QA: Links, Anker, h1, Meta, Inline-Styles, Platzhalter."""
import re, sys, os
from html.parser import HTMLParser
from collections import Counter

root = sys.argv[1]
pages = sorted(f for f in os.listdir(root) if f.endswith(".html"))

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=set(); self.links=[]; self.h1=0; self.imgs_noalt=0; self.style=0; self.title=""; self.desc=False; self._t=False; self.heads=[]
    def handle_starttag(self, t, a):
        a=dict(a)
        if "id" in a: self.ids.add(a["id"])
        if t=="a" and "href" in a: self.links.append(a["href"])
        if t in ("link","script","img") and (a.get("href") or a.get("src")): self.links.append(a.get("href") or a.get("src"))
        if t=="h1": self.h1+=1
        if re.fullmatch(r"h[1-6]", t): self.heads.append(int(t[1]))
        if t=="img" and "alt" not in a: self.imgs_noalt+=1
        if "style" in a and t!="body": self.style+=1
        if t=="title": self._t=True
        if t=="meta" and a.get("name")=="description": self.desc=True
    def handle_endtag(self,t):
        if t=="title": self._t=False
    def handle_data(self,d):
        if self._t: self.title+=d

parsed={}
for p in pages:
    x=P(); x.feed(open(os.path.join(root,p),encoding="utf-8").read()); parsed[p]=x

problems=[]
titles=Counter(x.title for x in parsed.values())
for p,x in parsed.items():
    if x.h1!=1: problems.append(f"{p}: {x.h1} h1")
    if not x.desc: problems.append(f"{p}: keine meta description")
    if titles[x.title]>1: problems.append(f"{p}: Titel doppelt")
    if x.imgs_noalt: problems.append(f"{p}: img ohne alt")
    if x.style: problems.append(f"{p}: {x.style} Inline-Styles")
    # Überschriftensprünge
    for a,b in zip(x.heads,x.heads[1:]):
        if b>a+1: problems.append(f"{p}: Überschriftensprung h{a}->h{b}"); break
    for l in x.links:
        if re.match(r"(https?:|mailto:|tel:|data:)", l): continue
        path,_,frag=l.partition("#"); path=path.split("?")[0].lstrip("/")
        target=path or p
        if path and not os.path.exists(os.path.join(root,path)):
            problems.append(f"{p}: toter Link {l}"); continue
        if frag and target.endswith(".html") and frag not in parsed[target].ids:
            problems.append(f"{p}: Anker fehlt {l}")

print("\n".join(sorted(set(problems))) or "keine Probleme")
# Platzhalter sammeln
ph=Counter()
for dp,_,fs in os.walk(root):
    for f in fs:
        if f.endswith((".html",".css",".js")):
            for m in re.findall(r"\[\[ERSETZEN:[^\]]*\]\]", open(os.path.join(dp,f),encoding="utf-8").read()):
                ph[(f,m)]+=1
print("\nPLATZHALTER:")
for (f,m),n in sorted(ph.items()): print(f"{f} ×{n}: {m}")
