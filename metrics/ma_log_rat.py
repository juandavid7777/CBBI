import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.stats import norm

from api.coinsoto_api import cs_fetch
from metrics.base_metric import BaseMetric
from utils import add_common_markers, mark_highs_lows


class MALogRatMetric(BaseMetric):
    @property
    def name(self) -> str:
        return 'MALogRat'

    @property
    def description(self) -> str:
        return 'Moving Average Log Ratio'

    def _calculate(self, df: pd.DataFrame, ax: list[plt.Axes]) -> pd.Series:  
        
        #----------------------------------------------------------
        
        #6. Defines time (day) parameters for risk. Roll_long cannot be more than 326 as it will exclude the peak
        roll_short = 7
        roll_long = 350 #interesting 140

        #Moving average and risk index generated
        df["MA_short"] = df["Price"].rolling(roll_short).mean()
        df["MA_long"] = df["Price"].rolling(roll_long).mean()

        #Risk according to moving averages
        df["risk_MA"] = np.log(df["MA_short"]/df["MA_long"])

        df["SE_risk_MA"] = df["risk_MA"].expanding().std()
        df["mean_risk_MA"] = df["risk_MA"].expanding().mean()
        
        #Limits
        df['HighModel'] = df["mean_risk_MA"] + 1.96*df["mean_risk_MA"]
        df['LowModel'] = df["mean_risk_MA"] - 1.96*df["mean_risk_MA"]

        #Creates a normalization variable
        df["Index"] = df.apply(lambda x: norm.cdf(x['risk_MA'], x["mean_risk_MA"], x["SE_risk_MA"]),axis = 1)
        
        #----------------------------------------------------------
        df['IndexNoNa'] = df['Index'].fillna(0)
        ax[0].set_title(self.description)
        sns.lineplot(data=df, x='Date', y='IndexNoNa', ax=ax[0])
        add_common_markers(df, ax[0])

        sns.lineplot(data=df, x='Date', y='risk_MA', ax=ax[1])
        sns.lineplot(data=df, x='Date', y='HighModel', ax=ax[1])
        sns.lineplot(data=df, x='Date', y='LowModel', ax=ax[1])
        add_common_markers(df, ax[1], price_line=False)
        
        return df["Index"]