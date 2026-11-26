import pandas as pd
df=pd.read_csv("features.csv")
s=pd.read_csv("attack_schedule.csv")
s["ts"]=pd.to_datetime(s["timestamp"],utc=True).astype("int64")//10**9
df["label"]="normal"
starts=s[s.event=="START"].reset_index(drop=True)
ends=s[s.event=="END"].reset_index(drop=True)
for i in range(len(starts)):
    a,b,typ=starts.loc[i,"ts"],ends.loc[i,"ts"],starts.loc[i,"type"]
    df.loc[(df.timestamp>=a)&(df.timestamp<=b),"label"]=typ
df.to_csv("dataset.csv",index=False)
print("=== Répartition des classes ===")
print(df.label.value_counts())
