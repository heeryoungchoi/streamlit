#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import streamlit as st
import pandas as pd 
import altair as alt 
import plotly.express as px
import matplotlib.pyplot as plt 
import seaborn as sns 
import warnings
import altair as alt
import plotly.express as px
from datetime import datetime
from dateutil.relativedelta import relativedelta

warnings.filterwarnings(action='ignore')

from matplotlib import font_manager 
font_manager.fontManager.addfont('./NanumGothic.ttf')
prop = font_manager.FontProperties(fname='./NanumGothic.ttf')


#데이터 불러오기

df_new = pd.read_csv('./casino_vip_list_202411_dashboard_all.csv')
df_old = pd.read_csv('./casino_vip_list_dashboard_all_old.csv')

df_full = pd.concat([df_old,df_new]) 
df_full = df_full.drop_duplicates()

df_full.to_csv('./casino_vip_list_dashboard_all_old.csv',index=False)

df_reshaped =  df_full.loc[(df_full.model_result==1) & (df_full['trip_res'].isnull())]

df_reshaped.loc[df_reshaped.cust_kind == '0','cust_kind'] = '국제'
df_reshaped.loc[df_reshaped.cust_kind == '1','cust_kind'] = '일본'
df_reshaped.loc[df_reshaped.cust_kind == '2','cust_kind'] = '중국'

## 국적별 파이차트 함수화
def make_pie_1(df):
    df_pie = df
    df_pie = df_pie[['cust_kind','cust_id']]
    df_pie = pd.DataFrame(df_pie.groupby('cust_kind').agg(['count']))
    df_pie.columns = ['count']
    
    labels=df_pie.index
    colors=sns.color_palette('pastel')[0:3]
    wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}
    
    plt.rc('font',family='NanumGothic')
    fig1, ax = plt.subplots()
    ax.set_title('조직별 이탈 예측 비율')
    ax.pie(df_pie['count'], labels=labels , colors=colors, autopct='%.0f%%', wedgeprops = wedgeprops, startangle=180, shadow=True)  
    ax.legend(loc='upper right', fontsize=10)

    return (fig1)

 #국적별 유닛별 파이차트
def make_pie_2(df):
    
    df_pie = df
    df_pie_unit = df_pie[['cust_kind','unit_cd','cust_id']]
    df_pie_unit = df_pie_unit.groupby(['cust_kind','unit_cd']).agg(['count'])
    df_pie_unit.columns = ['count']
    
    
    #labels=['일본','중국','국제']
    colors=sns.color_palette('pastel')[0:10]
    wedgeprops={'width':0.7, 'edgecolor': 'w', 'linewidth': 5}
    
    
    d1=df_pie_unit.loc['일본']
    d2=df_pie_unit.loc['중국']
    d3=df_pie_unit.loc['국제']
    
    
    fig2, axes = plt.subplots(1, 3)
    fig2.set_size_inches((12, 5))
    plt.subplots_adjust(wspace = 0.15, hspace = 0.15)
    
    # figure 전체 제목
    fig2.suptitle('조직별 유닛별 이탈 예측 비율', fontsize = 15)
    
    
    axes[0].pie(d1['count'], labels=d1.index , colors=colors, autopct='%.0f%%', wedgeprops = wedgeprops, startangle=180, shadow=True) 
    axes[0].legend(loc='upper right', fontsize=8,  bbox_to_anchor=(1.0,1.3)) 
    axes[0].set_title('일본')
    
    axes[1].pie(d2['count'], labels=d2.index , colors=colors, autopct='%.0f%%', wedgeprops = wedgeprops, startangle=180, shadow=True) 
    axes[1].legend(loc='upper right', fontsize=8, bbox_to_anchor=(1.0,1.2))
    axes[1].set_title('중국')
    
    axes[2].pie(d3['count'], labels=d3.index , colors=colors, autopct='%.0f%%', wedgeprops = wedgeprops, startangle=180, shadow=True) 
    axes[2].legend(loc='upper right', fontsize=8)
    axes[2].set_title('국제')

    return (fig2) 

