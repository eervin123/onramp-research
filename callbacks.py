import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash
import dash_table
from dash_table.Format import Format, Group, Scheme
import dash_table.FormatTemplate as FormatTemplate
from datetime import datetime as dt
from dash_app import dash_app
import datetime 
import pytz
import math

####################################################################################################
# 000 - FORMATTING INFO
####################################################################################################

####################### Corporate css formatting
corporate_colors = {
    'onramp-dark' : '#131c4f',
    'dark-blue-grey' : '#424972',
    'medium-blue-grey' : '#424972',
    'superdark-green' : '#424972',
    'dark-green' : '#424972',
    'medium-green' : '#b8bbca',
    'light-green' : '#b8bbca',
    'pink-red' : '#00eead',
    'dark-pink-red' : '#00eead',
    'white' : 'rgb(251, 251, 252)',
    'light-grey' : '#b0b6bd'
}
externalgraph_rowstyling = {
    'margin-left' : '15px',
    'margin-right' : '15px'
}

externalgraph_colstyling = {
    'border-radius' : '10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : corporate_colors['superdark-green'],
    'background-color' : corporate_colors['superdark-green'],
    'box-shadow' : '0px 0px 17px 0px rgba(186, 218, 212, .5)',
    'padding-top' : '10px'
}

filterdiv_borderstyling = {
    'border-radius' : '0px 0px 10px 10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : corporate_colors['light-green'],
    'background-color' : corporate_colors['light-green'],
    'box-shadow' : '2px 5px 5px 1px rgba(255, 101, 131, .5)'
    }

navbarcurrentpage = {
    'text-decoration' : 'underline',
    'text-decoration-color' : corporate_colors['pink-red'],
    'text-shadow': '0px 0px 1px rgb(251, 251, 252)'
    }

recapdiv = {
    'border-radius' : '10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : 'rgb(251, 251, 252, 0.1)',
    'margin-left' : '15px',
    'margin-right' : '15px',
    'margin-top' : '15px',
    'margin-bottom' : '15px',
    'padding-top' : '5px',
    'padding-bottom' : '5px',
    'background-color' : 'rgb(251, 251, 252, 0.1)'
    }

recapdiv_text = {
    'text-align' : 'left',
    'font-weight' : '350',
    'color' : corporate_colors['white'],
    'font-size' : '1.5rem',
    'letter-spacing' : '0.04em'
    }

####################### Corporate chart formatting
colors = ['#a90bfe', '#7540ee', '#3fb6dc'] 
corporate_title = {
    'font' : {
        'size' : 16,
        'color' : corporate_colors['white']}
}

corporate_xaxis = {
    'showgrid' : False,
    'linecolor' : corporate_colors['light-grey'],
    'color' : corporate_colors['light-grey'],
    'tickangle' : 330,
    'titlefont' : {
        'size' : 12,
        'color' : corporate_colors['light-grey']},
    'tickfont' : {
        'size' : 11,
        'color' : corporate_colors['light-grey']},
    'zeroline': False,
    
    
}

corporate_yaxis = {
    'showgrid' : True,
    'color' : corporate_colors['light-grey'],
    'gridwidth' : 0.5,
    'gridcolor' : corporate_colors['dark-green'],
    'linecolor' : corporate_colors['light-grey'],
    'titlefont' : {
        'size' : 12,
        'color' : corporate_colors['light-grey']},
    'tickfont' : {
        'size' : 11,
        'color' : corporate_colors['light-grey']},
    'zeroline': False
}

corporate_font_family = 'Circular STD'

corporate_legend = {
    'orientation' : 'h',
    'yanchor' : 'bottom',
    'y' : 1.01,
    'xanchor' : 'right',
    'x' : 1.05,
	'font' : {'size' : 15, 'color' : corporate_colors['light-grey']}
} # Legend will be on the top right, above the graph, horizontally

