import re

import pandas as pd 

from bcr_api.bwproject   import BWProject, BWUser 
from bcr_api.bwresources import * 

class BrandwatchInterface:
    def data_extraction_settings_method(self, output_file_name: str, start_date: str, end_date: str, username: str, password: str, token_file: str, project_id: str, widget_names_list: list[str]):
        self.output_file_name  = output_file_name
        self.start_date        = start_date 
        self.end_date          = end_date
        self.widget_names_list = widget_names_list 
        
        with open(token_file, "r") as f:
            self.brandwatch_user    = BWUser(username = username, password = password, token = f.read())
            self.brandwatch_project = BWProject(username = username, project = project_id)

    def extract_data(self):
        self.__query_object, output_data_list = BWQueries(self.brandwatch_project), []

        for widget_name in self.widget_names_list:
            query_result             = self.__query_object.get_mentions(name = widget_name, startDate = self.start_date, endDate = self.endDate)
            result_table             = pd.DataFrame(query_result)
            result_table["fullText"] = result_table.apply(lambda x: re.sub(r"[\x00-\x1F]+", "", x["fullText"]), axis = 1)
            output_data_list.append(result_table)

        self.combined_dataframe = pd.concat(output_data_list).reset_index(drop = True)

    def save_result_data(self):
        match (self.output_file_name.split(".")[-1].lower()):
            case "xlsx" : self.combined_dataframe.to_excel(self.output_file_name, index = False)
            case "csv"  : self.combined_dataframe.to_csv(self.output_file_name, index = False)
            case _      : raise Exception("Unknown file type")