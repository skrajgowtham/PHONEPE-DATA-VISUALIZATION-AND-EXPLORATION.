import json
import psycopg2
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

#DataFrame Creation & SQL Connection
mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      password="Suguna@12",
                      database="phonepe_data",
                      port="5432")
cursor=mydb.cursor()

#Aggre_Insurance
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1=cursor.fetchall()
Agg_insurance=pd.DataFrame(table1,columns=("States", "Years", "Quarter", 
                                           "Transaction_type" ,"Transaction_count", 
                                           "Transaction_amount"))

#Aggre_Transaction
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2=cursor.fetchall()
Agg_Transaction=pd.DataFrame(table2,columns=("States", "Years", "Quarter", 
                                           "Transaction_type" ,"Transaction_count", 
                                           "Transaction_amount"))

#Aggre_User
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3=cursor.fetchall()
Agg_User=pd.DataFrame(table3,columns=("States", "Years", "Quarter", 
                                           "Brands" ,"Transaction_count",
                                           "Percentage"))

#Map_Insurance
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4=cursor.fetchall()
Map_Insurance=pd.DataFrame(table4,columns=("States", "Years", "Quarter", 
                                           "Districts" ,"Transaction_count",
                                           "Transaction_amount"))

#Map_Transaction
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5=cursor.fetchall()
Map_Transaction=pd.DataFrame(table5,columns=("States", "Years", "Quarter", 
                                           "Districts" ,"Transaction_count",
                                           "Transaction_amount"))

#Map_User
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()
Map_User=pd.DataFrame(table6,columns=("States", "Years", "Quarter", 
                                           "Districts" ,"Registered_Users",
                                           "AppOpens"))

#Top_Insurance
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()
Top_Insurance=pd.DataFrame(table7,columns=("States", "Years", "Quarter", 
                                           "Pincodes" ,"Transaction_count",
                                           "Transaction_amount"))

#Top_Transaction
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8=cursor.fetchall()
Top_Transaction=pd.DataFrame(table8,columns=("States", "Years", "Quarter", 
                                           "Pincodes" ,"Transaction_count",
                                           "Transaction_amount"))

#Top_User
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()
Top_User=pd.DataFrame(table9,columns=("States", "Years", "Quarter", 
                                           "Pincodes" ,"Registered_Users",))

def Transaction_amount_count_Y(df,year):
    tcay=df[df["Years"]==year]
    tcay.reset_index(drop=True,inplace=True)
    tcaygroup=tcay.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tcaygroup.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(tcaygroup, x="States",y="Transaction_amount",title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Cividis,height=650,width=600)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count=px.bar(tcaygroup, x="States",y="Transaction_count",title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Rainbow,height=650,width=600)
        st.plotly_chart(fig_count)

    colum1,colum2=st.columns(2)
    with colum1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()    

        fig_india_one=px.choropleth(tcaygroup,geojson=data1,locations= "States", featureidkey="properties.ST_NM",
                                    color="Transaction_amount",color_continuous_scale="Rainbow",
                                    range_color=(tcaygroup["Transaction_amount"].min(),tcaygroup["Transaction_amount"].max())
                                    ,hover_name="States", title=f"{year} TRANSACTION AMOUNT", fitbounds="locations",
                                    height=600,width=600)
        fig_india_one.update_geos(visible=False)
        st.plotly_chart(fig_india_one)
    with colum2:
        fig_india_two=px.choropleth(tcaygroup,geojson=data1,locations= "States", featureidkey="properties.ST_NM",
                                    color="Transaction_count",color_continuous_scale="Rainbow",
                                    range_color=(tcaygroup["Transaction_count"].min(),tcaygroup["Transaction_count"].max())
                                    ,hover_name="States", title=f"{year} TRANSACTION COUNT", fitbounds="locations",
                                    height=600,width=600)
        fig_india_two.update_geos(visible=False)
        st.plotly_chart(fig_india_two)
    return tcay

