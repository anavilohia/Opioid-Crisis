#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

state_abbreviations = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


def get_income_data (income_data_file):

    income_data_file = open(income_data_file, "r", encoding="utf-8")
    income_data_html = income_data_file.read()
    income_data_pd = pd.read_html(income_data_html)[0]
    
    counties = income_data_pd[1].as_matrix()[1:]
    states = income_data_pd[2].as_matrix()[1:]
    income = income_data_pd[3].as_matrix()[1:]
    
    income_data = {}
    
    for i in range(0, len(counties)):
        
        if type(counties[i]) != str or type(states[i]) != str:
            continue
        
        county = counties[i] + ", " + states[i]
        
        county = county.replace(" County", "")
        
        income_value = float(re.sub(r'\D', '', income[i]))
        
        income_data[county] = income_value
    
    return income_data
    

def get_death_data (death_data_file):

    death_data_pd = pd.read_table(death_data_file).as_matrix()
    
    death_data = {}
    
    for row in death_data_pd:
        
        county,state = row[1].split(", ")
        
        county = county.replace(" County", "")
        
        try:
            death_rate = float(row[5])
        except:
            death_rate = 0
        
        death_data[county + ", " + state_abbreviations[state]] = death_rate
        
    return death_data
 

def merge_data (income_data, death_data):
    
    data = {}
    
    for county in income_data.keys():
        
        if not county in death_data:
            continue
        
        try:
            income = income_data[county]
            death_rate = death_data[county]

        except:
            continue
        
        data[county] = (income, death_rate)
        
    return data


def data_to_lists (data):
    
    list1 = []
    list2 = []
    
    for value in data.values():
        
        list1.append(value[0])
        list2.append(value[1])

    
    return list1, list2
    
def graph_data (data, list1, list2):

    # scatter plot
    
    plt.title("Opioid Incidence Rate vs. Per Capita Income")
    plt.xlabel("Per Capita Income")
    plt.ylabel("Opioid Incidence Rate (per 100,000 people)")

    for county in data.keys():
            plt.scatter(*data[county])
            
    plt.show()
    
    # heatmap
    
    weights = [1] * len(list2)
    for i in range(0, len(list1)):
        list2[i] = list2[i] * -1000
    list1 = np.array(list1)
    list2 = np.array(list2)
    weights = np.array(weights)
    
    heatmap = plt.hist2d(list2, list1, weights=weights, bins=30)[0]
    extent = [0, 100, 0, 100]
    plt.clf()
    plt.imshow(heatmap)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.show()
    
    # bar graph
    
    income_threshold = 40000
    
    below_threshold = []
    above_threshold = []
    
    
    for county in data.keys():
        
        income = data[county][0]
        incidence_rate = data[county][1]
        
        if income < income_threshold:
            below_threshold.append(incidence_rate)
        else:
            above_threshold.append(incidence_rate)
            
    avg_below = np.average(below_threshold)
    avg_above = np.average(above_threshold)
    
    objects = ("Below $" + str(income_threshold), "Above $" + str(income_threshold))
    y_pos = np.arange(len(objects))
    performance = [avg_below, avg_above]
     
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Average Opioid Incidence Rate (per 100,000 people)')
    plt.title('Opioid Incidence Rate By Income Category')
     
    plt.show()



income_data = get_income_data("income_data.txt")
death_data = get_death_data("death_data.txt")
data = merge_data(income_data, death_data)
list1, list2 = data_to_lists(data)
graph_data(data, list1, list2)






