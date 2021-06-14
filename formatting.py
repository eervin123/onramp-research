
import plotly.graph_objs as go



####################################################################################################
# 000 - FORMATTING INFO
####################################################################################################

onramp_colors = {
    "dark_blue" : "#131C4F",
    "seafoam"   : "#00EEAD",
    "gray"      : "#B0B6BD",
    "light_blue": "#2F61D5",
    "pink"      : "#A90BFE",
    "purple"    : "#7540EE",
    "cyan"      : "#3FB6DC",
    "orange"    : "#FF7052",
    "white"     : "white",
    "btc"       : "#f2a900"
}

externalgraph_rowstyling = {"margin-left": "15px", "margin-right": "15px"}

externalgraph_colstyling = {
    "border-radius": "10px",
    "border-style": "solid",
    "border-width": "1px",
    "border-color": onramp_colors["gray"],
    "background-color": onramp_colors["dark_blue"],
    "box-shadow": "0px 0px 17px 0px rgba(186, 218, 212, .5)",
    "padding-top": "10px",
}

navbarcurrentpage = {
    "text-decoration": "underline",
    "text-decoration-color": onramp_colors["seafoam"],
    "text-shadow": "0px 0px 1px rgb(251, 251, 252)",
    "font-family": "Circular STD",
}

recapdiv = {
    "border-radius": "10px",
    "border-style": "solid",
    "border-width": "1px",
    "border-color": "#424972",
    "margin-left": "15px",
    "margin-right": "15px",
    "margin-top": "15px",
    "margin-bottom": "15px",
    "padding-top": "5px",
    "padding-bottom": "5px",
    "background-color": "rgb(251, 251, 252, 0.1)",  # behind slider
}


onramp_title = {"font": {"size": 20, "color": onramp_colors["gray"]}}

onramp_xaxis = {
    "showgrid": False,
    "linecolor": onramp_colors["gray"],
    "color": onramp_colors["gray"],
    "tickangle": 0,
    "titlefont": {"size": 16, "color": onramp_colors["gray"]},
    "tickfont": {"size": 14, "color": onramp_colors["gray"]},
    "zeroline": False,
}

onramp_yaxis = {
    "showgrid": False,
    "color": onramp_colors["gray"],
    "gridwidth": 0.5,
    "gridcolor": onramp_colors["gray"],
    "linecolor": onramp_colors["gray"],
    "titlefont": {"size": 16, "color": onramp_colors["gray"]},
    "tickfont": {"size": 14, "color": onramp_colors["gray"]},
    "zeroline": False,
}
onramp_font_family = "Roboto"

onramp_legend = {
    "orientation": "h",
    "yanchor": "bottom",
    "y": -.3,
    "xanchor": "left",
    "x": 0,
    "font": {"size": 17, "color": onramp_colors["gray"]},
}  # Legend will be on the bottom middle

onramp_margins = {
    "l": 40,
    "r": 20,
    "t": 10,
    "b": 120,
}  # Set top margin to in case there is a legend


onramp_layout = go.Layout(
    colorway= [onramp_colors["btc"], onramp_colors["white"], onramp_colors["cyan"], '#B0B6BD', onramp_colors["pink"], onramp_colors["purple"], onramp_colors["light_blue"], onramp_colors["orange"]],
    font = {'family' : onramp_font_family},
    title=onramp_title,
    title_x=0.5, # Align chart title to center
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=onramp_xaxis,
    yaxis=onramp_yaxis,
    #height=200,
    legend=onramp_legend,
    margin=onramp_margins,
)


onramp_template = dict(layout=go.Layout(onramp_layout))

#----------------------------Second Template for graphs which need legends inside them

onramp_legend_dashboard = {
    "orientation": "v",
    "yanchor": "top",
    "y": 1,
    "xanchor": "left",
    "x": .04,
    "font": {"size": 17, "color": onramp_colors["gray"]},
}  # Legend will be on the bottom middle

onramp_layout_dashboard = go.Layout(
    colorway= [onramp_colors["btc"], onramp_colors["white"], onramp_colors["cyan"], '#B0B6BD'],
    font = {'family' : onramp_font_family},
    title=onramp_title,
    title_x=0.5, # Align chart title to center
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=onramp_xaxis,
    yaxis=onramp_yaxis,
    #height=200,
    legend=onramp_legend_dashboard,
    margin=onramp_margins,
)

onramp_template_dashboard = dict(layout=go.Layout(onramp_layout_dashboard))

custom_scale = [
    # Let first 10% (0.1) of the values have color rgb(0, 0, 0)
    [0, "#3FB6DC"],
    [0.1, "#3FB6DC"],
    # Let values between 10-20% of the min and max of z
    # have color rgb(20, 20, 20)
    [0.1, "#3FA3D8"],
    [0.2, "#3FA3D8"],
    # Values between 20-30% of the min and max of z
    # have color rgb(40, 40, 40)
    [0.2, "#4090D5"],
    [0.3, "#4090D5"],
    [0.3, "#407ED1"],
    [0.4, "#407ED1"],
    [0.4, "#406BCD"],
    [0.5, "#406BCD"],
    [0.5, "#4158CA"],
    [0.6, "#4158CA"],
    [0.6, "#4145C6"],
    [0.7, "#4145C6"],
    [0.7, "#4133C2"],
    [0.8, "#4133C2"],
    [0.8, "#4220BF"],
    [0.9, "#4220BF"],
    [0.9, "#420DBB"],
    [1.0, "#420DBB"],
]