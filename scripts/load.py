import pandas as pd
from sqlalchemy import create_engine,text

def load_data(input_path="../data/transformed.csv"):
    df = pd.read_csv(input_path)
    engine = create_engine("postgresql+psycopg2://postgres:123456@localhost:5432/zomato_db")

    dim_location = df[['location']].drop_duplicates().reset_index(drop=True)
    dim_location['location_id'] = dim_location.index + 1

    dim_cuisine = df[['cuisines']].drop_duplicates().reset_index(drop=True)
    dim_cuisine['cuisine_id'] = dim_cuisine.index + 1

    dim_rest_type = df[['rest_type']].drop_duplicates().reset_index(drop=True)
    dim_rest_type['rest_type_id'] = dim_rest_type.index + 1

    fact = (
        df.merge(dim_location, on='location', how='left')
          .merge(dim_cuisine, on='cuisines', how='left')
          .merge(dim_rest_type, on='rest_type', how='left')
    )

    fact = fact[[
        'name', 'online_order', 'book_table', 'rate', 'votes',
        'approx_cost(for two people)', 'dish_liked', 'phone',
        'location_id', 'cuisine_id', 'rest_type_id'
    ]].rename(columns={'approx_cost(for two people)': 'approx_cost'})

    # print(dim_location.head())
    # print(dim_cuisine.head())
    # print(dim_rest_type.head())
    # print(fact.head())

    
    dim_location.to_sql('dim_location',engine, index=False, if_exists='replace')
    dim_cuisine.to_sql('dim_cuisine', engine, index=False, if_exists='replace')
    dim_rest_type.to_sql('dim_rest_type',engine, index=False, if_exists='replace')
    fact.to_sql('fact_restaurants', engine, index=False, if_exists='replace')

    with engine.begin() as conn:
        conn.execute(text("""
            ALTER TABLE fact_restaurants
            ADD COLUMN id SERIAL PRIMARY KEY;
        """))

    engine.dispose()

load_data()
