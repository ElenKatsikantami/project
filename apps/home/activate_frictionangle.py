from python_ags4 import AGS4
import pandas as pd
import numpy as np

def round_up(n, decimals=0): 
    multiplier = 10 ** decimals 
    return np.ceil(n * multiplier) / multiplier

def apply_first(x):
    if 0<=x<60:
        return  (27.1 + 0.3*x + 0.00054*(x**2))//0.1/10
    elif x>=60:
        return  (20*(x**0.18)+5.2)//0.1/10

def apply_second(x):
    if 0<=x<60:
        return (-0.0014*x**2 + 0.3534*x + 26.964)//0.1/10
    elif x>=60:
        return  (10.687*np.log(x)-0.6255)//0.1/10

def apply_third(x):
    if 0<=x<60:
        Coarse = 0.00002*x**3 - 0.0056*x**2 + 0.583*x + 27.558
    elif x>=60:
        Coarse = 9.3873*np.log(x)+8.2633
    if 0<=x<60:
        Fine = -0.00002*x**3 - 0.0015*x**2 + 0.4089*x + 27.395
    elif x>=60:
        Fine = 4*np.log(x)+25.83

    y = round_up(( Coarse + Fine)/2,1)
    return y


def apply_forth(x):
    if 0  <= x <= 1:
        return (25+x)//0.1/10
    elif x > 1 :
        return (24.22573*(x**0.1547204))//0.1/10
    
def apply_fifth(x):
    return ((12*x)**0.5 + 20)//0.1/10

def first_correction(ispt_sheet):
    df_ispt = ispt_sheet
    if df_ispt["ISPT_NVAL"].dtype == "O":
        df_ispt["ISPT_NVAL"][~df_ispt["ISPT_NVAL"].str.isalnum()] = \
        df_ispt["ISPT_NVAL"][~df_ispt["ISPT_NVAL"].str.isalnum()].apply(lambda x: x.split("/")[0]).copy()
        df_ispt["ISPT_NVAL"]=pd.to_numeric(df_ispt["ISPT_NVAL"])
    return  df_ispt["ISPT_NVAL"]



def activate_frictionangle(file_ags,method):
    tables, headings = AGS4.AGS4_to_dataframe(file_ags)
    
    if "ISPT_correctedN" in headings["ISPT"] :
        Nspt = pd.to_numeric(tables["ISPT"]["ISPT_correctedN"][2:])
    else:
        Nspt = first_correction(tables["ISPT"][2:].copy())
        
    if method == "1":
        if "ISPT_(N1)60" not in headings["ISPT"]:
            return "NSPT must be activated first"
        N_60 = pd.to_numeric(tables["ISPT"]["ISPT_(N1)60"][2:])
        FractionAngle = N_60.apply(apply_first)
    elif method == "2":
        FractionAngle = Nspt.apply(apply_second)
    elif method == "3":
        if "ISPT_(N1)60" not in headings["ISPT"]:
            return "NSPT must be activated first"
        N_60 = pd.to_numeric(tables["ISPT"]["ISPT_(N1)60"][2:])
        FractionAngle = N_60.apply(apply_third)
    elif method == "4":
        FractionAngle = Nspt.apply(apply_forth)
    elif method == "5":
        FractionAngle = Nspt.apply(apply_fifth)
        
    
    tables["ISPT"]["ISPT_FractionAngle"] = pd.Series(["",""]).append(FractionAngle) 
    if "ISPT_FractionAngle" not in headings["ISPT"] :
        case = 1
        headings["ISPT"].append("ISPT_FractionAngle")
    else:
        case = 0
    AGS4.dataframe_to_AGS4(tables, headings,file_ags)
    if case:
        return f"Fraction Angle is activated successfully"
    else:
        return f"Fraction Angle is reactivated successfully"