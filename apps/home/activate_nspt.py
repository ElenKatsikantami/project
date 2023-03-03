from python_ags4 import AGS4
import pandas as pd
import numpy as np
import re
import math
def get_machines(x):
    objects = re.findall("\(\S+\)",x)
    if len(objects)==0:
        return [x]
    else:
        return [i[1:-1] for i in objects ]
def get_CN(x,method): 
    conventer = 107.25177991111
    if method =="Peck" :
        nc = 0.77 * math.log(20*conventer/x)
    elif method =="Seed" :
        nc = 1- 0.25*math.log(x/conventer)
    elif method =="Liao" :
        nc = (conventer/x)**0.5
    elif method =="Skempton":
        nc = 200 / (100+x)
    return min(2,nc)
    # 300 / (200+x)
    # 170 / (70+x)
def get_CR(x):
        if x <= 4:
            return 0.75
        elif x <= 6:
            return 0.85
        elif x <= 10:
            return 0.95
        else:
            return 1    
def get_Total_Unit_Weight(x):
    if x >= 50:
        return 20
    elif x <= 15:
        return 18
    else:
        return 19    
def first_correction(ispt_sheet):
    df_ispt = ispt_sheet
    if df_ispt["ISPT_NVAL"].dtype == "O":
        df_ispt["ISPT_NVAL"][~df_ispt["ISPT_NVAL"].str.isalnum()] = \
        df_ispt["ISPT_NVAL"][~df_ispt["ISPT_NVAL"].str.isalnum()].apply(lambda x: x.split("/")[0]).copy()
        df_ispt["ISPT_NVAL"]=pd.to_numeric(df_ispt["ISPT_NVAL"])
    df_ispt["sum"]=df_ispt[["ISPT_PEN3","ISPT_PEN4","ISPT_PEN5","ISPT_PEN6"]].sum(axis=1).replace(0,300)
    df_ispt["corrected"] = list(map(lambda x,y:120 if (x*300/y)>=120 else int(np.ceil((x*300/y))),df_ispt["ISPT_NVAL"],df_ispt["sum"]))
    df_ispt["ISPT_NVAL"]= list(map(lambda x,y:y if x==50 else x,df_ispt["ISPT_NVAL"],df_ispt["corrected"]))
    return  df_ispt

def activate_nspt(file_ags,Efficiency_file,cs,method):
    file_ags_name = file_ags.split("\\")[-1]
    tables, headings = AGS4.AGS4_to_dataframe(file_ags)
    if "ISPT_(N1)60" in headings["ISPT"]:
        return f"NSPT is already activated for {file_ags_name}"
    df_ispt = first_correction(tables["ISPT"][2:].copy())

    try:
        df_efficiency = pd.read_excel(Efficiency_file).dropna()
        dictionery ={i:j for i,j in zip(df_efficiency.iloc[:,0] ,np.round(df_efficiency.iloc[:,1]*(100 if df_efficiency.iloc[:,1][0]<1 else 1),1)) }
    except:
        dictionery = {}
    machines=[]
    for i in list(map(lambda x :get_machines(x),tables["HDPH"]["HDPH_EXC"][2:].replace(np.nan,"").unique())):
        machines.extend(i)
    for i in machines:
        if i not in dictionery:
            Efficiency = 60
            dictionery[i]= Efficiency 
            
    elevations = [i for i in tables["LOCA"].columns if i in ["LOCA_GL","LOCA_LOCZ"]]
    df = tables["LOCA"][2:][elevations+["LOCA_ID"]].replace("",np.nan).dropna(axis=1)
    elevation = [i for i in df.columns if i in ["LOCA_GL","LOCA_LOCZ"]][0]
    df = df[["LOCA_ID"]+[elevation]]
    df[elevation] = df[elevation].apply(float)
    groundWater_sheet = [i for i in tables.keys() if i in ["WSTG","MOND","WSTK"]][0]
    groundWater_dict = {"WSTG":"WSTG_DPTH","MOND":"MOND_RDNG","WSTK":"WSTK_DEP"}
    groundWater_column = groundWater_dict[groundWater_sheet]
    df["water"] = tables[groundWater_sheet][groundWater_column][2:].apply(float)
    df["machines"] = tables["HDPH"]["HDPH_EXC"]
    df["efficency"] = df["machines"].replace(np.nan,"").apply(lambda x :min([dictionery[i] for i in get_machines(x)])) 
    df=df.set_axis(df["LOCA_ID"])

    df_Interpretation = df_ispt.copy()[["LOCA_ID","ISPT_TOP","ISPT_NVAL"]]
    df_Interpretation["ISPT_TOP"] = df_Interpretation["ISPT_TOP"].apply(float)
    df_Interpretation=df_Interpretation.set_axis(df_Interpretation["LOCA_ID"])
    df_Interpretation["EGL"] = df[elevation]
    df_Interpretation["water"] = df["water"]
    df_Interpretation["GWL"] = df_Interpretation["EGL"]-df_Interpretation["water"]
    df_Interpretation["Elevation"] = df_Interpretation["EGL"]-df_Interpretation["ISPT_TOP"]
    df_Interpretation["Total Unit Weight"] = df_Interpretation["ISPT_NVAL"].apply(get_Total_Unit_Weight)
    df_Interpretation["Effective"] = df_Interpretation["Total Unit Weight"] - 10*(df_Interpretation["Elevation"]< df_Interpretation["GWL"]).apply(int)
    df_Interpretation["Effective Overburden Pressure, s'v0"] = df_Interpretation["Effective"]*df_Interpretation["ISPT_TOP"]
    Effective_all = df_Interpretation["Effective Overburden Pressure, s'v0"]
    Effective_modified = []
    for i in df_Interpretation.index.unique():
        Effective_modified.extend( list(map(lambda x,y:(x+y)/2,Effective_all.loc[i]
            ,Effective_all.loc[i][1:].append(pd.Series(Effective_all.loc[i][-1])))) )
    df_Interpretation[" "] = Effective_modified
    df_Interpretation["CN"] = df_Interpretation[" "].apply(get_CN , method =method)

    df_Interpretation["Efficiency"] = df["efficency"]        

    df_Interpretation["CS"] = cs
    diameter = int(tables['CORE']["CORE_DIAM"][3])
    if 115 >= diameter >= 65:
        df_Interpretation["CB"] = 1.0
    elif  65 < diameter <= 150:
        df_Interpretation["CB"] = 1.05
    else:
        df_Interpretation["CB"] = 1.15
    df_Interpretation["CR"] = df_Interpretation["ISPT_TOP"].apply(get_CR)

    df_Interpretation["N60"] = (df_Interpretation["Efficiency"]/60)*df_Interpretation["CB"]*\
                                df_Interpretation["CS"]*df_Interpretation["CR"]*df_Interpretation["ISPT_NVAL"]
    condition = (df_Interpretation["ISPT_TOP"] <= 5).apply(int)
    df_Interpretation["(N1)60"] = np.round(df_Interpretation["N60"]*condition + df_Interpretation["N60"]*df_Interpretation["CN"]*(1-condition), decimals=1)

    tables["ISPT"]["ISPT_(N1)60"] = np.concatenate((tables["ISPT"]["ISPT_NVAL"][:2],df_Interpretation["(N1)60"]))
    
    headings["ISPT"].append("ISPT_(N1)60")
    AGS4.dataframe_to_AGS4(tables, headings,file_ags)
    
    return f"NSPT activated for {file_ags_name}"