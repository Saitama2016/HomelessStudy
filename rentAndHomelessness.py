import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import datetime as dt
from statistics import mean

# Read CSV file of Prices
price_data = pd.read_csv("./OGData/price.csv")

los_angeles_prices = price_data.loc[price_data["City"] == "Los Angeles"]

print(los_angeles_prices)

rent_data = {
    'Year': [],
    'Average Rent': []
}

january_list = []

for col in los_angeles_prices.columns:
    if "January" in col:
        january_list.append(col)

print(january_list)
avg_rent = los_angeles_prices[january_list].values[0]

# Convert Numpy Array to List
avg_rent_list = np.ndarray.tolist(avg_rent)
print(avg_rent_list)

for year in january_list:
    rent_data['Year'].append(year)

for rent in avg_rent:
    rent_data['Average Rent'].append(rent)

print(rent_data)

rent_table = pd.DataFrame(rent_data, columns=['Year', 'Average Rent'])
rent_table.index = rent_table.index + 1
print(rent_table)

# Check the type of data in each element in avg_rent numpy array
# for rent in avg_rent:
#     print(type(rent))

homeless_data = pd.read_csv("./OGData/2007-2016-Homelessnewss-USA.csv")

los_angeles_homelessness = homeless_data.loc[homeless_data["CoC Name"].str.contains("Los Angeles")]

total_homeless_la = los_angeles_homelessness.loc[los_angeles_homelessness["Measures"] == "Total Homeless"]

homeless_updated_data = {
    'Year': [],
    'Total Homeless': []
}

years = []
homeless_count = []

for year in total_homeless_la["Year"]:
    year = dt.datetime.strptime(year, "%m/%d/%Y").strftime("%B %Y")
    years.append(year)

for total in total_homeless_la["Count"]:
    total = total.replace(',','')
    total = float(total)
    homeless_count.append(total)

print(homeless_count)

for homeless in homeless_count:
    homeless_updated_data['Total Homeless'].append(homeless)

for year in years:
    homeless_updated_data['Year'].append(year)

print(homeless_updated_data)

homeless_table = pd.DataFrame(homeless_updated_data, columns=['Year', 'Total Homeless'])
homeless_table.index = homeless_table.index + 1
print(homeless_table)

merge_table = homeless_table.merge(rent_table)
print(merge_table)

merged_rent = []
merged_homeless = []
merged_year = []

for rent in merge_table['Average Rent']:
    merged_rent.append(rent)

for homeless in merge_table['Total Homeless']:
    merged_homeless.append(homeless)

for year in merge_table['Year']:
    merged_year.append(year)

xs = np.array(merged_rent, dtype=np.float64)
ys = np.array(merged_homeless, dtype=np.float64)

def best_fit_slope_and_intercept(xs,ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) / 
        ((mean(xs)*mean(xs)) - mean(xs*xs)))
    
    b = mean(merged_homeless) - m*mean(merged_rent)

    return m, b

m, b = best_fit_slope_and_intercept(xs, ys)

regression_line = [(m*x) + b for x in xs]

string_regression_line = str(m)+'x' + ' + ' + str(b)

matplotlib.get_backend()
plt.scatter(xs, ys, color="dodgerblue", label="Total Homeless")
plt.plot(xs, regression_line, color="red", label="Regression Line")
plt.xlabel('Average Rent (USD)')
plt.ylabel('Total Homeless')
plt.title("Rent and Homelessness Los Angeles (2011-2016)", weight="bold")
for i, txt in enumerate(merged_year):
    plt.annotate(txt, (xs[i], ys[i]), weight="bold", fontsize="8")
plt.legend()
plot_name = 'rent_and_homelessness_' + dt.datetime.now().strftime("%m_%d_%Y") + '.png'
plot_dir = './Graphs/'
if not os.path.exists(plot_dir):
    os.mkdir(plot_dir)
full_plot_name = os.path.join(plot_dir, plot_name)
plt.savefig(full_plot_name, bbox_inches='tight')
plt.show(block=False)
plt.close('all')