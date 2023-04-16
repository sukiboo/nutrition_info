"""
    Visualize nutritional info of various foods using the dataframe
    ./data/nutrition_info.csv produced by the function process_usda_data
    from ./process_nutrition_data.py
"""

import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

sns.set_theme(style='darkgrid', palette='muted', font='monospace', font_scale=.9)
colors = defaultdict(lambda: 'dodgerblue',
    {
    'Water': '#AEF0F3',
    'Protein': '#2BCE2B',
    'Carbohydrate': '#4146DA',
    'Sugar': '#999CEB',
    'Fiber': '#FFBE0B',
    'Fat': '#DA0331',
    'Fat, monounsaturated': '#FC4A71',
    'Fat, polyunsaturated': '#FB0E41',
    'Fat, saturated': '#8D0220',
    ##'Cholesterol': '',
    ##'Iron': '',
    ##'Calcium': '',
    ##'Magnesium': '',
    ##'Potassium': '',
    ##'Zinc': '',
    ##'Selenium': '',
    ##'Sodium': '',
    ##'Phosphorus': '',
    ##'Copper': '',
    ##'A': '',
    ##'B1': '',
    ##'B2': '',
    ##'B3': '',
    ##'B6': '',
    ##'B9': '',
    ##'B12': '',
    ##'C': '',
    ##'D': '',
    ##'E': '',
    ##'K': '',
    ##'DHA': '',
    ##'EPA': '',
    ##'DPA': '',
    None: '#00000000'
    })