#국적별 라이프사이클별 파이차트
def make_pie_3(df):

    df_pie = df
    df_pie_life = df_pie[['cust_kind','lifecycle','cust_id']]
    df_pie_life = df_pie_life.groupby(['cust_kind','lifecycle']).agg(['count'])
    df_pie_life.columns = ['count']
    
    #labels=['일본','중국','국제']
    colors=sns.color_palette('pastel')[0:10]
    
    d1=df_pie_life.loc['일본']
    d2=df_pie_life.loc['중국']
    d3=df_pie_life.loc['국제']
    
    fig3, axes = plt.subplots(1, 3)
    fig3.set_size_inches((15, 5))
    plt.subplots_adjust(wspace = 0.15, hspace = 0.15)
    
    # figure 전체 제목
    fig3.suptitle('조직별 라이프사이클별 이탈 예측 고객 수', fontsize = 15)
    
    
    p1 = axes[0].bar( d1.index ,d1['count'], color = colors, edgecolor='gray'
                ,linewidth=1)
    axes[0].bar( d1.index ,d1['count'], color = colors,  edgecolor='gray'
                ,linewidth=1)
    axes[0].legend(loc='upper right', fontsize=5) 
    axes[0].set_title('일본')
    
    for i, j in enumerate(p1) :
        axes[0].text(i, j.get_height()+10, d1['count'][i], ha = 'center')
        

    p2 = axes[1].bar(d2.index ,d2['count'], color = colors, edgecolor='gray'
                ,linewidth=1) 
    axes[1].bar(d2.index ,d2['count'], color = colors,edgecolor='gray'
                ,linewidth=1)
    axes[1].legend(loc='upper right', fontsize=5)
    axes[1].set_title('중국')

    for i, j in enumerate(p2) :
        axes[1].text(i, j.get_height()+3, d2['count'][i], ha = 'center')

    p3 = axes[2].bar(d3.index ,d3['count'], color = colors,  edgecolor='gray'
                ,linewidth=1) 
    axes[2].bar(d3.index ,d3['count'], color = colors, edgecolor='gray'
                ,linewidth=1) 
    axes[2].legend(loc='upper right', fontsize=5)
    axes[2].set_title('국제')

    for i, j in enumerate(p3) :
        axes[2].text(i, j.get_height()+3, d3['count'][i], ha = 'center')

    return(fig3)

def df_top3(df):

    df1 = df[['cust_kind','cust_nm', 'gender','last_visit_date','lifecycle','unit_cd','ave_days','net','w/l','comp','trip']]
    df_j=df1.loc[df1.cust_kind=='일본'].sort_values('w/l',ascending=False).head(3)
    df_ch=df1.loc[df1.cust_kind=='중국'].sort_values('w/l',ascending=False).head(3)
    df_g=df1.loc[df1.cust_kind=='국제'].sort_values('w/l',ascending=False).head(3)

    
    df_all = pd.concat([df_j,df_ch,df_g])

    df_all['last_visit_date'] = df_all["last_visit_date"].astype(str)
    df_all.columns=['조직','고객이름','성별','마지막 방문일','라이프사이클','유닛','평균방문일수','매출','기대수익','콤프','트립리더여부']  

    df_all=df_all.reset_index(drop=True)
    return(df_all)


def df_summary(df):

    df1 = df[['cust_kind','cust_nm']]
    df_table = pd.DataFrame(df1.groupby('cust_kind').agg(['count']))
    df_table = df_table.reset_index(drop=False)
    df_table.columns = ['조직','이탈 예측 고객 수']

    df_table['조직1'] = pd.Categorical(df_table['조직'],categories=['일본','중국','국제'],ordered=True)
    df_table = df_table.sort_values(by=['조직','조직1','이탈 예측 고객 수'])
    df_table = df_table[['조직','이탈 예측 고객 수']]

    df_table=df_table.set_index('조직')

    return(df_table)


