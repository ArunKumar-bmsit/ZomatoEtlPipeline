import pandas as pd
import numpy as np

def transform_data(input_path="../data/raw_extract.csv"):
    df = pd.read_csv(input_path)

    df['rate'] = df['rate'].str.replace('/5', '', regex=False)
    df['rate'] = pd.to_numeric(df['rate'], errors='coerce')
    df['rate']=df['rate'].fillna(df['rate'].median())
    df['phone']=df['phone'].fillna('Not Available')
    df['dish_liked']=df['dish_liked'].fillna('No information')
    df['cuisines']=df['cuisines'].fillna('Not Specified')
    df = df.dropna(subset=['location'])
    df['rest_type']=df['rest_type'].fillna(df['rest_type'].mode()[0])
    df['approx_cost(for two people)'] = pd.to_numeric(df['approx_cost(for two people)'], errors='coerce')
    df['approx_cost(for two people)']=df['approx_cost(for two people)'].fillna(df['approx_cost(for two people)'].median())

    df.to_csv("../data/transformed.csv", index=False)
    return "../data/transformed.csv"

transform_data()