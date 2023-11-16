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
# In[32]:
def expander__population_sex():
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
    #country = df.loc[df['Name'] == country_select['Name'], 'code'].iloc[0]


    def get_data_population_sex(country):
        toc_df = eurostat.get_toc_df()
        f = toc_df.loc[toc_df['code']=='DEMO_PJANGROUP']
        f = f.reset_index(drop=True)
        title = f['title'][0]

        dic = eurostat.get_dic('DEMO_PJANGROUP', 'unit', full=False, frmt="dict", lang="en")
        dic_s_adj = eurostat.get_dic('DEMO_PJANGROUP', 'sex', full=False, frmt="dict", lang="en")
        dic_na_item = eurostat.get_dic('DEMO_PJANGROUP', 'age', full=False, frmt="dict", lang="en")


        df = pd.read_csv('geo.csv')

        par_values = eurostat.get_dic('DEMO_PJANGROUP', 'geo',full=False, frmt="dict", lang="en")

        #my_filter_pars = {'startPeriod': 2000, 'geo': list(df['code'])}
        my_filter_pars = {'startPeriod': 2000, 'geo': country}

        data = eurostat.get_data_df('DEMO_PJANGROUP', filter_pars=my_filter_pars)

        data['geo\TIME_PERIOD'] = data['geo\TIME_PERIOD'].replace(par_values)
        data['unit'] = data['unit'].replace(dic)
        data['sex'] = data['sex'].replace(dic_s_adj)
        data['age'] = data['age'].replace(dic_na_item)

        data = data.drop(['freq'], axis=1)

        df = data.melt(id_vars=["unit","sex", "age","geo\TIME_PERIOD"], 
            var_name="Year", 
            value_name="Value")

        df = df.dropna()

        dfn = df.convert_dtypes()

        return dfn


    # In[70]:


    df_population_sex = get_data_population_sex(country)
    #df_population_sex


    # In[ ]:


    #st.set_page_config(page_title="population_sex", page_icon=":bar_chart:", layout="wide")
    st.markdown("<h1 style='text-align: center; color: #145DA0;font-size: xxx-large'>       Population</h1>", unsafe_allow_html=True)


    # In[115]:


    def chart_population_sex():
        data = Data()
        #data.set_filter("df['age'] == 'From 15 to 24 years'")
        data.add_data_frame(df_population_sex)


        chart = Chart(display="manual")

        #chart = Chart(width="70%", height="100px")
        chart.animate(data)


        #chart.animate(Style({"legend": {"width": '100%'}}))

        chart.feature("tooltip", True)
        chart.animate(Style({ "plot.xAxis.label.angle": "0.785rad" }))
        chart.animate(
            Config(
                {
                    "channels": {"x": "Year", "y": "Value"},
                    "title": "Total Population",
                    "geometry": "area",
                }
            ),delay=0, duration=2,
        )

        chart.animate(
            Data.filter(
            "record.sex != 'Total'"
        ),
            Config.line(
            {
                "x": "Year",
                "y": "Value",
                "dividedBy": "sex",
                "title": "Population of Males and Female",
            }
        ),delay=0, duration=2,
    )
    #     chart.animate(Config({"split": True}))
    #     chart.animate(
    #     Config(
    #         {
    #             "channels": {
    #                 "y": {"detach": ["sex"]},
    #                 "x": {"attach": ["sex"]},
    #             },
    #         }
    #     )
    # )

        chart.animate(
            Config(
                {
                    "channels": {"y": "Value"},
                    "title": "Population of Males and Female",
                    "geometry": "circle",
                }
            ),delay=0, duration=2,
        )

        #chart.animate(Config({"channels": {"y": {"range": {"max": "150%"}}}}))


        chart.animate(Data.filter(
            "record.sex == 'Males' && record.Year == '2022' && record.age != 'Total' && record.age != 'Unknown' && record.age != '75 years or over' && record.age != 'From 80 to 84 years' && record.age != '85 years or over'"
        ),
        Config.treemap(
            {
                "size": "Value",
                "color": "age",
                "title": "Male Population by Age in 2022",
            }
        ),delay=0, duration=2,
    )

        chart.animate(Data.filter(
            "record.sex == 'Females' && record.Year == '2022' && record.age != 'Total' && record.age != 'Unknown' && record.age != '75 years or over' && record.age != 'From 80 to 84 years' && record.age != '85 years or over'"
        ),
        Config.treemap(
            {
                "size": "Value",
                "color": "age",
                "title": "Female Population by Age in 2022",
            }
        ),delay=0, duration=2,
    )



        chart.feature("tooltip", True)
        #chart.animate(Style({"legend": {"width": 50}}))
        return chart._repr_html_() 



    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()


    lottie_url_analysis = "https://assets10.lottiefiles.com/packages/lf20_5e7wgehs.json"
    lottie_analysis = load_lottieurl(lottie_url_analysis)







    def story():
        data = Data()
        data.add_data_frame(df_population_sex)

        style = Style(
            { "plot.xAxis.label.angle": "0.785rad" })

        story = Story(data=data, style=style)
        story.set_feature("tooltip", True)

        slide1 = Slide(

            Step( 
               Config(
                    {
                        "channels": {"x": "Year", "y": "Value"},
                        "title": "Total Population",
                        "geometry": "rectangle",
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
                    "title": "Population of Males and Female",
                }
            ),

            )

        )


        slide2.add_step(Step(
            Data.filter("record.sex != 'Total'"),
            Config(
                {
                    "channels": {"y": "Value"},
                    "title": "Population of Males and Female",
                    "geometry": "circle",
                }
            )
            )
        )

        story.add_slide(slide2)

    #     slide3 = Slide(

    #         Step(
    #             Config(
    #             {
    #                 "channels": {"y": "Value"},
    #                 "title": "Population of Males and Female",
    #                 "geometry": "circle",
    #             }
    #         ),

    #         )

    #     )

    #     story.add_slide(slide3) 


        slide3 = Slide(

            Step(
                Data.filter(
            "record.sex == 'Males' && record.Year == '2022' && record.age != 'Total' && record.age != 'Unknown' && record.age != '75 years or over' && record.age != 'From 80 to 84 years' && record.age != '85 years or over'"
        ),
        Config.treemap(
            {
                "size": "Value",
                "color": "age",
                "title": "Male Population by Age in 2022",
            }
        ),

            )

        )

        story.add_slide(slide3)


        slide4 = Slide(

            Step(
                Data.filter(
            "record.sex == 'Females' && record.Year == '2022' && record.age != 'Total' && record.age != 'Unknown' && record.age != '75 years or over' && record.age != 'From 80 to 84 years' && record.age != '85 years or over'"
        ),
        Config.treemap(
            {
                "size": "Value",
                "color": "age",
                "title": "Female Population by Age in 2022",
            }
        ),

            )

        )

        story.add_slide(slide4)
        story.set_size(width=800, height=480)


        return story.play()


    with st.expander('Show Chart', expanded=True):
        left_column, right_column = st.columns([0.3, 0.7])
        with left_column:
            st_lottie(lottie_analysis, key="population_sex",height=200)
            st.markdown("<h4 style='text-align: center; color: #2E8BC0; font-family: Comic Sans MS'; text-align: center;padding-top: 160px;>This refers to the number of persons having their usual residence in a country on 1 January of the respective year. When usually resident population is not available, countries may report legal or registered residents.</h4>", unsafe_allow_html=True)
        with right_column:
            #st.button("Animate ♻️")
            story()
        #     _CHART = chart_population_sex()
        #     html(_CHART,width=2800, height=800)

#st.write(country)
expander__population_sex()

#st.sidebar.button("Animate ♻️")

