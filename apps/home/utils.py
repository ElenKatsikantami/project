import re
import pyproj
import pandas as pd
import numpy as np
from . ags_reference import ags_reference


class util:
    """ags class to process ags files"""

    def __init__(self, tables):
        """class initialization"""
        self.tables = tables
        self.heading_to_remove = ["TYPE", "UNIT"]
        
    def _get_reference(self,variable):
        """Get variable reference"""
        try:
            variable_ref = ags_reference.get(variable,None)
            if variable_ref:
                return variable_ref
            else:
                return False
        except Exception as exp:
            print(str(exp))
    
    def get_geojson(self, loca, ags, proj_code_to_wgs, holetable, geojson):
        """get the geojson"""
        coordinate_fields = ["LOCA_LOCX",
                             "LOCA_LOCY", "HOLE_LOCX", "HOLE_LOCY"]
        try:
            coordinates_columns = [
                i for i in loca.columns if i in coordinate_fields]
            for heading in self.heading_to_remove:
                loca = loca[loca["HEADING"] != heading]
            loca = loca[(loca[coordinates_columns[0]].str.len() != 0)]
            loca["latitude"], loca["longitude"] = proj_code_to_wgs.transform(pd.to_numeric(
                loca[coordinates_columns[0]]), pd.to_numeric(loca[coordinates_columns[1]]))
            for _, row in loca.iterrows():
                hole_dict = {}
                feature = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [row['longitude'], row['latitude']]}, "properties": {
                    "id": row['LOCA_ID'], "lat": round(float(row['latitude']), 4), "lon": round(float(row['longitude']), 4)}}
                geojson['features'].append(feature)
                hole_dict['ags'] = ags.ags_file.name.split(
                    '/')[-1].split('_')[0]
                hole_dict['LOCA_ID'] = row['LOCA_ID']
                hole_dict['longitude'] = round(float(row['longitude']), 4)
                hole_dict['latitude'] = round(float(row['latitude']), 4)
                hole_dict['LOCA_TYPE'] = row['LOCA_TYPE']
                holetable.append(hole_dict)
        except Exception as exp:
            print(str(exp))
        return True

    def get_NSPT(self):
        """get the NSPT"""
        nspt_data, nspt_value = {}, []
        try:
            elevations = re.findall("\w+_LOCZ|\w+_GL", " ".join(self.tables['LOCA'].columns))
            df_ispt = self.tables['ISPT']
            for heading in self.heading_to_remove:
                df_ispt = df_ispt[df_ispt["HEADING"] != heading]
            for column in df_ispt.columns:
                df_ispt[column] = pd.to_numeric(
                    df_ispt[column], errors='ignore')
            if df_ispt["ISPT_NVAL"].dtype == "O":
                df_ispt["ISPT_NVAL"][~df_ispt["ISPT_NVAL"].str.isalnum()] = \
                    df_ispt["ISPT_NVAL"][~df_ispt["ISPT_NVAL"].str.isalnum()].apply(
                    lambda x: x.split("/")[0]).copy()
            df_ispt["ISPT_NVAL"] = pd.to_numeric(df_ispt["ISPT_NVAL"])
            df_ispt["sum"] = df_ispt[["ISPT_PEN3", "ISPT_PEN4",
                                          "ISPT_PEN5", "ISPT_PEN6"]].sum(axis=1).replace(0, 300)
            df_ispt["corrected"] = list(map(lambda x, y: 120 if (
                    x*300/y) >= 120 else int(np.ceil((x*300/y))), df_ispt["ISPT_NVAL"], df_ispt["sum"]))
            df_ispt["ISPT_NVAL"] = list(
                    map(lambda x, y: y if x == 50 else x, df_ispt["ISPT_NVAL"], df_ispt["corrected"]))
            df_interpretation = df_ispt.copy(
                )[["LOCA_ID", "ISPT_TOP", "ISPT_NVAL", "ISPT_TYPE"]]
            loca_copy = self.tables['LOCA'].copy()[["LOCA_ID"]+[elevations[1]]]
            df_merg = df_interpretation.merge(
                    loca_copy, on='LOCA_ID', how='left')
            for column in df_merg.columns:
                df_merg[column] = pd.to_numeric(
                        df_merg[column], errors='ignore')
            df_merg["Elevation"] = df_merg["LOCA_LOCZ"]-df_merg["ISPT_TOP"]
            loca_ids = df_merg.LOCA_ID.unique().tolist()
            for lid in loca_ids:
                nspt_value_outer = []
                for _, row in df_merg[df_merg['LOCA_ID'] == lid].iterrows():
                    nspt_value_inner = []
                    nspt_value_inner.append(round(row["ISPT_NVAL"],4))
                    nspt_value_inner.append(round(row["Elevation"],4))
                    nspt_value_outer.append(nspt_value_inner)
                nspt_value.append(nspt_value_outer)
            nspt_data['value'] = nspt_value
            nspt_data['category'] = loca_ids
        except Exception as exp:
            print(str(exp))
        return nspt_data

    def get_EMOD(self):
        """get the NSPT"""
        nspt_data, nspt_value = {}, []
        try:
            elevations = re.findall("\w+_LOCZ|\w+_GL", " ".join(self.tables['LOCA'].columns))
            df_ispt = self.tables['ISPT']
            for heading in self.heading_to_remove:
                df_ispt = df_ispt[df_ispt["HEADING"] != heading]
            for column in df_ispt.columns:
                df_ispt[column] = pd.to_numeric(
                    df_ispt[column], errors='ignore')
            if df_ispt["ISPT_NVAL"].dtype == "O":
                df_ispt["ISPT_NVAL"][~df_ispt["ISPT_NVAL"].str.isalnum()] = \
                    df_ispt["ISPT_NVAL"][~df_ispt["ISPT_NVAL"].str.isalnum()].apply(
                    lambda x: x.split("/")[0]).copy()
            df_ispt["ISPT_NVAL"] = pd.to_numeric(df_ispt["ISPT_NVAL"])
            df_ispt["sum"] = df_ispt[["ISPT_PEN3", "ISPT_PEN4",
                                          "ISPT_PEN5", "ISPT_PEN6"]].sum(axis=1).replace(0, 300)
            df_ispt["corrected"] = list(map(lambda x, y: 120 if (
                    x*300/y) >= 120 else int(np.ceil((x*300/y))), df_ispt["ISPT_NVAL"], df_ispt["sum"]))
            df_ispt["ISPT_NVAL"] = list(
                    map(lambda x, y: y if x == 50 else x, df_ispt["ISPT_NVAL"], df_ispt["corrected"]))
            df_interpretation = df_ispt.copy(
                )[["LOCA_ID", "ISPT_TOP", "ISPT_NVAL", "ISPT_TYPE"]]
            loca_copy = self.tables['LOCA'].copy()[["LOCA_ID"]+[elevations[1]]]
            df_merg = df_interpretation.merge(
                    loca_copy, on='LOCA_ID', how='left')
            for column in df_merg.columns:
                df_merg[column] = pd.to_numeric(
                        df_merg[column], errors='ignore')
            df_merg["Elevation"] = df_merg["LOCA_LOCZ"]-df_merg["ISPT_TOP"]
            loca_ids = df_merg.LOCA_ID.unique().tolist()
            for lid in loca_ids:
                nspt_value_outer = []
                for _, row in df_merg[df_merg['LOCA_ID'] == lid].iterrows():
                    nspt_value_inner = []
                    nspt_value_inner.append(round(1.5*row["ISPT_NVAL"],4))
                    nspt_value_inner.append(round(row["Elevation"],4))
                    nspt_value_outer.append(nspt_value_inner)
                nspt_value.append(nspt_value_outer)
            nspt_data['value'] = nspt_value
            nspt_data['category'] = loca_ids
        except Exception as exp:
            print(str(exp))
        return nspt_data

    def get_Friction_Angle(self):
        """get the NSPT"""
        nspt_data, nspt_value = {}, []
        try:
            elevations = re.findall("\w+_LOCZ|\w+_GL", " ".join(self.tables['LOCA'].columns))
            df_ispt = self.tables['ISPT']
            for heading in self.heading_to_remove:
                df_ispt = df_ispt[df_ispt["HEADING"] != heading]
            for column in df_ispt.columns:
                df_ispt[column] = pd.to_numeric(
                    df_ispt[column], errors='ignore')
            if df_ispt["ISPT_NVAL"].dtype == "O":
                df_ispt["ISPT_NVAL"][~df_ispt["ISPT_NVAL"].str.isalnum()] = \
                    df_ispt["ISPT_NVAL"][~df_ispt["ISPT_NVAL"].str.isalnum()].apply(
                    lambda x: x.split("/")[0]).copy()
            df_ispt["ISPT_NVAL"] = pd.to_numeric(df_ispt["ISPT_NVAL"])
            df_ispt["sum"] = df_ispt[["ISPT_PEN3", "ISPT_PEN4",
                                          "ISPT_PEN5", "ISPT_PEN6"]].sum(axis=1).replace(0, 300)
            df_ispt["corrected"] = list(map(lambda x, y: 120 if (
                    x*300/y) >= 120 else int(np.ceil((x*300/y))), df_ispt["ISPT_NVAL"], df_ispt["sum"]))
            df_ispt["ISPT_NVAL"] = list(
                    map(lambda x, y: y if x == 50 else x, df_ispt["ISPT_NVAL"], df_ispt["corrected"]))
            df_interpretation = df_ispt.copy(
                )[["LOCA_ID", "ISPT_TOP", "ISPT_NVAL", "ISPT_TYPE"]]
            loca_copy = self.tables['LOCA'].copy()[["LOCA_ID"]+[elevations[1]]]
            df_merg = df_interpretation.merge(
                    loca_copy, on='LOCA_ID', how='left')
            for column in df_merg.columns:
                df_merg[column] = pd.to_numeric(
                        df_merg[column], errors='ignore')
            df_merg["Elevation"] = df_merg["LOCA_LOCZ"]-df_merg["ISPT_TOP"]
            loca_ids = df_merg.LOCA_ID.unique().tolist()
            for lid in loca_ids:
                nspt_value_outer = []
                for _, row in df_merg[df_merg['LOCA_ID'] == lid].iterrows():
                    nspt_value_inner = []
                    friction_angle = np.floor(27.1+(0.3*row["ISPT_NVAL"])-(0.00054*(row["ISPT_NVAL"]**2)))
                    nspt_value_inner.append(round(friction_angle,4))
                    nspt_value_inner.append(round(row["Elevation"],4))
                    nspt_value_outer.append(nspt_value_inner)
                nspt_value.append(nspt_value_outer)
            nspt_data['value'] = nspt_value
            nspt_data['category'] = loca_ids
        except Exception as exp:
            print(str(exp))
        return nspt_data

    def _get_elevation(self):
        """get the elevation"""
        try:
            elevations = re.findall("\w+_LOCZ|\w+_GL", " ".join(self.tables['LOCA'].columns))
            loca_copy = self.tables['LOCA'].copy()[["LOCA_ID"]+[elevations[1]]]
        except Exception as exp:
            print(str(exp))
        return loca_copy

    def get_factual_chart_data(self,variable_one, variable_two='Elevation'):
        """get the chart data for factual"""
        data, value = {}, []
        possible_value = ['_DEPT','_BASE','_TOP']
        null_values = ['NP','np']
        try:
            v_ref = self._get_reference(variable_one)
            if variable_two == "Elevation":
                df_elevation = self._get_elevation()
            data_frame = self.tables[v_ref['heading']]
            req_column_list = ["LOCA_ID",v_ref['column']]
            for req_column in data_frame.columns:
                if any(x in req_column for x in possible_value):
                    req_column_list.append(req_column)
            for heading in self.heading_to_remove:
                data_frame = data_frame[data_frame["HEADING"] != heading]
            for col in data_frame.columns:
                data_frame[col] = pd.to_numeric(
                    data_frame[col], errors='ignore')
            if data_frame[v_ref['column']].dtype == "O":
                data_frame[v_ref['column']][~data_frame[v_ref['column']].str.isalnum()] = \
                    data_frame[v_ref['column']][~data_frame[v_ref['column']].str.isalnum()].apply(
                    lambda x: x.split("/")[0]).copy()
            df_interpretation = data_frame.copy()[req_column_list]
            df_interpretation = df_interpretation[(df_interpretation[v_ref['column']].astype(str).str.contains('|'.join(null_values))==False)]
            df_interpretation[v_ref['column']] = df_interpretation[v_ref['column']].astype(str).str.replace('\W', '', regex=True)
            df_merg = df_interpretation.merge(
                    df_elevation, on='LOCA_ID', how='left')
            loca_ids = df_merg.LOCA_ID.unique().tolist()
            for column in df_merg.columns:
                if column in [v_ref['column'],'LOCA_LOCZ']:
                    df_merg[column] = pd.to_numeric(df_merg[column], errors='coerce')
            df_merg = df_merg.dropna()
            depth = None
            print(df_merg)
            for req_column in df_merg.columns:
                if possible_value[0] in req_column:
                    print('dept')
                    depth = req_column
                    break
                elif possible_value[2] in req_column:
                    print('top')
                    base = [color for color in df_merg.columns if possible_value[1] in color]
                    if base:
                        depth = [req_column,base[0]]
                    else:
                        depth = req_column
            if depth:
                if isinstance(depth,list):
                    print('mean')
                    df_merg["mean"] = df_merg[depth].mean(axis=1)
                    df_merg["Elevation"] = df_merg["LOCA_LOCZ"]-df_merg["mean"]
                else:
                    df_merg["Elevation"] = df_merg["LOCA_LOCZ"]-df_merg[depth]
            else:
                df_merg["Elevation"] = df_merg["LOCA_LOCZ"]
            # print(df_merg)
            for lid in loca_ids:
                value_outer = []
                for _, row in df_merg[df_merg['LOCA_ID'] == lid].iterrows():
                    value_inner = []
                    value_inner.append(round(row[v_ref['column']],4))
                    value_inner.append(round(row["Elevation"],4))
                    value_outer.append(value_inner)
                value.append(value_outer)
            data['value'] = value
            data['category'] = loca_ids
        except Exception as exp:
            print('error')
            print(str(exp))
        return data

    def get_chart_list_base_on_ags(self,headings):
        """Filter out the chart variable base on ags"""
        chart_heading = []
        try:
            for chart_variable in [*ags_reference]:
                chart_heading.append(ags_reference[chart_variable]['heading'])
            column_list = [x for x in chart_heading if x in headings]
            variable_list = [x for x in [*ags_reference]if ags_reference[x]['heading'] in column_list]
        except Exception as exp:
            print(str(exp))
        return variable_list
