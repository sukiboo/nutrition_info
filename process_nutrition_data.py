"""
    Prosess nutritional info from FNDDS 2019-2020 dataset available at
    https://fdc.nal.usda.gov/download-datasets.html
    Foods in the resulting dataframe are represented by their FDC ID that can be
    found on the Survey Foods (FNDDS) tab at https://fdc.nal.usda.gov/fdc-app.html
    All nutrition values listed are per 100g of food.
"""

import json
import pandas as pd


# keep only the following nutrients in this order
nutrient_name = {
    'Energy': 'Energy',
    'Water': 'Water',
    # macronutrients
    'Protein': 'Protein',
    'Carbohydrate, by difference': 'Carbohydrate',
    'Sugars, total including NLEA': 'Sugar',
    'Fiber, total dietary': 'Fiber',
    'Total lipid (fat)': 'Fat',
    'Fatty acids, total monounsaturated': 'Fat, monounsaturated',
    'Fatty acids, total polyunsaturated': 'Fat, polyunsaturated',
    'Fatty acids, total saturated': 'Fat, saturated',
    'Cholesterol': 'Cholesterol',
    # minerals
    'Calcium, Ca': 'Calcium',
    'Copper, Cu': 'Copper',
    'Iron, Fe': 'Iron',
    'Magnesium, Mg': 'Magnesium',
    'Phosphorus, P': 'Phosphorus',
    'Potassium, K': 'Potassium',
    'Selenium, Se': 'Selenium',
    'Sodium, Na': 'Sodium',
    'Zinc, Zn': 'Zinc',
    # vitamins
    'Vitamin A, RAE': 'A',
    'Thiamin': 'B1',
    'Riboflavin': 'B2',
    'Niacin': 'B3',
    'Vitamin B-6': 'B6',
    'Folate, total': 'B9',
    'Vitamin B-12': 'B12',
    'Vitamin C, total ascorbic acid': 'C',
    'Vitamin D (D2 + D3)': 'D',
    'Vitamin E (alpha-tocopherol)': 'E',
    'Vitamin K (phylloquinone)': 'K',
    # Omega-3
    'PUFA 22:5 n-3 (DPA)': 'DPA',
    'PUFA 22:6 n-3 (DHA)': 'DHA',
    'PUFA 20:5 n-3 (EPA)': 'EPA',
    # ignored values
    ##'Alcohol, ethyl'
    ##'Caffeine'
    ##'Theobromine'
    ##'Retinol' # included in Vitamin A
    ##'Carotene, beta' # can be converted to Vitamin A
    ##'Carotene, alpha' # can be converted to Vitamin A
    ##'Cryptoxanthin, beta' # also carotenoid
    ##'Lycopene' # also carotenoid
    ##'Lutein + zeaxanthin' # this too
    ##'Choline, total'
    ##'Folic acid'
    ##'Folate, food'
    ##'Folate, DFE'
    ##'Vitamin E, added'
    ##'Vitamin B-12, added'
    ##'SFA 4:0'
    ##'SFA 6:0'
    ##'SFA 8:0'
    ##'SFA 10:0'
    ##'SFA 12:0'
    ##'SFA 14:0'
    ##'SFA 16:0'
    ##'SFA 18:0'
    ##'MUFA 18:1'
    ##'PUFA 18:2'
    ##'PUFA 18:3'
    ##'PUFA 20:4'
    ##'MUFA 16:1'
    ##'PUFA 18:4'
    ##'MUFA 20:1'
    ##'MUFA 22:1'
}


# RDA data is taken from https://www.fda.gov/media/99069/download
# see also pages 903-906 at
# https://s3.amazonaws.com/public-inspection.federalregister.gov/2016-11867.pdf
rda_nutrients = {
    'Energy': 2000,
    'Water': 4000,
    # macronutrients
    'Protein': 100,
    'Carbohydrate, by difference': 200,
    'Sugars, total including NLEA': 50,
    'Fiber, total dietary': 30,
    'Total lipid (fat)': 100,
    'Fatty acids, total monounsaturated': 35,
    'Fatty acids, total polyunsaturated': 35,
    'Fatty acids, total saturated': 30,
    'Cholesterol': 300,
    # minerals
    'Iron, Fe': 18,
    'Calcium, Ca': 1300,
    'Copper, Cu': .9,
    'Magnesium, Mg': 420,
    'Selenium, Se': 55,
    'Sodium, Na': 2300,
    'Phosphorus, P': 1250,
    'Potassium, K': 4700,
    'Zinc, Zn': 11,
    # vitamins
    'Vitamin A, RAE': 900,
    'Thiamin': 1.2,
    'Riboflavin': 1.3,
    'Niacin': 16,
    'Vitamin B-6': 1.7,
    'Folate, total': 400,
    'Vitamin B-12': 2.4,
    'Vitamin C, total ascorbic acid': 90,
    'Vitamin D (D2 + D3)': 20,
    'Vitamin E (alpha-tocopherol)': 15,
    'Vitamin K (phylloquinone)': 120,
    # Omega-3
    'PUFA 22:5 n-3 (DPA)': .2,
    'PUFA 22:6 n-3 (DHA)': .2,
    'PUFA 20:5 n-3 (EPA)': .2,
    }


def process_usda_data(save=True):
    """Process and save USDA nutrition data"""
    usda_data_file = './data/FoodData_Central_survey_food_json_2022-10-28.json'
    with open(usda_data_file, 'r') as data_file:
        usda_data = json.loads(data_file.read())

    # start with RDA control entry
    foods = dict({0: {'Description': 'RDA',\
                      **{nutrient_name[nutrient]: amount\
                      for nutrient, amount in rda_nutrients.items()}}})

    # extract the relevant nutrition info for each food item
    for food in list(usda_data.values())[0]:
        foods[food['fdcId']] = {'Description': food['description']}
        info = foods[food['fdcId']]
        for nutrient in food['foodNutrients']:
            if nutrient['nutrient']['name'] in nutrient_name:
                label = f"{nutrient_name[nutrient['nutrient']['name']]}"
                info[label] = nutrient['amount']

    # save the processed info
    df = pd.DataFrame.from_dict(foods, orient='index')
    df = df[['Description'] + list(nutrient_name.values())]
    df = df.reset_index().rename(columns={'index': 'FDC ID'})
    if save:
        df.to_csv('./data/nutrition_info.csv', index=False)
    return df


if __name__ == '__main__':

    df = process_usda_data(save=True)

