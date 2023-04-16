# Nutrition Info
A toy project to help me make more informed dietary choices.

Currently working with [FNDDS 2019-2020 dataset](https://fdc.nal.usda.gov/download-datasets.html) provided by the USDA.
The file structure is the following:
* `process_nutrition_data.py` reads `FoodData_Central_survey_food_json_2022-10-28.json` and parses it into the nice dataframe `nutrition_info.csv`
* `visualize_nutrition_data` takes info from `nutrition_info.csv` and visualizes it (see examples below)
* `main.py` visualizes the given food items, represented by their FDC ID, which can be found on the Survey Foods (FNDDS) tab at https://fdc.nal.usda.gov/fdc-app.html


## Future Work
This code is a bit rough and I might clean it up at if I ever have some free time (but since it's a hobby project, I wouldn't expect it to happen any time soon 🥲).
The main things to be done:
1. Pick nicer colors
2. Extend code functionality
3. Improve file organization


## Examples
![fruits](https://user-images.githubusercontent.com/38059493/232321191-6339cd77-3dd8-40ba-bb97-9a215649de91.png)
![vegetables](https://user-images.githubusercontent.com/38059493/232321196-148a53a0-e348-469f-af1b-a8217d3196d5.png)
![sides](https://user-images.githubusercontent.com/38059493/232321204-1f0bea38-1848-49f9-90a1-ed00677011b0.png)
![meats](https://user-images.githubusercontent.com/38059493/232321210-d7cd5b62-eaf6-4aa2-8c4b-06e7ab7c8258.png)

