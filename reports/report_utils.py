import os, json, pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def collect_validation_data(tunnels):
    rows=[]
    for t_name,t in tunnels.items():
        for f in os.listdir(t["image_dir"]):
            if f.endswith(".json"):
                d=json.load(open(os.path.join(t["image_dir"],f)))
                rows.append(d)
    return pd.DataFrame(rows)

def generate_excel(df,path="report.xlsx"):
    df.to_excel(path,index=False)
    return path

def generate_pdf(df,path="report.pdf"):
    doc=SimpleDocTemplate(path)
    styles=getSampleStyleSheet()
    content=[]
    for _,r in df.iterrows():
        content.append(Paragraph(str(r.to_dict()), styles["Normal"]))
    doc.build(content)
    return path
