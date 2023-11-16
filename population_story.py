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


def expander_population(country):
    
    st.markdown("<h2 style='text-align: center; color: #FACFCE;font-size: xxx-medium'>Population by age group....</h2>", unsafe_allow_html=True)    
    with st.expander('Show Chart', expanded=False):

        db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="research_lab_2022",
        database="data_story"
        )

        cursor = db_connection.cursor()

        my_variable = country

        query = "SELECT * FROM pop_age WHERE (geo = %s || geo = 'European Union - 27 countries (from 2020)')" # Change 'your_column' and the condition as needed


        cursor.execute(query, (my_variable,))

        # Create a Pandas DataFrame from the cursor object
        data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        cursor.close()
        db_connection.close()
        

        filtered_df = pd.DataFrame(data)
        age = st.selectbox("age", filtered_df['age'].unique())
        
        filtered_df = filtered_df[(filtered_df['age'] == age)]

       
        filtered_df.dropna()
        color_map = {'European Union - 27 countries (from 2020)': '#F2E3D5'}

        fig = px.line(filtered_df, x='year', y='value', title='Population by age group', color = 'geo', color_discrete_map=color_map)
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
        
        fig.update_layout(yaxis_title="Share of population",xaxis_title="")

        fig.update_layout(width=1200)
        st.plotly_chart(fig)
        
        markdown = filtered_df.to_string()
        #markdown = filtered_df.to_markdown()
        prompt = '     Provide summary of above provided Population by age group data in storytelling points briefly in brief important and significant 4 points. Answer format should start directly with 4 points without any title along with brief summary paragraph without title   mentioning how this is affecting the economy of the country.'
        final_prompt = markdown + prompt
        result = bard.get_answer(final_prompt)
        st.write(result['content'])
        
        st.button(':information_source:', key=None, help='Share of population in a certain age group compared to the total population.')
#------------------------------------------------------------------------------------------------------------------------------------------

    st.markdown("<h2 style='text-align: center; color: #FACFCE;font-size: xxx-medium'>Life expectancy at birth by sex....</h2>", unsafe_allow_html=True)    
    with st.expander('Show Chart', expanded=False):

        db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="research_lab_2022",
        database="data_story"
        )

        cursor = db_connection.cursor()

        my_variable = country

        query = "SELECT * FROM life_expect WHERE geo = %s " # Change 'your_column' and the condition as needed


        cursor.execute(query, (my_variable,))

        # Create a Pandas DataFrame from the cursor object
        data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        cursor.close()
        db_connection.close()

        filtered_df = pd.DataFrame(data)
        sex = st.selectbox("sex", filtered_df['sex'].unique())
        
        filtered_df = filtered_df[(filtered_df['sex'] == sex)]

        filtered_df.dropna()

        fig = px.bar(filtered_df, x="year", y="value", text_auto = True)
        fig.update_traces(textfont_size = 14, textangle = 0, textposition = "inside")


        fig.update_layout(width=1200)

        st.plotly_chart(fig)
        
        markdown = filtered_df.to_string()
        #markdown = filtered_df.to_markdown()
        prompt = '     Provide summary of above provided Life expectancy at birth by sex data in storytelling points briefly taking into account of COVID pandemic impact in brief important and significant 4 points. Answer format should start directly with 4 points without any title along with brief summary paragraph without title mentioning how this is affecting the economy of the country.'
        final_prompt = markdown + prompt
        result = bard.get_answer(final_prompt)
        st.write(result['content'])
        
        st.button(':information_source:', key=None, help='Life expectancy at birth is defined as the mean number of years that a new-born child can expect to live if subjected throughout his life to the current mortality conditions (age specific probabilities of dying).')
#------------------------------------------------------------------------------------------------------------------------------------------

    st.markdown("<h2 style='text-align: center; color: #FACFCE;font-size: xxx-medium'>Old-age-dependency ratio....</h2>", unsafe_allow_html=True)    
    with st.expander('Show Chart', expanded=False):

        db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="research_lab_2022",
        database="data_story"
        )

        cursor = db_connection.cursor()

        my_variable = country

        query = "SELECT * FROM old_age_depend_ratio WHERE geo = %s " # Change 'your_column' and the condition as needed


        cursor.execute(query, (my_variable,))

        # Create a Pandas DataFrame from the cursor object
        data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        cursor.close()
        db_connection.close()

        filtered_df = pd.DataFrame(data)
        
        filtered_df.dropna()

        fig = px.bar(filtered_df, x="year", y="value", text_auto = True)
        fig.update_traces(textfont_size = 14, textangle = 0, textposition = "inside")


        fig.update_layout(width=1200)

        st.plotly_chart(fig)
        
        markdown = filtered_df.to_string()
        #markdown = filtered_df.to_markdown()
        prompt = '     Provide summary of above provided Old-age-dependency ratio data in storytelling points briefly taking into account of COVID pandemic impact in brief important and significant 4 points. Answer format should start directly with 4 points without any title along with brief summary paragraph without title mentioning how this is affecting the economy of the country.'
        final_prompt = markdown + prompt
        result = bard.get_answer(final_prompt)
        st.write(result['content'])
        
        st.button(':information_source:', key=None, help='This indicator is the ratio between the number of persons aged 65 and over (age when they are generally economically inactive) and the number of persons aged between 15 and 64. The value is expressed per 100 persons of working age (15-64).')