def visualize_food(food, rda, name=None, amount_in_grams=100, show=True, save=False):
    """Visualize nutrition info for the given food"""
    print(food)
    # extract macros
    macro_labels = ['Protein', 'Carbohydrate', 'Fat']
    macro_values = [food[l] for l in macro_labels]
    macro_colors = [colors[l] for l in macro_labels]
    macros_sum = sum(macro_values)
    macro_offset = 90
    # extract macros with water
    water_labels = ['Protein', 'Carbohydrate', 'Water', 'Fat']
    water_values = [food[l] for l in water_labels]
    water_colors = [colors[l] for l in water_labels]
    water_offset = macro_offset
    # extract carbs
    carb_labels = ['Sugar', 'Fiber']
    carb_values = np.array([food[l] for l in carb_labels]) / macros_sum
    carb_colors = [colors[l] for l in carb_labels]
    carb_offset = macro_offset + 360 * macro_values[0] / macros_sum
    # extract fats
    fats_labels = ['Fat, saturated', 'Fat, polyunsaturated', 'Fat, monounsaturated']
    fats_values = np.array([food[l] for l in fats_labels]) / macros_sum
    fats_colors = [colors[l] for l in fats_labels]
    fats_offset = macro_offset
    # extract vitamins
    vitamin_labels = ['A', 'B1', 'B2', 'B3', 'B6', 'B9', 'B12', 'C', 'D', 'E', 'K']
    vitamin_values = [food[l]/rda[l] for l in vitamin_labels]
    vitamin_colors = [colors[l] for l in vitamin_labels]
    # extract minerals
    mineral_labels = ['Calcium', 'Copper', 'Iron', 'Magnesium', 'Phosphorus',
                      'Potassium', 'Selenium', 'Sodium', 'Zinc']
    mineral_values = [food[l]/rda[l] for l in mineral_labels]
    mineral_colors = [colors[l] for l in mineral_labels]
    # extract omega-3s
    omega_labels = ['DPA', 'DHA', 'EPA']
    omega_values = [food[l]/rda[l] for l in omega_labels]
    omega_colors = [colors[l] for l in omega_labels]

    # create figure and axes
    fig, ax = plt.subplots(figsize=(10,7))
    macro_ax = fig.add_axes([.0, .2, .6, .7])
    legend_ax = fig.add_axes([.0, .0, .6, .3])
    vitamin_ax = fig.add_axes([.7, .63, .25, .3])
    mineral_ax = fig.add_axes([.7, .26, .25, .27])
    omega_ax = fig.add_axes([.7, .07, .25, .09])
    # configure axes
    ax.axis('off')
    macro_ax.axis('off')
    legend_ax.axis('off')
    if name is None:
        name = food['Description']
    macro_ax.set_title(f"{name} (per {amount_in_grams}g)", size=14, weight='bold')

    # plot macros
    macro_ax.pie(macro_values, colors=macro_colors,
           startangle=macro_offset, counterclock=True, radius=1.,
           wedgeprops=dict(width=.5, edgecolor='w'))

    # plot macros with water
    macro_ax.pie(water_values, colors=water_colors,
           startangle=water_offset, counterclock=True, radius=.5,
           wedgeprops=dict(width=.2, edgecolor='w'))
    # plot carbs
    macro_ax.pie(carb_values, colors=carb_colors, normalize=False,
           startangle=carb_offset, counterclock=True, radius=1.,
           wedgeprops=dict(width=.2, edgecolor='w'))
    # plot fats
    macro_ax.pie(fats_values, colors=fats_colors, normalize=False,
           startangle=fats_offset, counterclock=False, radius=1.,
           wedgeprops=dict(width=.2, edgecolor='w'))
    # plot energy density
    macro_ax.text(0, 0, f"{food['Energy']:.0f}\nkcal",
                  ha='center', va='center', size=14, weight='bold')
    # plot macros legend
    legend_labels = ['Protein', None, None, 'Water',
                     'Carbohydrate', 'Sugar', 'Fiber', None,
                     'Fat', 'Fat, saturated',
                     'Fat, polyunsaturated', 'Fat, monounsaturated']
    legend = [mpl.patches.Patch(color=colors[label]) for label in legend_labels]
    legend_ax.legend(legend, legend_labels, ncol=3, loc='center')
    # plot vitamins
    vitamin_pos = range(len(vitamin_values))
    vitamin_ax.barh(vitamin_pos, vitamin_values, color=vitamin_colors, height=1.)
    vitamin_ax.set_ylim([vitamin_pos[0]-.5, vitamin_pos[-1]+.5])
    vitamin_ax.set_yticks(vitamin_pos)
    vitamin_ax.set_yticklabels(vitamin_labels)
    vitamin_ax.invert_yaxis()
    vitamin_ax.set_xlim([0,1])
    vitamin_ax.set_xticks([.0,.25,.5,.75,1.])
    vitamin_ax.set_xticklabels(['0%','25%','50%','75%','100%'])
    vitamin_ax.set_title('Vitamins (% of RDA)', size=10, weight='bold')
    # plot minerals
    mineral_pos = range(len(mineral_values))
    mineral_ax.barh(mineral_pos, mineral_values, color=mineral_colors, height=1.)
    mineral_ax.set_ylim([mineral_pos[0]-.5, mineral_pos[-1]+.5])
    mineral_ax.set_yticks(mineral_pos)
    mineral_ax.set_yticklabels(mineral_labels)
    mineral_ax.invert_yaxis()
    mineral_ax.set_xlim([0,1])
    mineral_ax.set_xticks([.0,.25,.5,.75,1.])
    mineral_ax.set_xticklabels(['0%','25%','50%','75%','100%'])
    mineral_ax.set_title('Minerals (% of RDA)', size=10, weight='bold')
    # plot omega-3s
    omega_pos = range(len(omega_values))
    omega_ax.barh(omega_pos, omega_values, color=omega_colors, height=1.)
    omega_ax.set_ylim([omega_pos[0]-.5, omega_pos[-1]+.5])
    omega_ax.set_yticks(omega_pos)
    omega_ax.set_yticklabels(omega_labels)
    omega_ax.invert_yaxis()
    omega_ax.set_xlim([0,1])
    omega_ax.set_xticks([.0,.25,.5,.75,1.])
    omega_ax.set_xticklabels(['0%','25%','50%','75%','100%'])
    omega_ax.set_title('Omega-3 (% of RDA)', size=10, weight='bold')

    # save and show the plot
    if save:
        os.makedirs(f'./images', exist_ok=True)
        plt.savefig(f'./images/{name}.png', dpi=300)
    if show:
        plt.show()
    else:
        plt.close()


if __name__ == '__main__':

    # load processed nutrition data
    df = pd.read_csv('./data/nutrition_info.csv')
    rda = df.iloc[np.where(df['FDC ID']==0)[0].item()]
    food = df.iloc[np.where(df['FDC ID']==2343846)[0].item()]
    visualize_food(food, rda, show=True, save=False)

