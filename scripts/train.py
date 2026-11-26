import pandas as pd, joblib
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

df=pd.read_csv("dataset.csv")
feats=["qlen","entropy","num_sub","longest_label","is_txt","is_nxdomain","qps","nx_ratio"]
X=df[feats].fillna(0); y=df["label"]

# --- Non supervisé : anomalies (entraîné sur le normal) ---
Xn=df[df.label=="normal"][feats].fillna(0)
iso=IsolationForest(contamination=0.1,random_state=42).fit(Xn)
joblib.dump(iso,"iso.pkl")

# --- Supervisé : classification du type d'attaque ---
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=0.3,stratify=y,random_state=42)
rf=RandomForestClassifier(n_estimators=300,class_weight="balanced",random_state=42).fit(Xtr,ytr)
pred=rf.predict(Xte)
print(classification_report(yte,pred))
print(confusion_matrix(yte,pred))
joblib.dump(rf,"rf.pkl")
print("Modèles sauvegardés : iso.pkl, rf.pkl")
