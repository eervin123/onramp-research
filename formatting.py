
import plotly.graph_objs as go



####################################################################################################
# 000 - FORMATTING INFO
####################################################################################################

####################### Corporate css formatting
corporate_colors = {
    "onramp-dark": "#131c4f",
    "dark-blue-grey": "#424972",
    "medium-blue-grey": "#424972",
    "superdark-green": "#424972",
    "dark-green": "#424972",
    "medium-green": "#b8bbca",
    "light-green": "#b8bbca",
    "pink-red": "#00eead",
    "dark-pink-red": "#00eead",
    "white": "rgb(251, 251, 252)",
    "light-grey": "#b0b6bd",
}

externalgraph_rowstyling = {"margin-left": "15px", "margin-right": "15px"}

externalgraph_colstyling = {
    "border-radius": "10px",
    "border-style": "solid",
    "border-width": "1px",
    "border-color": corporate_colors["light-grey"],
    "background-color": corporate_colors["onramp-dark"],
    "box-shadow": "0px 0px 17px 0px rgba(186, 218, 212, .5)",
    "padding-top": "10px",
}

filterdiv_borderstyling = {
    "border-radius": "0px 0px 10px 10px",
    "border-style": "solid",
    "border-width": "1px",
    "border-color": "#424972",
    "background-color": "#424972",
    "box-shadow": "2px 5px 5px 1px rgba(255, 101, 131, .5)",
}

navbarcurrentpage = {
    "text-decoration": "underline",
    "text-decoration-color": corporate_colors["pink-red"],
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

recapdiv_text = {
    "text-align": "left",
    "font-weight": "350",
    "color": corporate_colors["white"],
    "font-size": "1.5rem",
    "letter-spacing": "0.04em",
}

####################### Corporate chart formatting

corporate_title = {"font": {"size": 16, "color": corporate_colors["white"]}}

corporate_xaxis = {
    "showgrid": False,
    "linecolor": corporate_colors["light-grey"],
    "color": corporate_colors["light-grey"],
    "tickangle": 315,
    "titlefont": {"size": 12, "color": corporate_colors["light-grey"]},
    "tickfont": {"size": 14, "color": corporate_colors["light-grey"]},
    "zeroline": False,
}

corporate_yaxis = {
    "showgrid": True,
    "color": corporate_colors["light-grey"],
    "gridwidth": 0.5,
    "gridcolor": corporate_colors["dark-green"],
    "linecolor": corporate_colors["light-grey"],
    "titlefont": {"size": 12, "color": corporate_colors["light-grey"]},
    "tickfont": {"size": 11, "color": corporate_colors["light-grey"]},
    "zeroline": False,
}

corporate_font_family = "Circular STD"

corporate_legend = {
    "orientation": "h",
    "yanchor": "bottom",
    "y": 1.01,
    "xanchor": "right",
    "x": 1.05,
    "font": {"size": 13, "color": corporate_colors["light-grey"]},
}  # Legend will be on the top right, above the graph, horizontally

corporate_margins = {
    "l": 5,
    "r": 5,
    "t": 45,
    "b": 15,
}  # Set top margin to in case there is a legend

corporate_layout = go.Layout(
    font={"family": corporate_font_family},
    title=corporate_title,
    title_x=0.5,  # Align chart title to center
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=corporate_xaxis,
    yaxis=corporate_yaxis,
    height=270,
    legend=corporate_legend,
    margin=corporate_margins,
)

my_template = dict(layout=go.Layout(corporate_layout))

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