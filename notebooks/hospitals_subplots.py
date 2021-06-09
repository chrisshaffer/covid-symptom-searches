import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def hospitals_subplots(hospital_by_date,ys,ylabels,color_codes,palette,axs):
    for i in range(len(ys)):
        if color_codes[i] == 'next':
            color = next(palette)
        else:
            color = color_codes[i]
            
        sns.lineplot(x = "date", y = ylabels[i], 
                    data = hospital_by_date,
                    color=color, ax = axs[i])

        plt.xticks(rotation=80)

        xtick_range = range(0,len(hospital_by_date.index),56)
        axs[i].set_title(ylabels[i] + ' by Date')
        if i == len(ys)-1:
            axs[i].set_xticks(xtick_range) # <--- set the ticks first
            axs[i].set_xlabel('Date', labelpad=15)
        else:
            axs[i].set_xticks([])
            axs[i].set_xlabel('')
            
    # ax.set_xlim(xlims[0],xlims[1])
        axs[i].set_ylabel('Count (/day)', labelpad=15)