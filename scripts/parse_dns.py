import json, math, pandas as pd
from collections import Counter

def entropy(s):
    if not s: return 0.0
    c=Counter(s); n=len(s)
    return -sum((v/n)*math.log2(v/n) for v in c.values())

rows=[]
with open("dns.log") as f:
    for line in f:
        line=line.strip()
        if not line or line.startswith("#"): continue
        try: r=json.loads(line)
        except: continue
        q=r.get("query") or ""
        labels=q.split(".")
        rows.append({
            "timestamp": float(r["ts"]),
            "src_ip": r.get("id.orig_h",""),
            "dst_ip": r.get("id.resp_h",""),
            "query": q,
            "qtype": r.get("qtype_name",""),
            "rcode": r.get("rcode_name",""),
            "qlen": len(q),
            "entropy": round(entropy(q),3),
            "num_sub": len(labels),
            "longest_label": max((len(l) for l in labels),default=0),
            "is_txt": int(r.get("qtype_name","")=="TXT"),
            "is_nxdomain": int(r.get("rcode_name","")=="NXDOMAIN"),
        })

df=pd.DataFrame(rows).sort_values("timestamp").reset_index(drop=True)
df["qps"]=df.groupby("src_ip")["timestamp"].transform(
    lambda t: t.rolling(50,min_periods=1).count()/t.diff().rolling(50,min_periods=1).sum().replace(0,1))
df["nx_ratio"]=df.groupby("src_ip")["is_nxdomain"].transform(
    lambda x: x.rolling(50,min_periods=1).mean())
df.to_csv("features.csv",index=False)
print("Lignes:",len(df))
print(df[["query","entropy","qps","is_txt","is_nxdomain"]].head())
