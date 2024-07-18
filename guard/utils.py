import csv 
import pandas as pd

def csv_to_dict(file_path):
    # print(file_path)
    file=pd.read_csv(file_path)
    # dic=file.to_dict()
    columns_name=file.columns.to_list()
    data_dict=file.to_dict(orient='list')
    


    return columns_name,data_dict

