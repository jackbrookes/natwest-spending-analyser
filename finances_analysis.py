# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 21:26:51 2017

@author: Jack
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math
import os

def load_datafiles(file_list):
    """
    loads, concatenates and returns a lst of csv files as a dataframe
    """
    df_list = []

    for f in file_list:
        temp_df = pd.read_csv(f, index_col=False)
        temp_df.drop(0, inplace=True)# delete first row (it is empty)
        df_list.append(temp_df)

    df = pd.concat(df_list, ignore_index=True)
    df.columns = [c.replace(' ', '') for c in df.columns]
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df['Year'] = df['Date'].map(lambda x: x.year)
    return df

def import_datasets(datafolder = 'datasets'):
    """
    Imports all files from datasets folder. Files should be CSV format and
    downloaded from NATWEST website. You can download results of up to 1 year
    intervals. It is recommended to download results from Jan 1st to Dec 31st
    for each year your account was active.
    """
    file_list = os.listdir(datafolder)
    path_list = [os.path.join(datafolder, f) for f in file_list]
    return load_datafiles(path_list)

def plot_balance(data):
    """
    Plots account balance over time
    """
    plt.plot(data["Date"], data["Balance"])
    plt.title('Balance over time')
    plt.show()

def plot_year_spending_hist(data, valmin = -math.inf, valmax = math.inf):
    """
    Plots a histogram of price of purchases for each year, filtered by a
    purchase range (can exclude large purchases or deposits)
    """
    df_st = data[data.Value.apply( lambda x: (x > valmin) and (x < valmax))]
    g = sns.FacetGrid(df_st, col = 'Year', col_wrap = 4)
    g = g.map(sns.distplot, "Value")
    sns.plt.show()


def plot_spending(data, filter_text):
    """
    Plots cumulative spending, can be filtered by a string contained in the
    description
    """
    df_st = data[data.Description.apply( lambda x: (filter_text in x))]
    df_st["Cumsum"] = df_st.Value.cumsum()
    plt.plot(df_st.Date, df_st.Cumsum)
    plt.title("Spending for '{}'".format(filter_text))
    plt.show()



if __name__ == '__main__':
    df = import_datasets('datasets')
    plot_balance(df)
    plot_year_spending_hist(df, -250, 0)
    plot_spending(df, "AMAZON")
