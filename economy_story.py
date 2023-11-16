import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
from bardapi import Bard
import os
from bardapi import BardCookies
from bard_cookies import cookie_dict
#st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")
st.markdown('<style src="style.css"></style>', unsafe_allow_html=True)

# cookie_dict = {
#     "__Secure-1PSID": "dAi142-wOcJQ-WIXxztDSDWqGuk-poaOdgWCLlV_6sXjxEBe5YjUGJl3yVyuLhd8fXdnIA.",
#     "__Secure-1PSIDTS": "sidts-CjIBNiGH7khRPIUJDQofUNCGfvTMgXxWHq2BIB24xO9ntcRawh3opJmNPJ6a4scCaoigThAA",
#         # Any cookie values you want to pass session object.
# }
cookie_dict = cookie_dict
bard = BardCookies(cookie_dict=cookie_dict)

def expander_economy(country):
    
    st.markdown("<h2 style='text-align: center; color: #FACFCE;font-size: xxx-medium'>HICP - annual data (average index and rate of change)....</h2>", unsafe_allow_html=True)    
    with st.expander('Show Chart', expanded=False):

        db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="research_lab_2022",
        database="data_story"
        )

        cursor = db_connection.cursor()

        my_variable = country

        query = "SELECT * FROM hcip WHERE (geo = %s || geo = 'European Union - 27 countries (from 2020)')" # Change 'your_column' and the condition as needed


        cursor.execute(query, (my_variable,))

        # Create a Pandas DataFrame from the cursor object
        data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        cursor.close()
        db_connection.close()
        

        filtered_df = pd.DataFrame(data)
        category = st.selectbox("category", filtered_df['category'].unique())
        
        filtered_df = filtered_df[(filtered_df['category'] == category)]

       
        filtered_df.dropna()
        color_map = {'European Union - 27 countries (from 2020)': '#F2E3D5'}

        fig = px.line(filtered_df, x='year', y='value', title='HICP - annual data', color = 'geo', color_discrete_map=color_map)
        fig.update_xaxes(
            dtick="M1",
            tickformat="%Y-%b",
            showline=True,
            showgrid=False,
            showticklabels=True,
            tickangle=0,
            tickfont=dict(size=10),


        )
        
        fig.add_vrect(x0="2019", x1="2020", 
              annotation_text="Start of<br>COVID-19<br>Period", annotation_position="top right",  
              annotation_font_size=11,
              annotation_font_color="#F2E3D5",
              fillcolor="orange", opacity=0.25, line_width=0)
        
        fig.update_layout(yaxis_title="Annual average index",xaxis_title="")

        fig.update_layout(width=1200)
        st.plotly_chart(fig)
        
        markdown = filtered_df.to_string()
        #markdown = filtered_df.to_markdown()
        prompt = '     Provide summary of above provided HICP - annual data (average index and rate of change) data in storytelling points briefly in brief important and significant 4 points. Answer format should start directly with 4 points without any title along with brief summary paragraph without title mentioning how this is affecting the economy of the country.'
        final_prompt = markdown + prompt
        result = bard.get_answer(final_prompt)
        st.write(result['content'])
        
        st.button(':information_source:', key=None, help='HICP - annual data (average index and rate of change)')
#------------------------------------------------------------------------------------------------------------------------------------------

    st.markdown("<h2 style='text-align: center; color: #FACFCE;font-size: xxx-medium'>Real GDP per capita....</h2>", unsafe_allow_html=True)    
    with st.expander('Show Chart', expanded=False):

        db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="research_lab_2022",
        database="data_story"
        )

        cursor = db_connection.cursor()

        my_variable = country

        query = "SELECT * FROM real_gdp_per_capita WHERE geo = %s " # Change 'your_column' and the condition as needed


        cursor.execute(query, (my_variable,))

        # Create a Pandas DataFrame from the cursor object
        data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        cursor.close()
        db_connection.close()

        filtered_df = pd.DataFrame(data)
        unit = st.selectbox("unit", filtered_df['unit'].unique())
        
        filtered_df = filtered_df[(filtered_df['unit'] == unit)]

        filtered_df.dropna()
        
        # Define a custom color scale
        color_scale = ['#FF0000',  # Red for negative values 
                       '#00FF00']  # Green for positive values
        
        fig = px.bar(filtered_df, x="year", y="value",color="value",
             color_continuous_scale=color_scale, text_auto = True)
        fig.update_traces(textfont_size = 14, textangle = 0, textposition = "inside")

        fig.update_layout(coloraxis_showscale=True)  # Hide the color bar
        fig.update_layout(width=1200)

        st.plotly_chart(fig)
        
        markdown = filtered_df.to_string()
        #markdown = filtered_df.to_markdown()
        prompt = '     Provide summary of above provided Real GDP per capita data in storytelling points briefly in brief important and significant 4 points. Answer format should start directly with 4 points without any title along with brief summary paragraph without title mentioning how this is affecting the economy of the country.'
        final_prompt = markdown + prompt
        result = bard.get_answer(final_prompt)
        st.write(result['content'])
              
        st.button(':information_source:', key=None, help='The indicator is calculated as the ratio of real GDP to the average population of a specific year. GDP measures the value of total final output of goods and services produced by an economy within a certain period of time. It includes goods and services that have markets (or which could have markets) and products which are produced by general government and non-profit institutions. It is a measure of economic activity and is also used as a proxy for the development in a country’s material living standards. However, it is a limited measure of economic welfare. For example, neither does GDP include most unpaid household work nor does GDP take account of negative effects of economic activity, like environmental degradation.')
#------------------------------------------------------------------------------------------------------------------------------------------
