# modules
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import scipy.stats as stats
from math import sqrt

warnings.filterwarnings('ignore')
import seaborn as sns
from math import sqrt
import matplotlib.pyplot as plt
import scipy.stats as stats

def hyp_test(pos_searches, neg_searches, hospital,axs,fig,nh,lw):

	inds = list([e in list(pos_searches['date']) for e in list(hospital['date'])])
	pos_search_hosp = hospital.iloc[inds]

	sns.histplot(ax = axs[0],data = pos_search_hosp[nh],color=sns.color_palette("hls",5)[2],bins = int(sqrt(pos_searches.shape[0])))
	sns.histplot(kde = True,ax = axs[0],data = pos_search_hosp[nh],color='r',bins = int(sqrt(pos_searches.shape[0])))

	axs[0].set_title('New Hospitalizations for (+) Search Change')
	axs[0].set_xlabel('Daily Hospitalized Change')

	inds = list([e in list(neg_searches['date']) for e in list(hospital['date'])])
	neg_search_hosp = hospital.iloc[inds]

	sns.histplot(ax = axs[1],data = neg_search_hosp[nh],color=sns.color_palette("hls",5)[3],bins = int(sqrt(neg_searches.shape[0])))
	sns.histplot(kde = True,ax = axs[1],data = neg_search_hosp[nh],color='r',bins = int(sqrt(neg_searches.shape[0])))

	plt.setp(axs[0].lines,linewidth=lw)
	plt.setp(axs[1].lines,linewidth=lw)

	axs[1].set_title('New Hospitalizations for (-) Search Change')
	axs[1].set_xlabel('Daily Hospitalized Change')


	_,pval = stats.ttest_ind(pos_search_hosp[nh], neg_search_hosp[nh], axis=0, equal_var=True, nan_policy='omit', alternative='two-sided')
	pval = round(pval,3)
	print(f'pvalue = {pval}')


	plt.suptitle(f'Welch\'s two-sided t-test, p-value = {pval}')
	fig.tight_layout()
	plt.show()
	
	return pval