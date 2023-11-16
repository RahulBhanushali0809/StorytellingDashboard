#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import streamlit as st
st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide",initial_sidebar_state="collapsed")

# In[105]:
import requests
#import eurostat
import pandas as pd
import streamlit as st
#from streamlit_option_menu import streamlit_option_menu
from streamlit.components.v1 import html
import pandas as pd
from ipyvizzu import Chart, Data, Config, Style
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from ipyvizzu import Chart, Data, Config, Style, DisplayTarget
from ipyvizzustory import Story, Slide, Step
from labor_story import expander_labor
from trade_story import expander_trade
from economy_story import expander_economy
from energy_story import expander_energy
from household_story import expander_household
from population_story import expander_population

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# Create a list of options
options = ['Germany',
 'Austria',
 'Belgium',
 'Bulgaria',
 'Croatia',
 'Cyprus',
 'Czechia',
 'Denmark',
 'Estonia',
 'Finland',
 'France',
 'Greece',
 'Hungary',
 'Ireland',
 'Italy',
 'Latvia',
 'Lithuania',
 'Luxembourg',
 'Malta',
 'Netherlands',
 'Poland',
 'Portugal',
 'Romania',
 'Slovakia',
 'Slovenia',
 'Spain',
 'Sweden']

# Create a sidebar filter with a default selection
selected_option = st.sidebar.selectbox("Select an option", options, index=0)


# Create a Streamlit app
def main():
    # Set the default selection to the first option
    selected_option = st.sidebar.selectbox("Select an option:", options, index=0)

    
country_text_color = "#F2A679"
st.markdown(f"<h1 style='text-align: center; color: #145DA0; font-size: xxx-Large'>Let's analyze Economy of <span style='color:{country_text_color}'>{selected_option}</span> for the past decade.</h1>", unsafe_allow_html=True)    
    
selected = option_menu(
            menu_title=None,  # required
            options=["Labor","Trade","Economy","Population","Energy & Carbon Footprint","Household Consumption"],  # required
            #icons=["house", "book", "envelope"],  # optional
            #menu_icon="cast",  # optional
            #default_index=0,  # optional
            orientation="horizontal",
        )




if selected == "Labor":
    expander_labor(selected_option)
if selected == "Trade":
    expander_trade(selected_option)
if selected == "Economy":
    expander_economy(selected_option)
if selected == "Population":
    expander_population(selected_option)
if selected == "Energy & Carbon Footprint":
    expander_energy(selected_option)
if selected == "Household Consumption":
    expander_household(selected_option)
