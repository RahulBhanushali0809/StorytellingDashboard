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

def expander_trade(country):
    
    st.markdown("<h2 style='text-align: center; color: #FACFCE;font-size: xxx-medium'>Imports of goods and services....</h2>", unsafe_allow_html=True)    
    with st.expander('Show Chart', expanded=False):

        db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="research_lab_2022",
        database="data_story"
        )

        cursor = db_connection.cursor()

        my_variable = country

        query = "SELECT * FROM imp_exp_gns WHERE geo = %s" # Change 'your_column' and the condition as needed


        cursor.execute(query, (my_variable,))

        # Create a Pandas DataFrame from the cursor object
        data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        cursor.close()
        db_connection.close()


        filtered_df = pd.DataFrame(data)

        filtered_df.dropna()

        fig = px.line(filtered_df, x='year', y='value', title='Imports of goods and services', color = 'category')
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
        
        fig.update_layout(yaxis_title="Current prices, million euro",xaxis_title="")

        fig.update_layout(width=1200)
        st.plotly_chart(fig)
        
        markdown = filtered_df.to_string()
        #markdown = filtered_df.to_markdown()
        prompt = '     Provide summary of above provided Imports of goods and services data in storytelling points briefly in brief important and significant 4 points. Answer format should start directly with 4 points without any title along with brief summary paragraph without title mentioning how this is affecting the economy of the country.'
        final_prompt = markdown + prompt
        result = bard.get_answer(final_prompt)
        st.write(result['content'])
        
        st.button(':information_source:', key=None, help='Exports of goods and services consist of transactions in goods and services (sales, barter, and gifts) from residents to non-residents. Imports of goods and services consist of transactions in goods and services (purchases, barter, and gifts) from non-residents to residents. Imports and exports of goods occur when economic ownership of goods changes between residents and non-residents. This applies irrespective of corresponding physical movements of goods across frontiers.')
#------------------------------------------------------------------------------------------------------------------------------------------

    st.markdown("<h2 style='text-align: center; color: #FACFCE;font-size: xxx-medium'>Balance of trade....</h2>", unsafe_allow_html=True)    
    with st.expander('Show Chart', expanded=False):

        db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="research_lab_2022",
        database="data_story"
        )

        cursor = db_connection.cursor()

        my_variable = country

        query = "SELECT geo, value, CONCAT(year, '-', quarter) as date FROM trade_bal WHERE geo = %s " # Change 'your_column' and the condition as needed


        cursor.execute(query, (my_variable,))

        # Create a Pandas DataFrame from the cursor object
        data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        cursor.close()
        db_connection.close()

        filtered_df = pd.DataFrame(data)
       
        filtered_df.dropna()

        fig = px.bar(filtered_df, x="date", y="value", text_auto = True)
        fig.update_traces(textfont_size = 14, textangle = 0, textposition = "inside")


        fig.update_layout(width=1200)

        st.plotly_chart(fig)
        
        markdown = filtered_df.to_string()
        #markdown = filtered_df.to_markdown()
        prompt = '     Provide summary of above provided Balance of trade data in storytelling points briefly in brief important and significant 4 points. Answer format should start directly with 4 points without any title along with brief summary paragraph without title mentioning how this is affecting the economy of the country.'
        final_prompt = markdown + prompt
        result = bard.get_answer(final_prompt)
        st.write(result['content'])
                  
        st.button(':information_source:', key=None, help='The International trade balance indicator is the difference between exports and imports of goods. Exports of goods record flows from an EA/EU Member State to a non-EA/EU country while imports record inwards flows. Exports are expressed in value terms and measured free on board (FOB), while imports are expressed in value terms and measured "cost, insurance, freight" (CIF ). "Goods" means all movable property including electric current. Data are expressed in million euros. Data are presented in the calendar and seasonally adjusted form.')
#------------------------------------------------------------------------------------------------------------------------------------------
