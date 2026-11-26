import pandas as pd, joblib, json, datetime
from collections import defaultdict

rf=joblib.load("rf.pkl"); iso=joblib.load("iso.pkl")
df=pd.read_csv("dataset.csv")
feats=["qlen","entropy","num_sub","longest_label","is_txt","is_nxdomain","qps","nx_ratio"]
X=df[feats].fillna(0)

proba=rf.predict_proba(X); classes=rf.classes_
df["pred"]=classes[proba.argmax(1)]
df["score"]=proba.max(1)
df["anom"]=(iso.predict(X)==-1).astype(int)

# indicateurs (règles métier)
df["ev_entropy"]=(df.entropy>3.8).astype(int)
df["ev_txt"]=(df.is_txt==1).astype(int)
df["ev_qps"]=(df.qps>40).astype(int)
df["ev_nx"]=(df.nx_ratio>0.5).astype(int)
df["ev"]=df[["ev_entropy","ev_txt","ev_qps","ev_nx"]].sum(axis=1)

# 3 critères : RF confiant + anomalie + au moins une règle ; on exige >=2
df["crit"]=(df.score>=0.85).astype(int)+df.anom+(df.ev>=1).astype(int)

cand=df[(df.pred!="normal")&(df.crit>=2)]
print("Candidats (>=2 criteres):",len(cand))

hits=defaultdict(int); seen=set(); final=[]
for _,r in cand.iterrows():
    key=(r.src_ip,r.pred); hits[key]+=1
    if hits[key]<3: continue                 # fenetre de confirmation
    if key in seen: continue                 # 1 entree par (ip,type)
    seen.add(key)
    ev=[]
    if r.ev_entropy: ev.append("entropie elevee")
    if r.ev_txt: ev.append("requetes TXT anormales")
    if r.ev_qps: ev.append("debit de requetes anormal")
    if r.ev_nx: ev.append("ratio NXDOMAIN eleve")
    final.append({
        "timestamp":datetime.datetime.utcfromtimestamp(r.timestamp).isoformat()+"Z",
        "attack_type":r.pred,"source_ip":r.src_ip,"target":r.dst_ip,
        "confidence_score":round(float(r.score),2),
        "evidence":ev or ["classifieur + anomalie concordants"]})

fname=f"log_{datetime.date.today()}_session1.json"
json.dump(final,open(fname,"w"),indent=2,ensure_ascii=False)
print(f"{len(final)} vrais positifs -> {fname}")