#-----------------------------------------------------------------------------------------------------------------------------------------

    st.markdown("<h2 style='text-align: center; color: #FACFCE;font-size: xxx-medium'>Projected old-age dependency ratio....</h2>", unsafe_allow_html=True)    
    with st.expander('Show Chart', expanded=False):

        db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="research_lab_2022",
        database="data_story"
        )

        cursor = db_connection.cursor()

        my_variable = country

        query = "SELECT * FROM old_age_depend_ratio_proj WHERE (geo = %s || geo = 'European Union - 27 countries (from 2020)') && year BETWEEN 2022 and 2032" # Change 'your_column' and the condition as needed


        cursor.execute(query, (my_variable,))

        # Create a Pandas DataFrame from the cursor object
        data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        cursor.close()
        db_connection.close()
        

        filtered_df = pd.DataFrame(data)
        projection = st.selectbox("projection", filtered_df['projection'].unique())
        
        filtered_df = filtered_df[(filtered_df['projection'] == projection)]

       
        filtered_df.dropna()
        color_map = {'European Union - 27 countries (from 2020)': '#F2E3D5'}

        fig = px.line(filtered_df, x='year', y='value', title='Projected old-age dependency ratio', color = 'geo', color_discrete_map=color_map)
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
        
        fig.update_layout(yaxis_title="Old-age dependency ratio",xaxis_title="")
        
        
        fig.update_layout(width=1200)
        st.plotly_chart(fig)
        
        markdown = filtered_df.to_string()
        #markdown = filtered_df.to_markdown()
        prompt = '     Provide summary of above provided Projected old-age dependency ratio data in storytelling points briefly taking into account of COVID pandemic impact in brief important and significant 4 points. Answer format should start directly with 4 points without any title along with brief summary paragraph without title mentioning how this is affecting the economy of the country.'
        final_prompt = markdown + prompt
        result = bard.get_answer(final_prompt)
        st.write(result['content'])
        
        st.button(':information_source:', key=None, help='This indicator is the ratio between the projected number of persons aged 65 and over (age when they are generally economically inactive) and the projected number of persons aged between 15 and 64. The value is expressed per 100 persons of working age (15-64).')
#------------------------------------------------------------------------------------------------------------------------------------------

    st.markdown("<h2 style='text-align: center; color: #FACFCE;font-size: xxx-medium'>Total fertility rate....</h2>", unsafe_allow_html=True)    
    with st.expander('Show Chart', expanded=False):

        db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="research_lab_2022",
        database="data_story"
        )

        cursor = db_connection.cursor()

        my_variable = country

        query = "SELECT * FROM fert_rate WHERE geo = %s " # Change 'your_column' and the condition as needed


        cursor.execute(query, (my_variable,))

        # Create a Pandas DataFrame from the cursor object
        data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        cursor.close()
        db_connection.close()

        filtered_df = pd.DataFrame(data)
        
        filtered_df.dropna()

        fig = px.line(filtered_df, x="year", y="value")
        fig.update_xaxes(
            dtick="M1",
            tickformat="%Y-%b",
            showline=True,
            showgrid=False,
            showticklabels=True,
            tickangle=0,
            tickfont=dict(size=10),


        )
        
        
        
        fig.update_layout(yaxis_title="Total fertility rate",xaxis_title="")

        fig.update_layout(width=1200)

        st.plotly_chart(fig)
        
        markdown = filtered_df.to_string()
        #markdown = filtered_df.to_markdown()
        prompt = '     Provide summary of above provided Total fertility rate data in storytelling points briefly taking into account of COVID pandemic impact in brief important and significant 4 points. Answer format should start directly with 4 points without any title along with brief summary paragraph without title mentioning mentioning how this is affecting the economy of the country.'
        final_prompt = markdown + prompt
        result = bard.get_answer(final_prompt)
        st.write(result['content'])
        
        st.button(':information_source:', key=None, help='The mean number of children that would be born alive to a woman during her lifetime if she were to survive and pass through her childbearing years conforming to the fertility rates by age of a given year.')
#---------------------------------------------------------------------------------------------------------------------------------------

    #st.button(':information_source:', key=None, help='Info')