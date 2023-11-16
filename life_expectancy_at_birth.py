#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st


# In[105]:
import requests
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import eurostat
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit.components.v1 import html
import pandas as pd
from ipyvizzu import Chart, Data, Config, Style
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from ipyvizzu import Chart, Data, Config, Style, DisplayTarget
from ipyvizzustory import Story, Slide, Step


from streamlit.components.v1 import html

def expander__life_expectancy_at_birth():
    
    df = pd.read_csv('geo1.csv', encoding = 'latin')
    country_select = st.selectbox(
                "Select the Country Filter:",
                options=df["Name"].unique()
                #default=df["Name"][1]
            )

    country_select = df.query(
           "Name == @country_select"
           )

    country = country_select['code'].iloc[0]

    #st.set_page_config(page_title="life_expectancy_at_birth", page_icon=":bar_chart:", layout="wide")
    st.markdown("<h1 style='text-align: center; color: #145DA0;font-size: xxx-large'>       Life Expectancy</h1>", unsafe_allow_html=True)
    def get_data_life_expectancy_at_birth(country):
        toc_df = eurostat.get_toc_df()
        f = toc_df.loc[toc_df['code']=='SDG_03_10']

        f = f.reset_index(drop=True)
        title = f['title'][0]

        dic = eurostat.get_dic('SDG_03_10', 'unit', full=False, frmt="dict", lang="en")
        dic_sex = eurostat.get_dic('SDG_03_10', 'sex', full=False, frmt="dict", lang="en")
        dic_age = eurostat.get_dic('SDG_03_10', 'age', full=False, frmt="dict", lang="en")


        

        par_values = eurostat.get_dic('SDG_03_10', 'geo',full=False, frmt="dict", lang="en")

        #my_filter_pars = {'startPeriod': 1960, 'geo': list(df['code'])}
        my_filter_pars = {'startPeriod': 1960, 'geo': country}

        data = eurostat.get_data_df('SDG_03_10', filter_pars=my_filter_pars)

        data['geo\TIME_PERIOD'] = data['geo\TIME_PERIOD'].replace(par_values)
        data['unit'] = data['unit'].replace(dic)
        data['sex'] = data['sex'].replace(dic_sex)
        data['age'] = data['age'].replace(dic_age)

        data = data.drop(['freq'], axis=1)

        df = data.melt(id_vars=["unit","sex","age", "geo\TIME_PERIOD"], 
            var_name="Year", 
            value_name="Value")

        df = df.dropna()

        dfn = df.convert_dtypes()

        return dfn


    df_life_expectancy_at_birth = get_data_life_expectancy_at_birth(country)


    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()


    lottie_url_analysis = "https://assets9.lottiefiles.com/packages/lf20_a3ntzciy.json"
    lottie_analysis = load_lottieurl(lottie_url_analysis)


    def story_life_expectancy_at_birth():
        data = Data()
        data.add_data_frame(df_life_expectancy_at_birth)

        style = Style(
            { "plot.xAxis.label.angle": "0.785rad" })

        story = Story(data=data, style=style)
        story.set_feature("tooltip", True)

        slide1 = Slide(

            Step(
                    Data.filter(
                "record.sex == 'Total'"
            ),
               Config(
                    {
                        "channels": {"x": "Year", "y": "Value"},
                        "title": "Total Life Expectancy at birth",
                        "geometry": "area",
                    }
                ),

            )

        )

        story.add_slide(slide1)



        slide2 = Slide(

            Step(
                Data.filter(
                "record.sex != 'Total'"
            ),Config.line(
                {
                    "x": "Year",
                    "y": "Value",
                    "dividedBy": "sex",
                    "title": "Life Expectancy of Males and Female",
                }
            ),

            )

        )


        slide2.add_step(Step(
            Data.filter("record.sex != 'Total'"),
            Config(
                {
                    "channels": {"y": "Value"},
                    "title": "Life Expectancy of Males and Female",
                    "geometry": "circle",
                }
            )
            )
        )

        story.add_slide(slide2)




    #     slide3 = Slide(

    #         Step(
    #             Data.filter(
    #         "record.sex == 'Males' && record.Year == '2021' "
    #     ),
    #     Config.treemap(
    #         {
    #             "size": "Value",
    #             "color": "age",
    #             "title": "Male Life Expectancy Population by Age in 2021",
    #         }
    #     ),

    #         )

    #     )

    #     story.add_slide(slide3)


    #     slide4 = Slide(

    #         Step(
    #             Data.filter(
    #         "record.sex == 'Females' && record.Year == '2021'"
    #     ),
    #     Config.treemap(
    #         {
    #             "size": "Value",
    #             "color": "age",
    #             "title": "Female Life Expectancy by Age in 2021",
    #         }
    #     ),

    #         )

    #     )

    #     story.add_slide(slide4)
        story.set_size(width=800, height=480)


        return story.play()


    with st.expander('Show Chart', expanded=True):

        left_column, right_column = st.columns([0.3, 0.7])
        with left_column:
            st_lottie(lottie_analysis, key="life_expectancy_at_birth",height=200)
            st.markdown("<h4 style='text-align: center; color: #2E8BC0; font-family: Comic Sans MS'; text-align: center;padding-top: 160px;>Life expectancy at birth is defined as the mean number of years that a new-born child can expect to live if subjected throughout his life to the current mortality conditions (age specific probabilities of dying).</h4>", unsafe_allow_html=True)
        with right_column:
            #st.button("Animate ♻️")
            story_life_expectancy_at_birth()
        #     _CHART = chart_population_sex()
        #     html(_CHART,width=2800, height=800)


expander__life_expectancy_at_birth()

#st.sidebar.button("Animate ♻️")


# In[ ]:




