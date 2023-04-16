"""
    Load the dataframe ./data/nutrition_info.csv produced by
    the function process_usda_data from ./process_nutrition_data.py
    and visualize it via the the function visualize_food
    from ./visualize_nutrition_data.py

    Each food is represented by its FDC ID that can be found on
    the Survey Foods (FNDDS) tab at https://fdc.nal.usda.gov/fdc-app.html
"""

import pandas as pd
import numpy as np
from visualize_nutrition_data import visualize_food


if __name__ == '__main__':

    # load processed nutrition data
    df = pd.read_csv('./data/nutrition_info.csv')
    rda = df.iloc[np.where(df['FDC ID']==0)[0].item()]

    # foods to visualize
    ids = {
            'Buckwheat': 2343846,
            'Pasta': 2343842,
            'Potato': 2344876,
            'Rice': 2343892,
            'Beef': 2341227,
            'Chicken': 2341360,
            'Pork': 2341282,
            'Salmon': 2341700,
            'Cucumber': 2345304,
            'Lettuce': 2345309,
            'Onion': 2345315,
            'Tomato': 2345232,
            'Apple': 2344711,
            'Banana': 2344720,
            'Lemon': 2344662,
            'Strawberry': 2344777,
            }

    # fisualize each food
    for name, id in ids.items():
        food = df.iloc[np.where(df['FDC ID']==id)[0].item()]
        visualize_food(food, rda, name=name, amount_in_grams=100, show=True, save=True)

