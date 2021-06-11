import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def hospitals_subplots(hospital_by_date,ys,ylabels,color_codes,palette):
    for i in range(len(ys)):
        if color_codes[i] == 'next':
            color = next(palette)
        else:
            color = color_codes[i]
        ax = plt.subplot(3,1,i+1)
        g = sns.lineplot(x = "date", y = ylabels[i], 
                    data = hospital_by_date,
                    color=color)
        plt.xticks(rotation=90)

        xtick_range = range(0,len(hospital_by_date.index),14)
        ax.set_title(ylabels[i] + ' by Date')
        if i == len(ys)-1:
            ax.set_xticks(xtick_range) # <--- set the ticks first
            ax.set_xlabel('Date', labelpad=15)
        else:
            ax.set_xticks([])
            ax.set_xlabel('')
            
    # ax.set_xlim(xlims[0],xlims[1])
    ax.set_ylabel('Count (/day)', labelpad=15)