def get_date(current, value, opt='month'):
    year = int(current[:4])
    month = int(current[4:6])
    day = int(current[6:]) if current[6:] else 1
    if opt=='month':
        delta = datetime(year,month,day) + relativedelta(months=value)
        new_date = str(delta.year) + str(delta.month).zfill(2)
    elif opt=='day':
        delta = datetime(year,month,day) + relativedelta(days=value)
        new_date = ''.join(str(delta.date()).split("-"))
    return new_date


#stremlit 세션 초기화
if "logged_in" not in st.session_state:
    st.session_state["logged_in"]=False

#log in 
def login() :
    if id == "admin" and pw =="1234":
        st.session_state["logged_in"] = True
        st.success("로그인에 성공했습니다!")
        st.rerun()
    else:
        st.error("ID 또는 password가 올바르지 않습니다.")       

#log out
def logout():
    st.session_state["logged_in"]=False
    st.info("로그아웃 되었습니다.")
    st.rerun()


if not st.session_state["logged_in"]:
    st.title("Login")
    id=st.text_input("ID")
    pw=st.text_input("Password",type="password")
    if st.button("Login"):
        login()

else:  

    st.set_page_config(
        page_title="이탈 예측 고객 Dashboard",
        layout="wide",
        initial_sidebar_state="expanded")
     
    alt.themes.enable("dark")


    # 사이드바에 select box를 활용하여 종을 선택한 다음 그에 해당하는 행만 추출하여 데이터프레임을 만들고자합니다.
    with st.sidebar:
        st.sidebar.title('카지노 VIP 이탈 고객 예측 Dashboard')
        
        #회사구분
        company_list = list(df_reshaped.company.unique())[::-1]
        selected_company = st.selectbox('지점', company_list, index=len(company_list)-1)


        #날짜 리스트
        date_list = list(df_reshaped.yyyymm.unique())[::-1]
        
        selected_date = st.selectbox('Select a date', date_list, index=len(date_list)-1)
        
        df_date_all = df_full.loc[(df_full.yyyymm == selected_date)&(df_full.company == selected_company)]
        df_selected_date = df_reshaped.loc[(df_reshaped.yyyymm == selected_date)&(df_reshaped.company == selected_company)]
        df_selected_date_sorted = df_selected_date.sort_values(by="yyyymm")


    #col = st.columns((5, 5, 5), gap='medium')
    empty1,con1,empty22 = st.columns([0.3,1.5,0.3])
    empyt1,con2,con3,empty2 = st.columns([0.3,0.5,1.0,0.3])
    empyt1,con4,empty2 = st.columns([0.3,1.0,0.3])
    empyt1,con5,empty2 = st.columns([0.3,1.0,0.3])

    with empty22:
        if st.button("Logout"):
            logout()

    with con1:
        
        st.title(str(selected_company))
        st.markdown('### 분석 결과 요약')
        st.write('-',str(selected_date)[0:4],'년',str(selected_date)[4:6],'월 부터 2년간(',get_date(str(selected_date),-23,opt='month')[0:4],'년',get_date(str(selected_date),-23,opt='month')[4:7],'월 ~ ',str(selected_date)[0:4],'년',str(selected_date)[4:6],'월) 실적이 존재하는 VIP 고객 ',len(df_date_all),'명 중',len(df_selected_date),'명이 이탈로 예측')
        summary = df_summary(df_selected_date)
        st.dataframe(summary.style.highlight_max(axis=0))

    with con2:
        st.markdown('#### 조직별 이탈 예측 고객 비율(%)')
        pie1 = make_pie_1(df_selected_date)
        st.pyplot(pie1)


    with con3:
        st.markdown('#### 조직별 이탈 고객 리스트(조직별 Top 3)')
        df_all = df_top3(df_selected_date)
        st.dataframe(df_all)    

    with con4:
        st.markdown('#### 조직별 유닛별 이탈 고객 비율(%)')
        pie2 = make_pie_2(df_selected_date)
        st.pyplot(pie2)


    with con5:
        st.markdown('#### 조직별 라이프사이클별 이탈 고객 수(명)')
        pie3 = make_pie_3(df_selected_date)    
        st.pyplot(pie3)



