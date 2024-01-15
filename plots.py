import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

def colored_metric(df, metric_name, metric_format, user_role = 0, range_vals = None, color_map = "jet"):
    
    #Defines parameters for blurring users
    user0_days_blurred = 365
    user1_days_blurred = 90
    
    if user_role == 0:
        df = df.copy()
        df.iloc[-user0_days_blurred:] = None
    
    elif user_role == 1:
        df = df.copy()
        df.iloc[-user1_days_blurred:] = None

    if range_vals:
        
        min_lim = range_vals[0]
        low_lim = range_vals[1]
        high_lim = range_vals[2]
        max_lim = range_vals[3]
       
        #Preprocessing inputs
        mid_lim1 = (high_lim - low_lim)*1/3 + low_lim
        mid_lim2 = (high_lim - low_lim)*2/3 + low_lim

        n_low = (low_lim-min_lim)/(max_lim - min_lim)
        n_high = (high_lim-min_lim)/(max_lim - min_lim)
        n_mid1 = (mid_lim1-min_lim) /(max_lim - min_lim)
        n_mid2 = (mid_lim2-min_lim) /(max_lim - min_lim)
    
        color_map = [[0,"green"],[n_low,"greenyellow"], [n_mid1,"lemonchiffon"], [n_mid2,"sandybrown"], [n_high,"lightcoral"], [1,"red"]] #lawngreen, crimson

    fig = go.Figure()

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["close"],
        mode = 'markers',
        name = 'Price',
        customdata = df[metric_name],
        hovertemplate='<br>'.join([
                '$%{y:'+'.1f'+'}',
                metric_name + ': %{customdata:' + metric_format + '}',
            ]),
        marker=dict(size=3,color = df[metric_name],showscale=True, colorbar=dict(title = metric_name), colorscale= color_map),
        ),secondary_y=False)
    
    fig.update_xaxes(range=[df.index[1], df.index[-1]])
    
    dark_theme = "floralWhite"
    
    if user_role == 0:

        fig.update_layout(
            shapes=[dict(
                type="rect",
#                 xref="paper",
                yref="paper",
                x0 = df.index[-user0_days_blurred],
                y0= 0,
                x1= df.index[-1],
                y1= 1,
                fillcolor=dark_theme,
                opacity = 1,
                layer="above",
                line_dash = "solid",
                line_width=3,
                line_color = dark_theme
                )],

            annotations = [dict(
                name="draft watermark",
                text="Bitcointrends",
                textangle=0,
                opacity=0.5,
                font=dict(color="white", size=40, family = "Arial"),
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                )]

                        )
        #Makes the plot static when rendered out
        config = {'staticPlot': True}
        
    elif user_role == 1:

        fig.update_layout(
            shapes=[dict(
                type="rect",
#                 xref="paper",
                yref="paper",
                x0 = df.index[-user1_days_blurred],
                y0= 0,
                x1= df.index[-1],
                y1= 1,
                fillcolor=dark_theme,
                opacity = 1,
                layer="above",
                line_dash = "solid",
                line_width=3,
                line_color = dark_theme
                )],

            annotations = [dict(
                name="draft watermark",
                text="Bitcointrends",
                textangle=0,
                opacity=0.5,
                font=dict(color="white", size=40, family = "Arial"),
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                )]

                        )

        #Makes the plot static when rendered out
        config = {'staticPlot': False}
    
    else:
        fig.update_layout(
            annotations = [dict(
                name="draft watermark",
                text="Bitcointrends",
                textangle=0,
                opacity=0.5,
                font=dict(color="white", size=40, family = "Arial"),
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                )]

                        )
        
        #Makes the plot static when rendered out
        config = {'staticPlot': False}

    #Defines figure properties
    fig.update_layout(
        title = metric_name,
        title_x=0,
        xaxis_title= "Date",
        yaxis_title= "USD/BTC",
        yaxis_type="log",
        coloraxis_colorbar=dict(title="Your Title"),
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        autosize=True,
    )
    
    

    return fig, config