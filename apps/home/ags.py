from python_ags4 import AGS4
from pandas import DataFrame
from pandas import to_numeric
from pandas import ExcelWriter
from openpyxl.utils import get_column_letter


class AGS:
    """ags class to process ags files"""

    def __init__(self, ags_file):
        """class initialization"""
        self.ags_file = ags_file
        self.ags_version = self._version_check()

    def _version_check(self):
        version = None
        file = open(self.ags_file, "r", encoding='utf-8', errors="replace")
        for _, line in enumerate(file, start=1):
            if line.startswith(r'"**PROJ"'):
                version = 'ags3'
                break
            if line.startswith(r'"GROUP"'):
                version = 'ags4'
                break
            break
        return version

    def _ags_to_dict(self):
        """ags to dict"""
        data, headings, line_numbers = {}, {}, {}
        close_file = True
        try:
            file = open(self.ags_file, "r", encoding='utf-8', errors="replace")
            for i, line in enumerate(file, start=1):
                temp = line.rstrip().split('","')
                temp = [item.strip('"') for item in temp]
                if '**' in temp[0]:
                    group = temp[0].strip('**')
                    data[group] = {}
                    line_numbers[group] = {'GROUP': i, 'HEADING': '-'}
                    headings[group] = []
                elif '*' in temp[0]:
                    if len(temp) != len(set(temp)):
                        print('Invalid length')
                    for item in temp:
                        headings[group].append(item.strip('*').strip('?'))
                        data[group][item.strip('*').strip('?')] = []
                elif len(temp) > 1:
                    if len(temp) != len(headings[group]):
                        print('Invalid length')
                    for i in range(0, len(temp)):
                        data[group][headings[group][i]].append(temp[i])
                else:
                    continue
        finally:
            if close_file:
                file.close()
        return data, headings

    def ags_to_dataframe(self):
        """convert ags to dictionary"""
        tables, headings = {}, {}
        if self.ags_version is not None:
            if self.ags_version == 'ags4':
                tables, headings = AGS4.AGS4_to_dataframe(self.ags_file)
                # print(tables)
            if self.ags_version == 'ags3':
                data, headings = self._ags_to_dict()
                for key in data:
                    tables[key] = DataFrame(data[key])
        return tables, headings

    def convert_to_numeric(self, dataframe):
        """Convert to Numeric"""
        data_frame = dataframe.copy()
        numeric_df = data_frame.loc[:, data_frame.iloc[1].str.contains('DP|MC|SF|SCI')].apply(to_numeric, errors='coerce')
        data_frame[numeric_df.columns] = numeric_df
        data_frame = data_frame.iloc[2:, :].reset_index(drop=True)
        return data_frame

    def ags_to_excel(self, output_file, sort_tables=False):
        """AGS to excel"""
        if self.ags_version is not None:
            if self.ags_version == 'ags4':
                tables, _ = AGS4.AGS4_to_dataframe(self.ags_file)
            if self.ags_version == 'ags3':
                tables, _ = self._ags_to_dict()
        if sort_tables is True:
            list_of_tables = sorted(tables.keys())
        else:
            list_of_tables = tables.keys()
        if len(list_of_tables) == 0:
            print("error")
        with ExcelWriter(output_file, engine='openpyxl') as writer:
            for key in list_of_tables:
                if 25000 < tables[key].shape[0] < 100000:
                    print("error")
                elif tables[key].shape[0] > 100000:
                    print("error")
                tables[key].to_excel(writer, sheet_name=key, index=False)
                for i, col in enumerate(tables[key], start=1):
                    max_width = min(max(13, tables[key][col].map(len).max() + 1), 75)
                    writer.sheets[key].column_dimensions[get_column_letter(i)].width = max_width

    def get_proj_code(self,region):
        """Get epsg code based on the region"""
        epsg = 4326
        if "Saudi Arabia" in region:
            epsg = 32636
        if "Abu Dhabi" in region:
            epsg = 32640
        if "Dubai" in region:
            epsg = 3997
        return epsg
