#import packages
import pandas as pd
import psycopg2
import plotly.express as px
import streamlit as st
import requests
from PIL import Image
from streamlit_option_menu import option_menu
from io import BytesIO


# creating connection to SQL
p_db = psycopg2.connect(host="localhost",
                        user="postgres",
                        password="password",
                        database="phonepe_database",
                        port="5432")
cursor = p_db.cursor()

# page navigation
st.set_page_config(page_title="Phonepe Pulse Data Visualization and Exploration",
                   layout="wide",
                   initial_sidebar_state="collapsed",
                   )

# sidebar option set up
with st.sidebar:
    select_page = option_menu("", ["Home", "Explore Data", "Insights"],
                              icons=["house", "graph-up-arrow", "bar-chart-line"],
                              menu_icon="menu-button-wide",
                              default_index=0,
                              styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px",
                                                   "--hover-color": "#6F36AD"},
                                      "nav-link-selected": {"background-color": "#6F36AD"}})

# setting up home page
if select_page == "Home":

    st.markdown("#")
    image_url = "https://pbs.twimg.com/card_img/1793773620797562880/euqVCkZS?format=jpg&name=large"

    # Download the image from the URL
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    width, height = image.size
    resized_image = image.resize((int(width / (height / 700)), 500))  # Adjust height to 150 pixels
    st.image(resized_image, use_column_width=False)
    st.markdown("#")

    st.title(":violet[Phonepe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and Plotly]")
    st.write(":violet[About this webpage :] This web application enables users to visualize PhonePe Pulse data in a meaningful manner, providing insights into transactions, user numbers, and usage patterns across different states and districts. Utilizing charts such as bar and pie charts, as well as a geo-visualization map, users can interact with the data to gain a deeper understanding of usage trends. Through the application, users can explore data related to transactions, user counts, and other relevant information, enhancing their understanding of PhonePe usage. The geo-visualization map offers an intuitive way to differentiate between states, with data displayed dynamically as users interact with the map.")
    st.write("---")
    st.markdown(":point_right: [Click here to Download the App!](https://www.phonepe.com/app-download/)")


