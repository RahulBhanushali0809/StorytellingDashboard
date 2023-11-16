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

def expander_household(country):
    
    st.markdown("<h2 style='text-align: center; color: #FACFCE;font-size: xxx-medium'>Final consumption expenditure of households, by consumption purpose.....</h2>", unsafe_allow_html=True)    
    with st.expander('Show Chart', expanded=False):

        db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="research_lab_2022",
        database="data_story"
        )

        cursor = db_connection.cursor()

        my_variable = country

        query = "SELECT * FROM consume_expend_household WHERE geo = %s || geo = 'European Union - 27 countries (from 2020)'" # Change 'your_column' and the condition as needed


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

        fig = px.line(filtered_df, x='year', y='value', title='Final consumption expenditure of households, by consumption purpose', color = 'geo', color_discrete_map=color_map)
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
        
        fig.update_layout(yaxis_title="Final consumption",xaxis_title="")
        
        fig.update_traces(line=dict(dash='dash'), selector=dict(name ='European Union - 27 countries (from 2020)'))

        fig.update_layout(width=1200)
        st.plotly_chart(fig)
        
        markdown = filtered_df.to_string()
        #markdown = filtered_df.to_markdown()
        #prompt = '     Provide summary of above provided Final consumption expenditure of households, by consumption purpose data in storytelling points briefly in brief important and significant 4 points. Answer format should start directly with 4 points without any title along with brief summary paragraph without title mentioning how this is affecting the economy of the country.'

        
        prompt = '     Provide summary of above provided Final consumption expenditure of households, by consumption purpose data in storytelling points briefly in brief important and significant 4 points. Answer format should start directly with 4 points without any title along with brief summary paragraph without title mentioning how countrys economic position is excellent but deteriorating due to this indicator with corresponding data'
        
        
           
        final_prompt = markdown + prompt
        result = bard.get_answer(final_prompt)
        st.write(result['content'])
        
        st.button(':information_source:', key=None, help='Household expenditure refers to any spending done by a person living alone or by a group of people living together in shared accommodation and with common domestic expenses. It includes expenditure incurred on the domestic territory (by residents and non-residents) for the direct satisfaction of individual needs and covers the purchase of goods and services, the consumption of own production (such as garden produce) and the imputed rent of owner-occupied dwellings.')
#------------------------------------------------------------------------------------------------------------------------------------------

    st.markdown("<h2 style='text-align: center; color: #FACFCE;font-size: xxx-medium'>Confidence indicators by sector....</h2>", unsafe_allow_html=True)    
    with st.expander('Show Chart', expanded=False):

        db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="research_lab_2022",
        database="data_story"
        )

        cursor = db_connection.cursor()

        my_variable = country

        query = "SELECT indicator, geo,value, CONCAT(year, '-', month) as date FROM confidence_by_sector WHERE geo = %s " # Change 'your_column' and the condition as needed


        cursor.execute(query, (my_variable,))

        # Create a Pandas DataFrame from the cursor object
        data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        cursor.close()
        db_connection.close()

        filtered_df = pd.DataFrame(data)
        indicator = st.selectbox("indicator", filtered_df['indicator'].unique())
        
        filtered_df = filtered_df[(filtered_df['indicator'] == indicator)]

        filtered_df.dropna()

        fig = px.bar(filtered_df, x="date", y="value", text_auto = True)
        fig.update_traces(textfont_size = 14, textangle = 0, textposition = "inside")


        fig.update_layout(width=1200)

        st.plotly_chart(fig)
        
        markdown = filtered_df.to_string()
        #markdown = filtered_df.to_markdown()
        prompt = '     Provide summary of above provided Confidence indicators by sector data in storytelling points briefly in brief important and significant 4 points. Answer format should start directly with 4 points without any title along with brief summary paragraph without title mentioning how countrys economic position is excellent but deteriorating due to this indicator with corresponding data'
        final_prompt = markdown + prompt
        result = bard.get_answer(final_prompt)
        st.write(result['content'])
        
        st.button(':information_source:', key=None, help='Five monthly confidence indicators for the sectors industry, services, retail trade, construction and consumers are produced by the Directorate General for Economic and Financial Affairs (DG ECFIN) of the European Commission to reflect economic perceptions and expectations. The surveys are implemented in the European Union (EU) and in the candidate countries, and addressed to representatives of the industry (manufacturing), services, retail trade and construction sectors, as well as to consumers. Confidence indicators are produced as arithmetic average of the (seasonally adjusted) balances of answers to selected questions chosen from the whole set of questions in each individual survey; balances series are the difference between positive and negative answering options, measured as percentage points of total answers. Monthly confidence indicators are produced monthly at country, EU and euro area level for all sectors but financial services, which covers the EU and the euro area only. Data are seasonally adjusted (SA). For more details on the methods used by DG ECFIN in the computation of confidence indicators, please refer to the user guide of The Joint Harmonised EU Programme of Business and Consumer Surveys. Source: DG ECFIN')
