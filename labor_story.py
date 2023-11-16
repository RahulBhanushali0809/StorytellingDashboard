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
#     "__Secure-1PSID": "cwim21ibXu6RWnA0AXtKEf8oGXqONgFdVNWpAAq_l6_CKhWRco687toNBb14l-NSnadvOw.",
#     "__Secure-1PSIDTS": "sidts-CjIBNiGH7gNIGK-mA6pTRpVVrV1HgCwZz8-e8_FqrnRHjetzfdHiaJFJJAen-2C2kgXrdBAA",
#     # Any cookie values you want to pass session object.
# }
cookie_dict = cookie_dict
bard = BardCookies(cookie_dict=cookie_dict)

def expander_labor(country):
    
    st.markdown(f"<h2 style='text-align: center; color: #FACFCE;font-size: xxx-medium'>Unemployment Rate by Sex for age group 15 to 74 years......</h2>", unsafe_allow_html=True)
    #st.markdown(f"<h1 style='text-align: center; color: #145DA0; font-size: xxx-medium'>Unemployment Rate by Sex for age group 15 to 74 years in <span style='color:{country_text_color}'>{country}</span>.</h1>", unsafe_allow_html=True)
    with st.expander('Show Chart', expanded=False):

        db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="research_lab_2022",
        database="data_story"
        )

        cursor = db_connection.cursor()

        my_variable = country

        query = "SELECT * FROM unemp_sex WHERE (geo = %s || geo = 'European Union - 27 countries (from 2020)') && age = 'From 15 to 74 years' && sex != 'Total'" # Change 'your_column' and the condition as needed


        cursor.execute(query, (my_variable,))

        # Create a Pandas DataFrame from the cursor object
        data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        cursor.close()
        db_connection.close()

        filtered_df = pd.DataFrame(data)
        
        sex = st.selectbox("sex", filtered_df['sex'].unique())
        
        filtered_df = filtered_df[(filtered_df['sex'] == sex)]

        filtered_df.dropna()
        color_map = {'European Union - 27 countries (from 2020)': '#F2E3D5'}
        
        fig = px.line(filtered_df, x='Year', y='Value', title='', color = 'geo', color_discrete_map=color_map)
        fig.update_xaxes(
            dtick="M1",
            tickformat="%Y-%b",
            showline=False,
            showgrid=False,
            showticklabels=True,
            tickangle=0,
            tickfont=dict(size=10),


        )
        fig.update_traces(line=dict(dash='dash'), selector=dict(name ='European Union - 27 countries (from 2020)'))
        
        fig.update_layout(yaxis_title="Percentage of population in the labour force",xaxis_title="")

        fig.update_layout(width=1200)
        
        
        fig.add_vrect(x0="2019", x1="2020", 
              annotation_text="Start of<br>COVID-19<br>Period", annotation_position="top right",  
              annotation_font_size=11,
              annotation_font_color="#F2E3D5",
              fillcolor="orange", opacity=0.25, line_width=0)
        
        
#         max_year_index = filtered_df['Year'].idxmax()
#         col1, col2, col3 = st.columns(3)
        
#         col1.metric("Highest", filtered_df['Value'].max())
#         col2.metric("Lowest" ,filtered_df['Value'].min())
#         col3.metric("Current", filtered_df.at[max_year_index, 'Value'])
        
        #st.plotly_chart(fig)
        
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig)
        st.markdown('</div>', unsafe_allow_html=True)
        
        
        
        markdown = filtered_df.to_string()
        #markdown = filtered_df.to_markdown()
        prompt = '     Provide summary of above provided unemployment for males and females data in storytelling points briefly in brief important and significant 4 points. Answer format should start directly with 4 points without any title along with brief summary paragraph without title mentioning how this is affecting the economy of the country.'
        final_prompt = markdown + prompt
        result = bard.get_answer(final_prompt)
        st.write(result['content'])
        
        st.button(':information_source:', key=None, help='Unemployment rate represents unemployed persons as a percentage of the labour force. The labour force is the total number of people employed and unemployed. Unemployed persons comprise persons aged 15 to 74 who were: a. without work during the reference week, b. currently available for work, i.e. were available for paid employment or self-employment before the end of the two weeks following the reference week, c. actively seeking work, i.e. had taken specific steps in the four weeks period ending with the reference week to seek paid employment or self-employment or who found a job to start later, i.e. within a period of, at most, three months. The indicator is based on the EU Labour Force Survey.')
