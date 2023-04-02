from python_ags4 import AGS4
import pandas as pd
import numpy as np

def round_up(n, decimals=0): 
    multiplier = 10 ** decimals 
    return np.ceil(n * multiplier) / multiplier

def apply_first(x):
    return  (27.1 + 0.3*x + 0.00054*(x**2))//0.1/10

def apply_second(x):
    return (-0.0014*x**2 + 0.3534*x + 26.964)//0.1/10

def apply_third(x):
    Coarse = 0.00002*x**3 - 0.0056*x**2 + 0.583*x + 27.558
    Fine = -0.00002*x**3 - 0.0015*x**2 + 0.4089*x + 27.395
    y = round_up(( Coarse + Fine)/2,1)
    return y

def apply_sixth(x):
    return ((12*x)**0.5 + 20)//0.1/10

def get_average(x):
    return (apply_first(x) + apply_second(x) + apply_third(x) + apply_sixth(x))/4
    
def apply_forth(x,maximum):
    z= get_average(maximum)
    if x <= 4 :
        y = 25 + 3 * x / 4

    elif x <= 10:
        y = 28 + 2 * (x-4) / 6

    elif x <= 30:
        y = 30 + 6 * (x-10) / 20

    elif x <= 50:
        y = 36 + 5 * (x-30) / 20

    else:
        y = 41 + (z-41)  * (x-50) / (maximum-50)

    return y//0.1/10

def apply_fifth(x,maximum):
    z= get_average(maximum)
    if x <= 4 :
        y = 25 + 5 * x / 4

    elif x <= 10:
        y = 30 + 5 * (x-4) / 6

    elif x <= 30:
        y = 35 + 5 * (x-10) / 20

    elif x <= 50:
        y = 40 + 5 * (x-30) / 20

    else:
        y = 45 + (z-45) * (x-50) / (maximum-50)

    return y//0.1/10



def first_correction(ispt_sheet):
    df_ispt = ispt_sheet
    if df_ispt["ISPT_NVAL"].dtype == "O":
        df_ispt["ISPT_NVAL"][~df_ispt["ISPT_NVAL"].str.isalnum()] = \
        df_ispt["ISPT_NVAL"][~df_ispt["ISPT_NVAL"].str.isalnum()].apply(lambda x: x.split("/")[0]).copy()
        df_ispt["ISPT_NVAL"]=pd.to_numeric(df_ispt["ISPT_NVAL"])
    return  df_ispt["ISPT_NVAL"]



def activate_frictionangle(file_ags,method):
    file_ags_name = file_ags.split("\\")[-1]
    tables, headings = AGS4.AGS4_to_dataframe(file_ags)
    if "ISPT_FractionAngle" in headings["ISPT"] :
        return f"Fraction Angle is already activated for {file_ags_name}"
    if "ISPT_correctedN" in headings["ISPT"] :
        Nspt = pd.to_numeric(tables["ISPT"]["ISPT_correctedN"][2:])
    else:
        Nspt = first_correction(tables["ISPT"][2:].copy())
        
    
    maximum = Nspt.max()
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
        FractionAngle = Nspt.apply(apply_forth,maximum= maximum)
    elif method == "5":
        FractionAngle = Nspt.apply(apply_fifth,maximum= maximum)
    elif method == "6":
        FractionAngle = Nspt.apply(apply_sixth)
        
    
    tables["ISPT"]["ISPT_FractionAngle"] = pd.Series(["",""]).append(FractionAngle)  
    headings["ISPT"].append("ISPT_FractionAngle")
    AGS4.dataframe_to_AGS4(tables, headings,file_ags)
    return f"Fraction Angle activated for {file_ags_name}"