#------------------------------------------------------------------------------------------------------------------------------------------

    st.markdown("<h2 style='text-align: center; color: #FACFCE;font-size: xxx-medium'>Gross debt-to-income ratio of households....</h2>", unsafe_allow_html=True)    
    with st.expander('Show Chart', expanded=False):

        db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="research_lab_2022",
        database="data_story"
        )

        cursor = db_connection.cursor()

        my_variable = country

        query = "SELECT * FROM debt_income_ratio_household WHERE geo = %s || geo = 'European Union - 27 countries (from 2020)'" # Change 'your_column' and the condition as needed


        cursor.execute(query, (my_variable,))

        # Create a Pandas DataFrame from the cursor object
        data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        cursor.close()
        db_connection.close()

        filtered_df = pd.DataFrame(data)
        
        filtered_df.dropna()
        
        
        color_map = {'European Union - 27 countries (from 2020)': '#F2E3D5'}

        fig = px.line(filtered_df, x='year', y='value', title='Gross debt-to-income ratio of households', color = 'geo', color_discrete_map=color_map)
        fig.update_xaxes(
            dtick="M1",
            tickformat="%Y-%b",
            showline=True,
            showgrid=False,
            showticklabels=True,
            tickangle=0,
            tickfont=dict(size=10),


        )
        fig.update_traces(line=dict(dash='dash'), selector=dict(name ='European Union - 27 countries (from 2020)'))
        
        fig.add_vrect(x0="2019", x1="2020", 
              annotation_text="Start of<br>COVID-19<br>Period", annotation_position="top right",  
              annotation_font_size=11,
              annotation_font_color="#F2E3D5",
              fillcolor="orange", opacity=0.25, line_width=0)
        
        fig.update_layout(yaxis_title="Gross debt-to-income ratio",xaxis_title="")

        
        
#         fig = px.bar(filtered_df, x="year", y="value", text_auto = True)
#         fig.update_traces(textfont_size = 14, textangle = 0, textposition = "inside")


        fig.update_layout(width=1200)

        st.plotly_chart(fig)
        
        markdown = filtered_df.to_string()
        #markdown = filtered_df.to_markdown()
        prompt = '     Provide summary of above provided Gross debt-to-income ratio of households data in storytelling points briefly in brief important and significant 4 points. Answer format should start directly with 4 points without any title along with brief summary paragraph without title mentioning how countrys economic position is excellent but deteriorating due to this indicator with corresponding data'
        
        
        # Input box for user prompt
        #prompt = st.text_area("Enter your prompt:")
        #final_prompt = markdown + prompt

        # Submit button
#         if st.button("Submit"):
#             if prompt:
#                 # Generate and display response
#                 result = bard.get_answer(final_prompt)
#                 #st.success("Model Response:")
#                 st.write(result['content'])
#             else:
#                 st.warning("Please enter a prompt.")
        
        
        final_prompt = markdown + prompt
        result = bard.get_answer(final_prompt)
        st.write(result['content'])
        
        st.button(':information_source:', key=None, help='Gross debt-to-income ratio of households (including Non-Profit Institutions Serving Households) is defined as loans (ESA 2010 code: AF4), liabilities divided by gross disposable income (B6G) with the latter being adjusted for the net change in pension entitlements (D8net). Detailed data and methodology on site http://ec.europa.eu/eurostat/sectoraccounts.')
#-----------------------------------------------------------------------------------------------------------------------------------------