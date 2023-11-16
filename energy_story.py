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

def expander_energy(country):
    
    st.markdown("<h2 style='text-align: center; color: #FACFCE;font-size: xxx-medium'>Share of renewable energy in gross final energy consumption by sector....</h2>", unsafe_allow_html=True)    
    with st.expander('Show Chart', expanded=False):

        db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="research_lab_2022",
        database="data_story"
        )

        cursor = db_connection.cursor()

        my_variable = country

        query = "SELECT * FROM energy_renewable WHERE geo = %s" # Change 'your_column' and the condition as needed


        cursor.execute(query, (my_variable,))

        # Create a Pandas DataFrame from the cursor object
        data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        cursor.close()
        db_connection.close()
        

        filtered_df = pd.DataFrame(data)
        category = st.selectbox("category", filtered_df['category'].unique())
        
        filtered_df = filtered_df[(filtered_df['category'] == category)]

       
        filtered_df.dropna()
        filtered_df.dropna()

        fig = px.line(filtered_df, x='year', y='value', title='Share of renewable energy in gross final energy consumption by sector')
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
        
        fig.update_layout(yaxis_title="share of renewable energy",xaxis_title="")

        fig.update_layout(width=1200)
        st.plotly_chart(fig)
        
        markdown = filtered_df.to_string()
        #markdown = filtered_df.to_markdown()
        prompt = '     Provide summary of above provided Share of renewable energy in gross final energy consumption by sector data in storytelling points briefly in brief important and significant 4 points. Answer format should start directly with 4 points without any title along with brief summary paragraph without title mentioning how this is affecting the economy of the country.'
        final_prompt = markdown + prompt
        result = bard.get_answer(final_prompt)
        st.write(result['content'])
        
        st.button(':information_source:', key=None, help='The indicator measures the share of renewable energy consumption in gross final energy consumption according to the Renewable Energy Directive. The gross final energy consumption is the energy used by end-consumers (final energy consumption) plus grid losses and self-consumption of power plants.')
#------------------------------------------------------------------------------------------------------------------------------------------

    st.markdown("<h2 style='text-align: center; color: #FACFCE;font-size: xxx-medium'>Final energy consumption....</h2>", unsafe_allow_html=True)    
    with st.expander('Show Chart', expanded=False):

        db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="research_lab_2022",
        database="data_story"
        )

        cursor = db_connection.cursor()

        my_variable = country

        query = "SELECT * FROM energy_consumption WHERE geo = %s " # Change 'your_column' and the condition as needed


        cursor.execute(query, (my_variable,))

        # Create a Pandas DataFrame from the cursor object
        data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        cursor.close()
        db_connection.close()

        filtered_df = pd.DataFrame(data)
        unit = st.selectbox("unit", filtered_df['unit'].unique())
        
        filtered_df = filtered_df[(filtered_df['unit'] == unit)]

        filtered_df.dropna()

        fig = px.bar(filtered_df, x="year", y="value", text_auto = True)
        fig.update_traces(textfont_size = 14, textangle = 0, textposition = "inside")


        fig.update_layout(width=1200)

        st.plotly_chart(fig)
        
        markdown = filtered_df.to_string()
        #markdown = filtered_df.to_markdown()
        prompt = '     Provide summary of above provided Final energy consumption data in storytelling points briefly in brief important and significant 4 points. Answer format should start directly with 4 points without any title along with brief summary paragraph without title mentioning how this is affecting the economy of the country.'
        final_prompt = markdown + prompt
        result = bard.get_answer(final_prompt)
        st.write(result['content'])
        
        st.button(':information_source:', key=None, help='The indicator measures the energy end-use in a country excluding all non-energy use of energy carriers (e.g. natural gas used not for combustion but for producing chemicals). “Final energy consumption” only covers the energy consumed by end users, such as industry, transport, households, services and agriculture; it excludes energy consumption of the energy sector itself and losses occurring during transformation and distribution of energy.')
#------------------------------------------------------------------------------------------------------------------------------------------
