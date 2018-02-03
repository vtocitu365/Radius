import sys
import json
import numpy as np
from collections import defaultdict
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from collections import Counter
from itertools import chain
import matplotlib.pyplot as plt
import pylab as pl

# Imports json file as a dictionary
with open('data_analysis.json') as f:
    data = json.load(f)

#---------------------------------------------------------------------------
# Code computes the fill rate, true-value fill rate, and cardinality
#---------------------------------------------------------------------------
# Calculates the fill rate
def fill_rate(data):
    count = defaultdict(int)
    for d in data:
        for key, value in d.iteritems():
            if value:
                count[key] += 1
    return count

# Calculates the true-value fill rate
def true_value_fill_rate(data):
    count = defaultdict(int)
    for d in data:
        for key, value in d.iteritems():
            if value and not (value == 0 or value.encode('utf-8') == 'null' \
                    or value == '' or value == ' ' or value == 'None' \
                    or value == 'none' or value == '0'):
                    count[key] += 1
    return count

# Finds the unique elements in each field by  turning each unique value into a
# dictionary key and returning the key a count of how many times each key
# appears.
def unique_category_values(data,key):
    item_count = defaultdict(int)
    for d in data:
        if d[key] and not (d[key] == 0 or d[key] == 'null' or d[key] == '' \
                or d[key] == ' ' or d[key] == 'none' or d[key] == '0' \
                or d[key] == 'None'):
                item_count[d[key]] += 1
    return item_count

# Calculates the number of unique elements and cardinality of each field by
# taking the dictionary of unique elements created for each field and
# returning its length as the number of unique elements, and the cardinality
# of each field
def get_cardinality(data, tvfr):
    unique_elements = defaultdict(int)
    cardinality = defaultdict(int)
    for key in data[0].keys():
        unique_elements[key]=len(unique_category_values(data,key))
        cardinality[key] = float(unique_elements[key]) / float(tvfr[key])
    return unique_elements, cardinality

#---------------------------------------------------------------------------
# Code ignores entries with empty fields save for the phone field, and
# analyzes the remainder.
#---------------------------------------------------------------------------
# Finds the entries with no empty or irrelevant data in any field except
# the 'phone' field
def not_empty_datapoints(data):
    empty_dict_count = []
    for d in data:
        count = 0
        for key, value in d.iteritems():
            if key != 'phone':
                if value == None or (value == 0 or value == 'null' \
                    or value == '' or value == ' ' or value == 'None' \
                    or value == 'none' or value == '0'):
                    count += 1
        if count == 0:
            empty_dict_count.append(d)
    return empty_dict_count

# Create the subplots
def build_plots(data, key, subplot_num):
    ax = fig.add_subplot(int("22"+subplot_num))
    data_count = data
    X = np.arange(len(data_count))
    squared = list(map(lambda x: np.log(x), data_count.values()))
    pl.bar(X, squared, align='center', width=0.5)
    pl.xticks(X, data_count.keys(), rotation=90)
    ymax = max(squared) + 1
    pl.ylim(0, ymax)
    ax.set_title(key)
    return fig

# Find which entries are not repeats
def get_unique_entries(data):
    with open('nonempty_data.txt', 'w') as w:
        w.writelines("%s\n" % str(l) for l in data)
        w.close()
    with open("nonempty_data.txt", "r")as f:
        reduced_data = f.readlines()
        new_data = ''
        count = 0
        for x in reduced_data:
            if x not in new_data:  # if item is a duplicate
                new_data = ''.join(x)
                count += 1
    return count

# Get the fill rate
fr = fill_rate(data)
# Get the true-value fill rate
tvfr = true_value_fill_rate(data)
# Get the number of unique elements and the cardinality
[unique_elements, cardinality] = get_cardinality(data,tvfr)
# Calculate the number of incorrectly input elements
num_incorrect_elements = defaultdict(int)
for key in fr.keys():
    num_incorrect_elements[key] = int(fr[key]) - int(tvfr[key])

# Count the number of times each category appears in the data
state_count = unique_category_values(data, 'state')
time_count = unique_category_values(data, 'time_in_business')
head_count = unique_category_values(data, 'headcount')
revenue_count = unique_category_values(data, 'revenue')

hist_title = "Prominence of categories in the Categorical Fields"
fig = plt.figure()
fig.suptitle(hist_title, fontsize=14)
build_plots(time_count,'time_in_business',"1")
build_plots(revenue_count,'revenue',"2")
build_plots(head_count,'headcount',"3")
plt.tight_layout()
plt.subplots_adjust(top=0.85)
pl.show()

# Find the number of entries with relevant data in all fields
# except the phone field.
not_empty_entries=  not_empty_datapoints(data)
num_nonempty_entries = get_unique_entries(not_empty_entries)