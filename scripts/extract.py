import pandas as pd

def extract_data():
    df=pd.read_csv('../data/zomato.csv')
    df.to_csv("../data/raw_extract.csv", index=False)
    print("run succesfully")
    return "../data/raw_extract.csv"
    
extract_data()