def Transaction_amount_count_Y_Q(df,quarter):
    tcay=df[df["Quarter"]==quarter]
    tcay.reset_index(drop=True,inplace=True)

    tcaygroup=tcay.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tcaygroup.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(tcaygroup, x="States",y="Transaction_amount",title=f"{tcay['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Cividis,height=650,width=600)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count=px.bar(tcaygroup, x="States",y="Transaction_count",title=f"{tcay['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Rainbow,height=650,width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()    

        fig_india_one=px.choropleth(tcaygroup,geojson=data1,locations= "States", featureidkey="properties.ST_NM",
                                    color="Transaction_amount",color_continuous_scale="Rainbow",
                                    range_color=(tcaygroup["Transaction_amount"].min(),tcaygroup["Transaction_amount"].max())
                                    ,hover_name="States", title=f"{tcay['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds="locations",
                                    height=600,width=600)
        fig_india_one.update_geos(visible=False)
        st.plotly_chart(fig_india_one)

    with col2:
        fig_india_two=px.choropleth(tcaygroup,geojson=data1,locations= "States", featureidkey="properties.ST_NM",
                                    color="Transaction_count",color_continuous_scale="Rainbow",
                                    range_color=(tcaygroup["Transaction_count"].min(),tcaygroup["Transaction_count"].max())
                                    ,hover_name="States", title=f"{tcay['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds="locations",
                                    height=600,width=600)
        fig_india_two.update_geos(visible=False)
        st.plotly_chart(fig_india_two)
    return tcay

def Aggreg_trans_Transaction_type(df,state):
    tcay=df[df["States"]==state]
    tcay.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)
    with col1:
        tcaygroup=tcay.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
        tcaygroup.reset_index(inplace=True)

        fig_pie_one=px.pie(data_frame=tcaygroup,names="Transaction_type",values="Transaction_amount",
                        width=600,title=f"{state.upper()} TRANSACTION AMOUNT",hole=0.4)
        st.plotly_chart(fig_pie_one)

    with col2:
        fig_pie_two=px.pie(data_frame=tcaygroup,names="Transaction_type",values="Transaction_count",
                        width=600,title=f"{state.upper()} TRANSACTION COUNT",hole=0.4)
        st.plotly_chart(fig_pie_two)

def Aggre_user_plot1(df,year):
    aguy=df[df["Years"]==year]
    aguy.reset_index(drop=True,inplace=True)
    aguygroup=pd.DataFrame(aguy.groupby("Brands")[["Transaction_count","Percentage"]].sum())
    aguygroup.reset_index(inplace=True)

    fig_bar_one=px.bar(aguygroup, x="Brands",y="Transaction_count",title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=800,color_discrete_sequence=px.colors.sequential.haline,hover_name="Brands")
    st.plotly_chart(fig_bar_one)
    return aguy

#Aggregated_user_plot_2
def Aggreg_user_plot2(df,quarter):
    aguyq=df[df["Quarter"]==quarter]
    aguyq.reset_index(drop=True,inplace=True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_one=px.bar(aguyqg, x="Brands",y="Transaction_count",title=f"{quarter} QUARTER BRANDS AND TRANSACTION COUNT",
                        width=800,color_discrete_sequence=px.colors.sequential.Magenta,hover_name="Brands")
    st.plotly_chart(fig_bar_one)
    return aguyq

#Aggregated_user_3
def Aggre_user_plot_3(df,state):
    auyqs=df[df["States"]==state]
    auyqs.reset_index(drop=True,inplace=True)

    fig_line_1=px.line(auyqs,x="Brands",y="Transaction_count",hover_data="Percentage",
                    title=f"{state.upper()} BRANDS,TRANSACTION COUNT,PERCENTAGE",width=1000,markers=True)
    st.plotly_chart(fig_line_1)


#Map_Insurance_District
def Map_insur_District(df,state):
    tcay=df[df["States"]==state]
    tcay.reset_index(drop=True,inplace=True)

    tcaygroup=tcay.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tcaygroup.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar_one=px.bar(tcaygroup,x="Transaction_amount",y="Districts",orientation="h",height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_one)

    with col2:
        fig_bar_two=px.bar(tcaygroup,x="Transaction_count",y="Districts",orientation="h",height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Magenta_r)
        st.plotly_chart(fig_bar_two)

#Map_user_plot_1
def map_user_plot_1(df,year):
    muy=df[df["Years"]==year]
    muy.reset_index(drop=True,inplace=True)

    muygroup=muy.groupby("States")[["Registered_Users","AppOpens"]].sum()
    muygroup.reset_index(inplace=True)

    fig_line_1=px.line(muygroup,x="States",y=["Registered_Users","AppOpens"],
                        title=f"{year} REGISTERED USER AND APPOPENS",width=1000,height=800,markers=True)
    st.plotly_chart(fig_line_1)
    return muy

#Map_user_plot_2
def map_user_plot_2(df,quarter):
    muyq=df[df["Quarter"]==quarter]
    muyq.reset_index(drop=True,inplace=True)

    muyqgroup=muyq.groupby("States")[["Registered_Users","AppOpens"]].sum()
    muyqgroup.reset_index(inplace=True)

    fig_line_1=px.line(muyqgroup,x="States",y=["Registered_Users","AppOpens"],
                        title=f"{df['Years'].min()} YEARS {quarter} QUARTER REGISTERED USER AND APPOPENS",width=1000,height=800,markers=True,
                        color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_line_1)
    return muyq       

#MAP User plot 3
def map_user_plot_3(df, state):
    muyqs= df[df["States"] == state]
    muyqs.reset_index(drop= True, inplace= True)
    muyqsg= muyqs.groupby("Districts")[["Registered_Users", "AppOpens"]].sum()
    muyqsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_plot_1= px.bar(muyqsg, x= "Registered_Users",y= "Districts",orientation="h",
                                    title= f"{state.upper()} REGISTERED USER",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_plot_1)

    with col2:
        fig_map_user_plot_2= px.bar(muyqsg, x= "AppOpens", y= "Districts",orientation="h",
                                    title= f"{state.upper()} APPOPENS",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_plot_2)

#Top_insur_plot_1
def Top_insurance_plot_1(df,state):
    tiy=df[df["States"]==state]
    tiy.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_top_insur_plot_1= px.bar(tiy, x="Quarter",y= "Transaction_amount",hover_data="Pincodes",
                                    title="TRANSACTION AMOUNT",height=650,width=600,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_top_insur_plot_1)
    with col2:
        fig_top_insur_plot_2= px.bar(tiy, x="Quarter",y= "Transaction_count",hover_data="Pincodes",
                                    title="TRANSACTION COUNT",height=650,width=600,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_top_insur_plot_2)

#Top User plot 1
def top_user_plot1(df,year):
    tuy=df[df["Years"]==year]
    tuy.reset_index(drop=True,inplace=True)

    tuygroup=pd.DataFrame(tuy.groupby(["States","Quarter"])["Registered_Users"].sum())
    tuygroup.reset_index(inplace=True)

    fig_top_plot_one=px.bar(tuygroup, x="States",y="Registered_Users",height=800,
                            title=f"{year} REGISTERED USERS",width=1000,
                            color_discrete_sequence=px.colors.sequential.haline,hover_name="States")
    st.plotly_chart(fig_top_plot_one)
    return tuy

#Top User plot 2
def top_user_plot_2(df,state):
    tuys=df[df["States"]==state]
    tuys.reset_index(drop=True,inplace=True)

    fig_top_plot_2=px.bar(tuys,x="Quarter",y="Registered_Users",title="REGISTERED USERS,PINCODES,QUARTERS",
                                width=1000,height=800,color="Registered_Users",hover_data="Pincodes",
                                color_continuous_scale=px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)


def ques1():
    brand= Agg_User[["Brands","Transaction_count"]]
    brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_count", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= Agg_Transaction[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    htd= Map_Transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)

def ques4():
    htd= Map_Transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)


def ques5():
    sa= Map_User[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques6():
    sa= Map_User[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= Agg_Transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= Agg_Transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    ht= Agg_Transaction[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques10():
    dt= Map_Transaction[["Districts", "Transaction_amount"]]
    dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "Districts", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)


#Streamlit Part
st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    select=option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select=="HOME":
    st.subheader("PhonePe-INDIA'S BEST TRANSACTION APP")
    st.subheader("PhonePe is an Indian digital payments and financial technology company")
    col1,col2= st.columns(2)

    with col1:
        st.write("****FEATURES****")
        st.write("****-> Credit & Debit card linking****")
        st.write("****-> Bank Balance check****")
        st.write("****-> Money Storage****")
        st.write("****-> PIN Authorization****")
        st.write("****-> Easy Transactions****")
        st.write("****-> One App For All Your Payments****")
        st.write("****-> Your Bank Account Is All You Need****")
        st.write("****-> Multiple Payment Modes****")
        st.write("****->PhonePe Merchants****")
        st.write("****-> Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****-> Earn Great Rewards****")
        st.download_button("DOWNLOAD THE PHONEPE APP", "https://www.phonepe.com/app-download/")

if select=="DATA EXPLORATION":

    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

#AGGREGATED
    with tab1:
        function=st.radio("Select The Analysis",["Insurance Analysis","Transaction Analysis","User Analysis"])
        if function=="Insurance Analysis":

            column1,column2=st.columns(2)
            with column1:
                years=st.slider("Choose the Year",Agg_insurance["Years"].min(),Agg_insurance["Years"].max(),Agg_insurance["Years"].min())
            tac_y=Transaction_amount_count_Y(Agg_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Choose the Quarter",tac_y["Quarter"].min(),tac_y["Quarter"].max(),tac_y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_y,quarters)


        elif function=="Transaction Analysis":
            column1,column2=st.columns(2)
            with column1:
                years=st.slider("Choose the Year",Agg_Transaction["Years"].min(),Agg_Transaction["Years"].max(),Agg_Transaction["Years"].min())
            Agg_tran_tac_y=Transaction_amount_count_Y(Agg_Transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Selecct the State",Agg_tran_tac_y["States"].unique())
            Aggreg_trans_Transaction_type(Agg_tran_tac_y,states)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Choose the Quarter",Agg_tran_tac_y["Quarter"].min(),Agg_tran_tac_y["Quarter"].max(),Agg_tran_tac_y["Quarter"].min())
            Agg_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Agg_tran_tac_y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Selecct the State_type",Agg_tran_tac_Y_Q["States"].unique())
            
            Aggreg_trans_Transaction_type(Agg_tran_tac_Y_Q,states)


        elif function=="User Analysis":
            column1,column2=st.columns(2)
            with column1:
                years=st.slider("Choose the Year",Agg_User["Years"].min(),Agg_User["Years"].max(),Agg_User["Years"].min())
            Aggre_user_Y=Aggre_user_plot1(Agg_User,years)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Choose the Quarter",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q=Aggreg_user_plot2(Aggre_user_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Selecct the State",Aggre_user_Y_Q["States"].unique())
            
            Aggre_user_plot_3(Aggre_user_Y_Q,states)
        
#MAP
    with tab2:
        function2=st.radio("Select The Analysis",["Map Insurance Analysis","Map Transaction Analysis","Map User Analysis"])
        if function2=="Map Insurance Analysis":
            column1,column2=st.columns(2)
            with column1:
                years=st.slider("Choose the Year_mi",Map_Insurance["Years"].min(),Map_Insurance["Years"].max(),Map_Insurance["Years"].min())
            map_insur_tac_y=Transaction_amount_count_Y(Map_Insurance,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Selecct the State_mapinsur",map_insur_tac_y["States"].unique())
            Map_insur_District(map_insur_tac_y,states)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Choose the Quarter_mi",map_insur_tac_y["Quarter"].min(),map_insur_tac_y["Quarter"].max(),map_insur_tac_y["Quarter"].min())
            map_insur_tac_y_Q=Transaction_amount_count_Y_Q(map_insur_tac_y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Selecct the State_type",map_insur_tac_y_Q["States"].unique())
            Map_insur_District(map_insur_tac_y_Q,states)


        elif function2=="Map Transaction Analysis":
            column1,column2=st.columns(2)
            with column1:
                years=st.slider("Choose the Year",Map_Transaction["Years"].min(),Map_Transaction["Years"].max(),Map_Transaction["Years"].min())
            map_tran_tac_y=Transaction_amount_count_Y(Map_Transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Selecct the State_mapinsur",map_tran_tac_y["States"].unique())
            Map_insur_District(map_tran_tac_y,states)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Choose the Quarter",map_tran_tac_y["Quarter"].min(),map_tran_tac_y["Quarter"].max(),map_tran_tac_y["Quarter"].min())
            map_tran_tac_y_Q=Transaction_amount_count_Y_Q(map_tran_tac_y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Selecct the State_type",map_tran_tac_y_Q["States"].unique())
            Map_insur_District(map_tran_tac_y_Q,states)
           
        elif function2=="Map User Analysis":
            column1,column2=st.columns(2)
            with column1:
                years_mu=st.slider("Choose the Year_mu",Map_User["Years"].min(),Map_User["Years"].max(),Map_User["Years"].min())
            map_user_y=map_user_plot_1(Map_User,years_mu)

            col1,col2=st.columns(2)
            with col1:
                quarters_mu=st.slider("Choose the Quarter_mu",map_user_y["Quarter"].min(),map_user_y["Quarter"].max(),map_user_y["Quarter"].min())
            map_user_Y_Q=map_user_plot_2(map_user_y,quarters_mu)

            col1,col2=st.columns(2)
            with col1:
                states_mu=st.selectbox("Selecct the State_mu",map_user_Y_Q["States"].unique())
            map_user_plot_3(map_user_Y_Q,states_mu)

#TOP
    with tab3:
        function3=st.radio("Select The Analysis",["Top Insurance Analysis","Top Transaction Analysis","Top User Analysis"])
        if function3=="Top Insurance Analysis":
            column1,column2=st.columns(2)
            with column1:
                years=st.slider("Choose the Year_ti",Top_Insurance["Years"].min(),Top_Insurance["Years"].max(),Top_Insurance["Years"].min())
            top_insur_tac_y=Transaction_amount_count_Y(Top_Insurance,years)

            col1,col2=st.columns(2)
            with col1:
                states_mu=st.selectbox("Selecct the State_ti",top_insur_tac_y["States"].unique())
            Top_insurance_plot_1(top_insur_tac_y,states_mu)

            col1,col2=st.columns(2)
            with col1:
                quarters_mu=st.slider("Choose the Quarter_mu",top_insur_tac_y["Quarter"].min(),top_insur_tac_y["Quarter"].max(),top_insur_tac_y["Quarter"].min())
            top_insur_tac_y_Q=Transaction_amount_count_Y_Q(top_insur_tac_y,quarters_mu)

        elif function3=="Top Transaction Analysis":
            column1,column2=st.columns(2)
            with column1:
                years=st.slider("Choose the Year_tt",Top_Transaction["Years"].min(),Top_Transaction["Years"].max(),Top_Transaction["Years"].min())
            top_tran_tac_y=Transaction_amount_count_Y(Top_Transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states_ti=st.selectbox("Selecct the State_tt",top_tran_tac_y["States"].unique())
            Top_insurance_plot_1(top_tran_tac_y,states_ti)

            col1,col2=st.columns(2)
            with col1:
                quarters_mu=st.slider("Choose the Quarter_tt",top_tran_tac_y["Quarter"].min(),top_tran_tac_y["Quarter"].max(),top_tran_tac_y["Quarter"].min())
            top_tran_tac_y_Q=Transaction_amount_count_Y_Q(top_tran_tac_y,quarters_mu)
        
        elif function3=="Top User Analysis":
            column1,column2=st.columns(2)
            with column1:
                years=st.slider("Choose the Year_tu",Top_User["Years"].min(),Top_User["Years"].max(),Top_User["Years"].min())
            top_user_Y=top_user_plot1(Top_User,years)

            col1,col2=st.columns(2)
            with col1:
                states_ti=st.selectbox("Selecct the State_tu",top_user_Y["States"].unique())
            top_user_plot_2(top_user_Y,states_ti)
    
if select == "TOP CHARTS":

    ques= st.selectbox("**Select the Question**",('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                  'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))
    
    if ques=="Top Brands Of Mobiles Used":
        ques1()

    elif ques=="States With Lowest Trasaction Amount":
        ques2()

    elif ques=="Districts With Highest Transaction Amount":
        ques3()

    elif ques=="Top 10 Districts With Lowest Transaction Amount":
        ques4()

    elif ques=="Top 10 States With AppOpens":
        ques5()

    elif ques=="Least 10 States With AppOpens":
        ques6()

    elif ques=="States With Lowest Trasaction Count":
        ques7()

    elif ques=="States With Highest Trasaction Count":
        ques8()

    elif ques=="States With Highest Trasaction Amount":
        ques9()

    elif ques=="Top 50 Districts With Lowest Transaction Amount":
        ques10()