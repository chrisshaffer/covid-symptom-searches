# custom functions
from load_data import load_data
from col_list import col_list
from clean_data import clean_data
from hospitals_subplots import hospitals_subplots
from hospitals_plot import hospitals_plot
from hyp_test import hyp_test

# modules
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import warnings
from datetime import datetime
import scipy.stats as stats
from math import sqrt
import itertools
from datetime import timedelta

import seaborn as sns
from math import sqrt
import matplotlib.pyplot as plt
import scipy.stats as stats


def params_to_pval(date_rng,symptom,delay,region,save):
    nh = 'new_hospitalized'
    dir = '~/DSI/covid-symptom-searches/data/'
    nrows= None
    usecols = 'date key ' + symptom
    usecols = usecols.split()
    hospital, searches, _ = load_data(dir,nrows,usecols)

    df = hospital[['key','date','new_hospitalized']]
    
    hospital = df[df['key'] == region]
    hospital[nh] = hospital[nh].diff()
    
    searches_cols_kd = list(searches.columns)
    searches_cols = searches_cols_kd[2:]

    df = clean_data(searches,hospital)
    
    df['date'] = df['date'].transform(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    df = df[(df['date'] > date_rng[0]) & (df['date'] < date_rng[1])]
    
    hospital['date'] = hospital['date'].transform(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    hospital = hospital[(hospital['date'] > date_rng[0]) & (hospital['date'] < date_rng[1])]
    
    searches = df[df['key'] == region]
    
    searches['date'] = searches['date'] + timedelta(days=delay)

    searches_by_date = searches[['date'] + searches_cols].groupby('date').sum()
    searches_by_date[symptom] = searches_by_date[symptom].diff()
    pos_searches = searches_by_date[searches_by_date[symptom] > 0]
    neg_searches = searches_by_date[searches_by_date[symptom] <= 0]

    pos_searches.reset_index(inplace = True)
    neg_searches.reset_index(inplace = True)

    # pos_searches.sort_values(by = 'date',axis=0,inplace=True)
    # neg_searches.sort_values(by = 'date',axis=0,inplace=True)
    
    # pos_searches['date'] = pos_searches['date'] + timedelta(days=delay)
    # neg_searches['date'] = neg_searches['date'] + timedelta(days=delay)
    titles = symptom.replace('search_trends','').replace('_',' ')

#     fig = plt.figure(figsize=(6,6))

    matplotlib.rcParams.update(matplotlib.rcParamsDefault)

    sns.set(font_scale = .7)
    plt.style.use("dark_background")
    sns.set_context("paper")

    matplotlib.rcParams.update({'grid.linewidth': .2})

    palette = itertools.cycle(sns.color_palette("husl"))
#     for i in range(2):
#             ax = plt.subplot()
#             if i == 0:
#                 data = pos_searches
#             elif i == 1:
#                 data = neg_searches
#             sns.scatterplot(x = "date", y = symptom,
#                             data = pd.DataFrame(data),
#                             color=next(palette),
#                             size = 2)
#             plt.xticks(rotation=80)
            
#             xtick_range = range(0,len(searches_by_date.index),14)
#             ax.set_xlim()
#             ax.set_title(titles[0])
#             ax.set_xticks(xtick_range) # <--- set the ticks first
#             ax.set_xlabel('date', labelpad=15)
#             ax.set_ylabel('Search Density ', labelpad=15)

#     fig.tight_layout()
#     plt.show()
    save_str = '_delay' + str(delay) + '_' + titles + '_' + region + '.png'

#     if save:
#          fig.savefig('../img/searchs_time_' + save_str)
    
    fig = plt.figure(figsize=(12,4))

    sns.histplot(data = pos_searches[symptom],color=next(palette),bins = 2*int(sqrt(pos_searches.shape[0])))
    sns.histplot(data = neg_searches[symptom],color=next(palette),bins = 2*int(sqrt(pos_searches.shape[0])))

    if save:
         fig.savefig('../img/searchs_hist_' + save_str)

    fig,axs = plt.subplots(1,2,figsize=(7,4))
    lw = 2

    pval = hyp_test(pos_searches, neg_searches, hospital,axs,fig,nh,lw)

    if save:
         fig.savefig('../img/searchs_hist_' + save_str)
         
    return pval