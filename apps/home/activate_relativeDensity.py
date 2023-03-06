from python_ags4 import AGS4
import pandas as pd
import numpy as np

def get_dr_Terzaghi(x):
    if x <= 4 :
        y = 15 * x / 4
        classification = "Very Loose"
    elif x <= 10:
        y = 15 + 20 * (x-4) / 6
        classification = "Loose"
    elif x <= 30:
        y = 35 + 30 * (x-10) / 20
        classification = "Medium"
        
    elif x <= 50:
        y = 65 + 20 * (x-30) / 20
        classification = "Dense"
    else:
        y = 85 + 15 * (x-50) / 50
        classification = "Very Dense"
    return pd.Series([y ,classification])

def get_dr_Skempton(x):
    return (x/60)**0.5

def first_correction(ispt_sheet):
    df_ispt = ispt_sheet
    for column in df_ispt.columns:
        df_ispt[column] = pd.to_numeric(df_ispt[column],errors='ignore')
    if df_ispt["ISPT_NVAL"].dtype == "O":
        df_ispt["ISPT_NVAL"][~df_ispt["ISPT_NVAL"].str.isalnum()] = \
        df_ispt["ISPT_NVAL"][~df_ispt["ISPT_NVAL"].str.isalnum()].apply(lambda x: x.split("/")[0]).copy()
        df_ispt["ISPT_NVAL"]=pd.to_numeric(df_ispt["ISPT_NVAL"])
    df_ispt["sum"]=df_ispt[["ISPT_PEN3","ISPT_PEN4","ISPT_PEN5","ISPT_PEN6"]].sum(axis=1).replace(0,300)
    df_ispt["corrected"] = list(map(lambda x,y:120 if (x*300/y)>=120 else int(np.ceil((x*300/y))),df_ispt["ISPT_NVAL"],df_ispt["sum"]))
    df_ispt["ISPT_NVAL"]= list(map(lambda x,y:y if x==50 else x,df_ispt["ISPT_NVAL"],df_ispt["corrected"]))
    return  df_ispt



def activateRelativeDensity(file_ags,method):
    file_ags_name = file_ags.split("\\")[-1]
    tables, headings = AGS4.AGS4_to_dataframe(file_ags)
    df_ispt = first_correction(tables["ISPT"][2:].copy())
    if method == "Terzaghi":
        if "ISPT_dr_Terzaghi" in headings["ISPT"] :
            return f"Relative Density is already activated for {file_ags_name} by Terzaghi and Peck method"
        df = df_ispt["ISPT_NVAL"].apply(get_dr_Terzaghi)
        tables["ISPT"]["ISPT_dr_Terzaghi"] = pd.Series(["",""]).append(df[0])
        tables["ISPT"]["ISPT_classifications"] = pd.Series(["",""]).append(df[1])
        headings["ISPT"].append("ISPT_dr_Terzaghi")
        headings["ISPT"].append("ISPT_classifications")
        AGS4.dataframe_to_AGS4(tables, headings,file_ags)
        return f"Relative Density activated for {file_ags_name} by Terzaghi and Peck method"
    if method == "Skempton":
        if "ISPT_dr_Skempton" in headings["ISPT"] :
            return f"Relative Density is already activated for {file_ags_name} by Skempton method"
        if "ISPT_(N1)60" not in headings["ISPT"]:
            return "NSPT must be activated first"
        dr = df_ispt["ISPT_(N1)60"].apply(get_dr_Skempton)
        tables["ISPT"]["ISPT_dr_Skempton"] = pd.Series(["",""]).append(dr)
        headings["ISPT"].append("ISPT_dr_Skempton")
        AGS4.dataframe_to_AGS4(tables, headings,file_ags)
        return f"Relative Density activated for {file_ags_name} by Skempton method"
    else :
        if ("ISPT_dr_Terzaghi" in headings["ISPT"] 
            and "ISPT_dr_Skempton" in headings["ISPT"] ):
            return f"Relative Density is already activated for {file_ags_name} by both methods"
        df = df_ispt["ISPT_NVAL"].apply(get_dr_Terzaghi)
        tables["ISPT"]["ISPT_dr_Terzaghi"] = pd.Series(["",""]).append(df[0])
        tables["ISPT"]["ISPT_classifications"] = pd.Series(["",""]).append(df[1])
        headings["ISPT"].append("ISPT_dr_Terzaghi")
        headings["ISPT"].append("ISPT_classifications")
        if "ISPT_(N1)60" not in headings["ISPT"]:
            return f"""NSPT must be activated first
                    Relative Density activated for {file_ags_name} by Terzaghi and Peck method only"""
        dr = df_ispt["ISPT_(N1)60"].apply(get_dr_Skempton)
        tables["ISPT"]["ISPT_dr_Skempton"] = pd.Series(["",""]).append(dr)
        headings["ISPT"].append("ISPT_dr_Skempton")
        AGS4.dataframe_to_AGS4(tables, headings,file_ags)
        return f"Relative Density activated for {file_ags_name} by both methods"