#------------------------------------------------------------------------------------------------------------------------------------------

    st.markdown("<h2 style='text-align: center; color: #FACFCE;font-size: xxx-medium'>Employment Rate by Sex for age group 20 to 64 years....</h2>", unsafe_allow_html=True)    
    with st.expander('Show Chart', expanded=False):

        db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="research_lab_2022",
        database="data_story"
        )

        cursor = db_connection.cursor()

        my_variable = country

        query = "SELECT * FROM emp_sex WHERE (geo = %s || geo = 'European Union - 27 countries (from 2020)') && age = 'From 20 to 64 years' && sex != 'Total'" # Change 'your_column' and the condition as needed


        cursor.execute(query, (my_variable,))

        # Create a Pandas DataFrame from the cursor object
        data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        cursor.close()
        db_connection.close()


        filtered_df = pd.DataFrame(data)
          
        sex = st.selectbox("Sex", filtered_df['sex'].unique())
        
        filtered_df = filtered_df[(filtered_df['sex'] == sex)]
       
        filtered_df.dropna()
        color_map = {'European Union - 27 countries (from 2020)': '#F2E3D5'}
        
        fig = px.line(filtered_df, x='Year', y='Value', title='sex', color = 'geo', color_discrete_map=color_map)
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
        fig.update_layout(width=1200)
        fig.update_layout(yaxis_title="Percentage of population in the labour force",xaxis_title="")
        
        fig.add_vrect(x0="2019", x1="2020", 
              annotation_text="Start of<br>COVID-19<br>Period", annotation_position="top right",  
              annotation_font_size=11,
              annotation_font_color="#F2E3D5",
              fillcolor="orange", opacity=0.25, line_width=0)

        st.plotly_chart(fig)
        
        markdown = filtered_df.to_string()
        #markdown = filtered_df.to_markdown()
        prompt = '     Provide summary of above provided employment for males and females data in storytelling points briefly in brief important and significant 4 points. Answer format should start directly with 4 points without any title along with brief summary paragraph without title mentioning how this is affecting the economy of the country.'
        final_prompt = markdown + prompt
        result = bard.get_answer(final_prompt)
        st.write(result['content'])
                  
        st.button(':information_source:', key=None, help='The employment rate of the total population is calculated by dividing the number of person aged 20 to 64 in employment by the total population of the same age group. The employment rate of men is calculated by dividing the number of men aged 20 to 64 in employment by the total male population of the same age group. The employment rate of women is calculated by dividing the number of women aged 20 to 64 in employment by the total female population of the same age group. The indicators are based on the EU Labour Force Survey.')
#----------------------------------------------------------------------------------------------------------------------------------------
        
    st.markdown("<h2 style='text-align: center; color: #FACFCE;font-size: xxx-medium'>Full-time and Part-time youth Employment by Profession in 2022.....</h2>", unsafe_allow_html=True)
    with st.expander('Show Chart', expanded=False):

        db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="research_lab_2022",
        database="data_story"
        )

        cursor = db_connection.cursor()

        my_variable = country

        query = "SELECT * FROM ft_pt_emp WHERE geo = %s && age = 'From 15 to 24 years' && isco08 != 'Total' && isco08 != 'No response' && worktime != 'Total' && Year=2022 && sex != 'Total'"  # Change 'your_column' and the condition as needed


        cursor.execute(query, (my_variable,))

        # Create a Pandas DataFrame from the cursor object
        data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        cursor.close()
        db_connection.close()

        df = pd.DataFrame(data)

        worktime_filter = st.selectbox("worktime", df['worktime'].unique())
        
        filtered_df = df[(df['worktime'] == worktime_filter)]

       
        filtered_df.dropna()
        filtered_df = filtered_df.sort_values(by="Value", ascending=False)


        # Group by 'Year', 'Quarter', and 'sex' and sum the 'Values' column
        filtered_df = filtered_df.groupby(['Year', 'Quarter', 'isco08', 'sex'])['Value'].sum().reset_index()

        # Group by 'Year' and 'sex' and sum the 'Values' column
        filtered_df = filtered_df.groupby(['Year', 'isco08','sex'])['Value'].sum().reset_index()

        #fig = px.bar(filtered_df, x="Value", y="isco08", color="sex", pattern_shape="sex", pattern_shape_sequence=["+", "-"])
        fig = px.bar(filtered_df, x="Value", y="isco08", color="sex", text_auto = True)
        fig.update_traces(textfont_size = 14, textangle = 0, textposition = "inside")
        fig.update_layout(yaxis_title="Occupation",xaxis_title="Full-time and part-time employment by sex, age and occupation (1 000)")

        fig.update_layout(width=1200)
        st.plotly_chart(fig)
        
        markdown = filtered_df.to_string()
        #markdown = filtered_df.to_markdown()
        prompt = '     Provide summary of above provided Full-time or Part-time youth Employment by Profession in 2022 data in storytelling points briefly in brief important and significant 4 points. Answer format should start directly with 4 points without any title along with brief summary paragraph without title mentioning how this is affecting the economy of the country.'
        final_prompt = markdown + prompt
        result = bard.get_answer(final_prompt)
        st.write(result['content'])
        
        st.button(':information_source:', key=None, help='Full-time and part-time employment by sex, age and occupation (1 000)')
#-----------------------------------------------------------------------------------------------------------------------------------------