# # setting up menu - explore data
if select_page == "Explore Data":
    st.sidebar.markdown("Explore Data", unsafe_allow_html=True)
    Type = st.sidebar.selectbox("Type", ("Transactions", "Users", "Insurance"))
    Year = st.sidebar.slider("Year", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)

    col1, col2 = st.columns(2)

    # transaction data exploration
    if Type == "Transactions":
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP

        st.markdown("## :violet[State Data - Transactions Amount]")
        cursor.execute(
            f"select state, sum(transaction_count) as Total_Transactions, sum(transaction_amount) as Total_amount from map_transaction where year = {Year} and quater = {Quarter} group by state order by state")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])

        # geojson- geoJSON data source for indias state boundaries
        fig = px.choropleth(df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',  # key in geoJSON file for thr state names
                            locations='State',
                            color='Total_amount',
                            color_continuous_scale='Viridis')

        # update_geos- updates props of geo layout, fitbounds- adjust the state boundaries and ensures all locations given are visible within viewport
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        st.markdown("## :violet[State Data - Transactions Count]")
        cursor.execute(
            f"select state, sum(transaction_count) as Total_Transactions, sum(transaction_amount) as Total_amount from map_transaction where year = {Year} and quater = {Quarter} group by state order by state")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
        df1.Total_Transactions = df1.Total_Transactions.astype(float)

        fig = px.choropleth(df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Total_Transactions',
                            color_continuous_scale='Inferno')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # visualizations - TOP PAYMENT TYPE

        st.markdown("## :violet[Top Payment Type]")
        cursor.execute(
            f"select transaction_type, sum(transaction_count) as Total_Transactions, sum(transaction_amount) as Total_amount from agg_transaction where year= {Year} and quater = {Quarter} group by transaction_type order by transaction_type")
        df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_type', 'Total_Transactions', 'Total_amount'])
        fig = px.pie(df,
                     title='Transaction Types Distribution',
                     names='Transaction_type',
                     values='Total_Transactions',
                     color='Total_amount',
                     color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=False)

        # visualizations TRANSACTIONS - DISTRICT WISE DATA

        st.markdown("## :violet[Select a State from below to explore more]")
        selected_state = st.selectbox("",
                                      ('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                       'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                       'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                       'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                       'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                       'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                       'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                       'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                       'Uttarakhand', 'West Bengal', 'Dadra & Nagar Haveli & Daman & Diu',
                                       'Dadra And Nagar Haveli And Daman And Diu'), index=30)

        cursor.execute(
            f"select state, districts,year,quater, sum(transaction_count) as Total_Transactions, sum(transaction_amount) as Total_amount from map_transaction where year = {Year} and quater = {Quarter} and state = '{selected_state}' group by state, districts,year,quater order by state,districts")

        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'District', 'Year', 'Quarter',
                                                       'Total_Transactions', 'Total_amount'])
        fig = px.bar(df1,
                     title=selected_state + " - District vs Total_Transactions",
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Viridis)
        st.plotly_chart(fig, use_container_width=True)

    #  user data exploration
    if Type == "Users":

        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[State Data - User App opening frequency]")
        cursor.execute(
            f"select state, sum(registered_users) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quater = {Quarter} group by state order by state")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
        df1.Total_Appopens = df1.Total_Appopens.astype(float)

        if Year == 2018 and Quarter in [1, 2, 3, 4]:
            st.warning(" :red[No Records to Display]")

        elif Year == 2019 and Quarter in [1]:
            st.warning(" :red[No Records to Display]")

        else:
            fig = px.choropleth(df1,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_Appopens',
                                color_continuous_scale='Viridis')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

        # BAR CHART TOTAL USERS - DISTRICT WISE DATA
        st.markdown("## :violet[Select any State below to explore more]")
        selected_state = st.selectbox("",
                                      ('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                       'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                       'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                       'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                       'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                       'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                       'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                       'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                       'Uttarakhand', 'West Bengal', 'Dadra & Nagar Haveli & Daman & Diu',
                                       'Dadra And Nagar Haveli And Daman And Diu'), index=30)

        cursor.execute(
            f"select state,year,quater,districts,sum(registered_users) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quater = {Quarter} and state = '{selected_state}' group by state, districts,year,quater order by state,districts")

        df = pd.DataFrame(cursor.fetchall(),
                          columns=['State', 'year', 'quarter', 'District', 'Total_Users', 'Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)

        fig = px.bar(df,
                     title=selected_state + " - District vs Total_users",
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Plotly3)
        st.plotly_chart(fig, use_container_width=True)

    if Type == "Insurance":

        # Overall State Data - INSURANCE TYPE - INDIA MAP
        st.markdown("## :violet[State Data - Insurance User - Transaction count ]")

        if Year == 2018 and Quarter in [1, 2, 3, 4]:
            st.warning(" :red[No Records to Display]")

        elif Year == 2019 and Quarter in [1, 2, 3, 4]:
            st.warning(" :red[No Records to Display] ")

        elif Year == 2020 and Quarter in [1]:
            st.warning(" :red[No Records to Display} ")

        else:

            cursor.execute(
                f"select state, sum(transaction_count) as Total_Transactions, sum(transaction_amount) as Total_amount from map_insurance where year = {Year} and quater = {Quarter} group by state order by state")
            df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])

            # df1.Total_Transactions = df1.Total_Transactions.astype(int)

            fig = px.choropleth(df1,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_Transactions',
                                color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

            # overall state transaction amount data in map insurance
            st.markdown("## :violet[State Data - Insurance user- Transaction Amount]")
            cursor.execute(
                f"select state, sum(transaction_count) as Total_Transactions, sum(transaction_amount) as Total_amount from map_insurance where year = {Year} and quater = {Quarter} group by state order by state")
            df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])

            df1.Total_amount = df1.Total_amount.astype(int)

            fig = px.choropleth(df1,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_amount',
                                color_continuous_scale='Plotly3')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