corporate_margins = {'l' : 5, 'r' : 0, 't' : 45, 'b' : 15}  # Set top margin to in case there is a legend

corporate_layout = go.Layout(
    #font = {'family' : corporate_font_family},
    title = corporate_title,
    title_x = 0.5, # Align chart title to center
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor = 'rgba(0,0,0,0)',
    xaxis = corporate_xaxis,
    yaxis = corporate_yaxis,
    height = 270,
    legend = corporate_legend,
    margin = corporate_margins,
    )

my_template = dict(
    layout=go.Layout(corporate_layout)
)
####################################################################################################
# 000 - DATA MAPPING
####################################################################################################

#Sales mapping

####################################################################################################
# 000 - IMPORT DATA DASHBOARD
####################################################################################################

df = pd.read_csv("datafiles/Slider_data20.csv", usecols = ['Date','TraditionalOnly', 'SP500Only', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13', 'd14', 'd15', 'd16', 'd17', 'd18', 'd19', 'd20', 'd21'], encoding='latin-1')
df['Date'] = pd.to_datetime(df['Date'], unit = 'ms')
df = df.set_index('Date')
#Stats Data
df_stats = pd.read_csv("datafiles/Slider_data20.csv", usecols = ['AnnReturn',	'AnnRisk','SharpeRatio','SortinoRatio','ReturnTraditional','ReturnSP500','RiskTraditional',	'RiskSP500','SharpeTraditional','SharpeSP500','SortinoTraditional',	'SortinoSP500'], encoding='latin-1')
df_stats = df_stats.dropna()

colors = ['#a90bfe', '#7540ee', '#3fb6dc'] 
################################################################################################################################################## 


####################################################################################################
# 000 - IMPORT DATA Other Chart 
####################################################################################################


####################################################################################################
####################################################################################################
####################################################################################################
# Dashboard PAGE
####################################################################################################
####################################################################################################
####################################################################################################

@dash_app.callback(

    [dash.dependencies.Output('pie_chart', 'figure'),
     dash.dependencies.Output('line_chart', 'figure'),
     dash.dependencies.Output('scatter_plot', 'figure'),
     dash.dependencies.Output('bar_chart_rr', 'figure'),
     dash.dependencies.Output('bar_chart_ss', 'figure')],
    [dash.dependencies.Input('slider_num', 'drag_value')]
)
def update_graphs(value):
    #print(value)
    #------------------------------------------------------------------------------Pie Chart ---------------------------------------------------------------------------
    value_dict = {
        0:1,
        .5:2,
        1:3,
        1.5:4,
        2:5,
        2.5:6,
        3:7,
        3.5:8,
        4:9,
        4.5:10,
        5:11,
        5.5:12,
        6:13,
        6.5:14,
        7:15,
        7.5:16,
        8:17,
        8.5:18,
        9:19,
        9.5:20,
        10:21
    }

    
    percent_dict = {'60/40' : 1-float(value)/100, 'Bitcoin': float(value)/100}
    
    #print(value)
    def graph_pie(percent_dictionary):

        colors_pie = ['#a90bfe', '#f2a900'] #BTC Orange
        assets = list(percent_dictionary.keys())

        percents = list(percent_dictionary.values())
        #print(percents)
        
        fig = px.pie( values = percents, names = assets, color = assets,
                                color_discrete_sequence= colors_pie,
                                title="Portfolio Allocation",
                                #width = 400, height = 400 
                                template= my_template,
                                height = 400
                                )
        fig.update_traces(hovertemplate='%{value:.0%}')
        #print("plotly express hovertemplate:", fig.data[0].hovertemplate)
        fig.update_layout(
        font = dict(
            family="Circular STD",
            color="white"
        ),
        title={
            'text': "<b>Portfolio Allocation<b>",
            'y':1,
            'x':0.49,
            'xanchor': 'center',
            'yanchor': 'top'},
        
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-.2,
        xanchor="left",
        x=0.30))
        fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
        fig.update_traces(textfont_size = 17)
        fig.update_layout(titlefont=dict(size =24, color='white'))
        fig.update_layout(margin = dict(l=10, r=20, t=40, b=0))
        
        return fig

    #print(percent_dict)
    value = value_dict[value]
    #print(value)
    #------------------------------------------------------------------------------Line Chart ---------------------------------------------------------------------------
    
    choice = 'd' + str(value)
    def graph_line_chart(df, choice):
        colors = ['#a90bfe', '#7540ee', '#3fb6dc'] 
        df = df[['TraditionalOnly', 'SP500Only', choice]]
        df.columns = ['Traditional Only', 'SP500 Only', "Combined Portfolio"]
        color_dict = {}
        color_dict['Traditional Only'] = colors[0]
        color_dict['SP500 Only'] = colors[1]
        color_dict['Combined Portfolio'] = colors[2]
        
    
        fig = px.line(df, labels={
                                "value": "",
                                "Date": "",
                                "color" : "",
                                "variable": ""
                                },
                        title="Portfolio Performance",
                        color_discrete_map=color_dict,
                        template= my_template,
                        #width = 450
                        )
        
        fig.update_yaxes( # the y-axis is in dollars
            tickprefix="$", showgrid=True
        )
        x = .82
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y= -.5,
            xanchor="right",
            x=.86
        ),
        font = dict(
            family="Roboto",
            color="white"
        ),
        title={
                'text': "<b>Portfolio Performance<b>",
                'y':1,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},)
        fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
        fig.update_yaxes(side = "right", nticks = 4)
        fig.update_layout(titlefont=dict(size =24, color='white', family = 'Circular STD'))
        fig.update_layout(margin = dict(l=0, r=30, t=20, b=0))
        return fig


    #------------------------------------------------------------------------------Scatter Plot ---------------------------------------------------------------------------
    risk_dic = {'60/40': float(df_stats.iloc[0][6])/100, 'S&P 500 Total Return': float(df_stats.iloc[0][7])/100, 'Combined Portfolio': float(df_stats.iloc[value-1][1])/100}
    #print(risk_dic)
    return_dic = {'60/40': float(df_stats.iloc[0][4])/100, 'S&P 500 Total Return': float(df_stats.iloc[0][5])/100, 'Combined Portfolio': float(df_stats.iloc[value-1][0])/100}
    
    def graph_scatter_plot(risk_dic, return_dic):
        colors = ['#a90bfe', '#7540ee', '#3fb6dc'] 
        labels = list(risk_dic.keys())

        xaxis_vol = list(risk_dic.values())
        yaxis_return = list(return_dic.values())


        size_list = [3, 3, 3]
        symbols = [1, 2, 0] #this makes the symbols square diamond and circle in order
        fig = px.scatter( x= xaxis_vol, y= yaxis_return, size = size_list, color = labels, 
                                #color_discrete_sequence=['#A90BFE','#FF7052','#66F3EC', '#67F9AF'],
                                color_discrete_sequence= colors,
                                template= my_template,
                                labels={
                                "x": "Annual Risk",
                                "y": "Annual Return",
                                "color" : "",
                                "symbol": ""

                                },
                                title="Risk vs. Return")
                                #width = 450, height = 450)
        fig.update_xaxes(showgrid = False)
        #print("plotly express hovertemplate:", fig.data[0].hovertemplate)
        fig.update_traces(hovertemplate='Annual Risk = %{x:.0%}<br>Annual Return = %{y:.0%}')
        
        fig.update_layout( 
        title={
            'text': "<b>Risk vs. Return<b>",
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font = dict(
            family="Circular STD",
            color="black"
        ),
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-.5,
        xanchor="left",
        x=0.1
        ))
        fig.update_yaxes(side = "right")
        fig.update_layout({
        'plot_bgcolor': 'rgba(255, 255, 255, 0)',
        'paper_bgcolor': 'rgba(255, 255, 255, 0)',
        })
        fig.update_layout(yaxis_tickformat = '%')
        fig.update_layout(xaxis_tickformat = '%')
        fig.update_layout(titlefont=dict(size =24, color='white'))
        fig.update_xaxes( title_font = {"size": 20})
        fig.update_yaxes( title_font = {"size": 20})
        fig.update_layout(margin = dict(l=10, r=50, t=20, b=0))

        return fig
    
    #------------------------------------------------------------------------------Bar Chart ---------------------------------------------------------------------------

    x_axis_rr = ['Ann. Return', 'Ann. Risk']
    x_axis_ss = ['Sharpe', 'Sortino']
    
    y_combined_rr = [float(df_stats.iloc[value-1][0])/100, float(df_stats.iloc[value-1][1])/100]
    y_6040_rr = [float(df_stats.iloc[0][4])/100, float(df_stats.iloc[0][6])/100]
    y_spy_rr = [float(df_stats.iloc[0][5])/100, float(df_stats.iloc[0][7])/100]

    y_combined_ss = [float(df_stats.iloc[value-1][2])/100, float(df_stats.iloc[value-1][3])/100]
    y_6040_ss = [float(df_stats.iloc[0][8])/100, float(df_stats.iloc[0][10])/100]
    y_spy_ss = [float(df_stats.iloc[0][9])/100, float(df_stats.iloc[0][11])/100]

    def graph_barchart(x_axis_rr_ss, y_combined, y_6040, y_spy):
        
        colors = ['#a90bfe', '#7540ee', '#3fb6dc'] 
        if(x_axis_rr_ss[0] == 'Ann. Return'):
            title = "<b>Ann. Return & Risk<b>"
            max_range = .5
        else:
            title = "<b>Sharpe & Sortino Ratio<b>"
            max_range = .05

        

        x_axis_rr_ss *= 3
        y_vals = []
        y_vals += y_6040
        y_vals += y_spy
        y_vals += y_combined
    
        
        strat = ['60/40 Only', '60/40 Only', 'S&P 500 Total Return', 'S&P 500 Total Return', 'Combined Portfolio', 'Combined Portfolio']

        df = pd.DataFrame(list(zip(x_axis_rr_ss, y_vals, strat)),
                columns =['Type', 'Values', 'Strategy'])
        #print(df)

        fig = px.bar(df, x="Type", y="Values",
                color='Strategy', barmode='group',
                color_discrete_sequence = colors, template= my_template, 
                labels={
                    "Type": "",
                    "Values": "",
                    "Strategy" : ""
                    })
        fig.update_traces(texttemplate='%{y:.2%}', textposition='outside')
        fig.update_layout(uniformtext_minsize=16, uniformtext_mode='hide')
        fig.update_traces(hovertemplate='%{y:.0%}')
        fig.update_yaxes(showticklabels = False)
        fig.update_yaxes(range=[0, max_range])
        fig.update_layout( 
        title={
            'text': title,
            'y': .85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font = dict(
            family="Circular STD",
            color="white"
        ),
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-.3,
        xanchor="left",
        x=0.11
        ),
        barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
        )
        fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
        fig.update_layout(xaxis_tickfont_size=19)
        fig.update_layout(titlefont=dict(size =24, color='white'))
        #fig.update_layout(margin = dict(l=10, r=0, t=100, b=0))

        return fig



    pie_fig     = graph_pie(percent_dict)
    line_fig    = graph_line_chart(df, choice)
    scatter_fig = graph_scatter_plot(risk_dic, return_dic)
    bar_rr_fig  = graph_barchart(x_axis_rr, y_combined_rr, y_6040_rr, y_spy_rr)
    bar_ss_fig  = graph_barchart(x_axis_ss, y_combined_ss, y_6040_ss, y_spy_ss)
    return pie_fig, line_fig, scatter_fig, bar_rr_fig, bar_ss_fig


