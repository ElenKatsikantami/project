import re
import math
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
            # import pdb; pdb.set_trace() #breakpoint  c n s q l
            coordinates_columns = [
                i for i in loca.columns if i in coordinate_fields]
            for heading in self.heading_to_remove:
                loca = loca[loca["HEADING_x"] != heading]
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
                hole_dict['LOCA_GL'] = row['LOCA_GL']
                hole_dict['MOND_RDNG'] = row['MOND_RDNG']
                holetable.append(hole_dict)
        except Exception as exp:
            print(str(exp))
        return True

    def _get_elevation(self):
        """get the elevation"""
        try:
            elevations = re.findall("\w+_LOCZ|\w+_GL", " ".join(self.tables['LOCA'].columns))
            # import pdb; pdb.set_trace() #breakpoint  c n s q l
            df_loca = self.tables['LOCA']
            df_hdph = self.tables['HDPH']
            df_loca = df_loca.merge(
                    df_hdph, on='LOCA_ID', how='left')
            loca_copy = df_loca.copy()[["LOCA_ID"]+[elevations[1]]+['HDPH_EXC']]
        except Exception as exp:
            print(str(exp))
        return loca_copy

    def _column_max_value(self,nspt):
        std_nval = 100
        try:
            if not nspt[0] or not nspt[1]:
                return nspt[0]
            try:
                nval,npen= int(nspt[0]),int(nspt[1])
            except Exception as exp:
                print(exp)
                return nspt[0]
            if npen == 450:
                return nval
            elif npen < 450:
                nval_update = (nval*300)/abs(npen-150)
                return 100 if nval_update>std_nval or nval_update<0 else int(nval_update)
            else:
                return nval
        except Exception as exp:
            print('error is here')
            print(str(exp))

    def get_factual_chart_data(self,variable_one, variable_two='Elevation', class_type='borehole'):
        """get the chart data for factual"""
        data, value = {}, []
        possible_value = ['_DEPT','_BASE','_TOP']
        null_values = ['NP','np']
        print(class_type)
        try:
            v_ref = self._get_reference(variable_one)
            df_elevation = self._get_elevation()
            data_frame = self.tables[v_ref['heading']]
            column_name = v_ref['column'][-1]
            req_column_list = ["LOCA_ID",column_name]
            for req_column in data_frame.columns:
                if any(x in req_column for x in possible_value):
                    req_column_list.append(req_column)
            for heading in self.heading_to_remove:
                data_frame = data_frame[data_frame["HEADING"] != heading]
            for col in data_frame.columns:
                data_frame[col] = pd.to_numeric(
                    data_frame[col], errors='ignore')
            if variable_one == 'N SPT':
                extra_col = v_ref['column'][0]
                data_frame[column_name] = data_frame[[column_name,extra_col]].apply(self._column_max_value,axis=1)
                print(data_frame[column_name])
            if data_frame[column_name].dtype == "O":
                data_frame[column_name][~data_frame[column_name].str.isalnum()] = \
                    data_frame[column_name][~data_frame[column_name].str.isalnum()].apply(
                    lambda x: x.split("/")[0]).copy()
            df_interpretation = data_frame.copy()[req_column_list] 
            df_interpretation = df_interpretation[(df_interpretation[column_name].astype(str).str.contains('|'.join(null_values))==False)]
            df_merg = df_interpretation.merge(
                    df_elevation, on='LOCA_ID', how='left')
            loca_ids = df_merg.LOCA_ID.unique().tolist()
            for column in df_merg.columns:
                if column in [column_name,'LOCA_LOCZ']:
                    df_merg[column] = pd.to_numeric(df_merg[column], errors='coerce')
            df_merg = df_merg.dropna()
            depth = None
            for req_column in df_merg.columns:
                if possible_value[0] in req_column:
                    depth = req_column
                    break
                elif possible_value[2] in req_column:
                    base = [color for color in df_merg.columns if possible_value[1] in color]
                    if base:
                        depth = [req_column,base[0]]
                    else:
                        depth = req_column
            if depth:
                if variable_two == "Elevation":
                    if isinstance(depth,list):
                        df_merg["mean"] = df_merg[depth].mean(axis=1)
                        df_merg["Elevation"] = df_merg["LOCA_LOCZ"]-df_merg["mean"]
                    else:
                        df_merg["Elevation"] = df_merg["LOCA_LOCZ"]-df_merg[depth]
                if variable_two == "Depth":
                    if isinstance(depth,list):
                        df_merg["mean"] = df_merg[depth].mean(axis=1)
                        df_merg["Elevation"] = df_merg["mean"]
                    else:
                        df_merg["Elevation"] = df_merg[depth]
            else:
                df_merg["Elevation"] = df_merg["LOCA_LOCZ"]
            if class_type == 'machine':
                loca_ids = df_merg.HDPH_EXC.unique().tolist()
                for lid in loca_ids:
                    value_outer = []
                    for _, row in df_merg[df_merg['HDPH_EXC'] == lid].iterrows():
                        value_inner = []
                        value_inner.append(round(row[column_name],4))
                        value_inner.append(round(row["Elevation"],4))
                        value_outer.append(value_inner)
                    value.append(value_outer)
                data['value'] = value
                data['category'] = loca_ids
            elif class_type == 'borehole':
                for lid in loca_ids:
                    value_outer = []
                    for _, row in df_merg[df_merg['LOCA_ID'] == lid].iterrows():
                        value_inner = []
                        value_inner.append(round(row[column_name],4))
                        value_inner.append(round(row["Elevation"],4))
                        value_outer.append(value_inner)
                    value.append(value_outer)
                data['value'] = value
                data['category'] = loca_ids
            elif class_type == 'boreholeandmachine':
                df_merg['mcahine_type_borehole'] = df_merg['LOCA_ID'].astype(str) +"("+ df_merg["HDPH_EXC"]+")"
                loca_ids = df_merg.mcahine_type_borehole.unique().tolist()
                for lid in loca_ids:
                    value_outer = []
                    for _, row in df_merg[df_merg['mcahine_type_borehole'] == lid].iterrows():
                        value_inner = []
                        value_inner.append(round(row[column_name],4))
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
            variable_list.append('Water Level')
            print(variable_list)
        except Exception as exp:
            print(str(exp))
        return variable_list

    def get_borehole_list_base_on_ags(self):
        """Filter out the ags variable base on ags"""
        try:
            loca_copy = self.tables['LOCA']
            for heading in self.heading_to_remove:
                loca_copy = loca_copy[loca_copy["HEADING"] != heading]
            variable_list = loca_copy.LOCA_ID.unique().tolist()
        except Exception as exp:
            print(str(exp))
        return variable_list

    def get_factual_chart_partical(self,variable_one, LOCA_ID):
        """get the chart data for factual"""
        data = {}
        req_column_list = ["LOCA_ID"]
        try:
            v_ref = self._get_reference(variable_one)
            data_frame = self.tables[v_ref['heading']]
            columns = v_ref['column']
            for column in columns:
                req_column_list.append(column)
            for heading in self.heading_to_remove:
                data_frame = data_frame[data_frame["HEADING"] != heading]
            for col in data_frame.columns:
                data_frame[col] = pd.to_numeric(
                    data_frame[col], errors='ignore')
            for column_name in columns:
                if data_frame[column_name].dtype == "O":
                    data_frame[column_name][~data_frame[column_name].str.isalnum()] = \
                        data_frame[column_name][~data_frame[column_name].str.isalnum()].apply(
                        lambda x: x.split("/")[0]).copy()
            df_merg = data_frame.copy()[req_column_list]
            df_merg = df_merg.loc[df_merg['LOCA_ID'] == LOCA_ID]
            for column in df_merg.columns:
                if column in columns:
                    df_merg[column] = pd.to_numeric(df_merg[column], errors='coerce')
            df_merg = df_merg.dropna()
            category = df_merg.SPEC_DPTH.unique().tolist()
            value_main = []
            for spec in category:
                value_outer = []
                for _, row in df_merg[df_merg['SPEC_DPTH'] == spec].iterrows():
                    value_inner = []
                    value_inner.append(round(math.log10(row[columns[1]]),4))
                    value_inner.append(round(row[columns[2]],4))
                    value_outer.append(value_inner)
                value_main.append(value_outer)
            data['value'] = value_main
            data['category'] = category
        except Exception as exp:
            print('error')
            print(str(exp))
        return data

    def get_factual_chart_waterlevel(self,variable_two):
        """get the chart data for factual"""
        data = {}
        req_column_list = ["LOCA_ID","LOCA_LOCZ","MOND_RDNG"]
        try:
            df_loca = self.tables['LOCA']
            df_mond = self.tables['MOND']
            if variable_two == "Elevation":
                df_loca = self._get_elevation()
            data_frame = df_loca.merge(df_mond, on='LOCA_ID', how='left')
            for heading in self.heading_to_remove:
                data_frame = data_frame[data_frame["HEADING"] != heading]
            for col in data_frame.columns:
                data_frame[col] = pd.to_numeric(
                    data_frame[col], errors='ignore')
            df_merg = data_frame.copy()[req_column_list]
            df_merg = df_merg.dropna()
            df_merg["MOND_RDNG"] = df_merg["LOCA_LOCZ"]-df_merg["MOND_RDNG"]
            category = df_merg.LOCA_ID.unique().tolist()
            columns = df_merg.columns
            req_value,dvalue = [],{}
            value_waterlevel = []
            value_elevation = []
            for spec in category:
                for _, row in df_merg[df_merg['LOCA_ID'] == spec].iterrows():
                    value_waterlevel.append(round(row[columns[2]],4))
                    value_elevation.append(round(row[columns[1]],4))
            dvalue['name'] =' Water Level'
            dvalue['data'] = value_waterlevel
            req_value.append(dvalue)
            dvalue = {}
            dvalue['name'] =' Elevation'
            dvalue['data'] = value_elevation
            req_value.append(dvalue)
            data['value'] = req_value
            data['categories'] = category
        except Exception as exp:
            print('error')
            print(str(exp))
        return data