# MENU 3 -
if select_page == "Insights":

    st.markdown("## :violet[Insights from data]")
    Type = st.sidebar.selectbox("*Type*", ("Transactions", "Users", "Insurance"))
    Year = st.sidebar.slider("*Year*", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("*Quarter*", min_value=1, max_value=4)

    # Transaction insight

    if Type == "Transactions":
        st.info(
            """
            - Highest number of transactions and total amount spent on PhonePe in different states and districts.
            - Highest number of PhonePe users and their app opening frequency in different states and districts.
            - Top 10 States, Districts, and Pincodes where the most insurance transactions occurred for a selected year-quarter combination.
            - Top 10 mobile brands and their respective percentages based on PhonePe users.
            """
        )
        tab1, tab2, tab3 = st.tabs(["$\color{violet} State $", "$\color{violet} District $", "$\color{violet} Pincode $"])

        with tab1:
            cursor.execute(
                f"select state, sum(transaction_count) as Total_Transactions_Count, sum(transaction_amount) as Total from agg_transaction where year = {Year} and quater = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count', 'Total_Amount'])

            fig = px.bar(df,
                         x='State',
                         y='Total_Amount',
                         orientation='v',
                         title='Highest 10 States by Total Amount',
                         color='Transactions_Count',
                         color_continuous_scale=px.colors.sequential.Inferno,
                         labels={'Transactions_Count': 'Transactions Count'})

            fig.update_layout(title_font=dict(color="violet"), xaxis_title='State', yaxis_title='Total Amount')
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            cursor.execute(
                f"select districts , sum(transaction_count) as Total_Count, sum(transaction_amount) as Total from map_transaction where year = {Year} and quater = {Quarter} group by districts order by Total desc limit 5")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                         names='District',
                         title='5 Highest Districts by Total_amount',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(title_font=dict(color="violet"), textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            cursor.execute(
                f"select pincodes, sum(transaction_count) as Total_Transactions_Count, sum(transaction_amount) as Total from top_transaction where year = {Year} and quater = {Quarter} group by pincodes order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transactions_Count', 'Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                         names='Pincode',
                         title='10 Highest Pincodes by Total_amount',
                         color_discrete_sequence=px.colors.sequential.Inferno,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(title_font=dict(color="violet"), textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    # users insights
    if Type == "Users":
        tab1, tab2, tab3 = st.tabs(
            ["$\color{violet} State $", "$\color{violet} District $", "$\color{violet} Pincode $"])

        with tab1:
            if Year == 2022 and Quarter in [2, 3, 4]:
                st.warning(" :red[No Records to Display] ")
            elif Year == 2023 and Quarter in [1, 2, 3, 4]:
                st.warning(" :red[No Records to Display] ")
            else:
                cursor.execute(
                    f"select brands, sum(transaction_count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quater = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Users', 'Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10 brands by total_users',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                fig.update_layout(title=dict(font=dict(color="violet")))
                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            cursor.execute(
                f"select districts, sum(registered_users) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quater = {Quarter} group by districts order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users', 'Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10 districts by total_users',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Inferno)
            fig.update_layout(title=dict(font=dict(color="violet")))
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            cursor.execute(
                f"select state, sum(registered_users) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quater = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                         names='State',
                         title='Top 10 states by total_users',
                         color_discrete_sequence=px.colors.sequential.Inferno_r,
                         hover_data=['Total_Appopens'],
                         labels={'Total_Appopens': 'Total_Appopens'})
            fig.update_traces(title=dict(font=dict(color="violet")), textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    # Insurance insights
    if Type == "Insurance":
        tab1, tab2, tab3 = st.tabs(["$\color{violet} State $", "$\color{violet} District $", "$\color{violet} Pincode $"])

        with tab1:

            if Year == 2018 and Quarter in [1, 2, 3, 4]:
                st.warning(" :red[No Records to Display] ")

            elif Year == 2019 and Quarter in [1, 2, 3, 4]:
                st.warning(" :red[No Records to Display] ")

            elif Year == 2020 and Quarter in [1]:
                st.warning(" :red[No Records to Display] ")


            else:
                cursor.execute(
                    f"select state, sum(transaction_count) as Total_Transactions_Count, sum(transaction_amount) as Total from agg_insurance where year = {Year} and quater = {Quarter} group by state order by Total desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count', 'Total_Amount'])

                fig = px.bar(df,
                             x='State',
                             y='Total_Amount',
                             orientation='v',
                             title='Highest 10 States by Total Amount',
                             color='Transactions_Count',
                             color_continuous_scale=px.colors.sequential.Inferno,
                             labels={'Transactions_Count': 'Transactions Count'})

                fig.update_layout(xaxis_title='State', yaxis_title='Total Amount')
                st.plotly_chart(fig, use_container_width=True)

        with tab2:

            if Year == 2018 and Quarter in [1, 2, 3, 4]:
                st.warning(" :red[No Records to Display] ")

            elif Year == 2019 and Quarter in [1, 2, 3, 4]:
                st.warning(" :red[No Records to Display] ")

            elif Year == 2020 and Quarter in [1]:
                st.warning(" :red[No Records to Display] ")

            else:
                cursor.execute(
                    f"select districts , sum(transaction_count) as Total_Count, sum(transaction_amount) as Total from map_insurance where year = {Year} and quater = {Quarter} group by districts order by Total desc limit 5")
                df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])

                fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Highest 5 District by Total_amount',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count': 'Transactions_Count'})

                fig.update_traces(title_font=dict(color="violet"), textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)

        with tab3:

            if Year == 2018 and Quarter in [1, 2, 3, 4]:
                st.warning(" :red[No Records to Display]")

            elif Year == 2019 and Quarter in [1, 2, 3, 4]:
                st.warning(" :red[No Records to Display] ")

            elif Year == 2020 and Quarter in [1]:
                st.warning(" :red[No Records to Display] ")

            else:

                cursor.execute(
                    f"select pincodes, sum(transaction_count) as Total_Transactions_Count, sum(transaction_amount) as Total from top_insurance where year = {Year} and quater = {Quarter} group by pincodes order by Total desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transactions_Count', 'Total_Amount'])
                fig = px.pie(df, values='Total_Amount',
                             names='Pincode',
                             title='Highest 10 pincodes by Total_amount',
                             color_discrete_sequence=px.colors.sequential.Inferno,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count': 'Transactions_Count'})

                fig.update_traces(title_font=dict(color="violet"), textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
