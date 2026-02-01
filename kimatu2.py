import streamlit as st
import pandas as pd
import plotly.express as px

st.title('広告費と売上')

df = pd.read_csv('ad_expense_sales.csv')

with st.sidebar:
    st.subheader('抽出条件')
    prod_category = st.multiselect('製品カテゴリを選択してください（複数選択可）', 
                                   df['prod_category'].unique())
    media = st.selectbox('広告媒体を選択してください', 
                         df['media'].unique())
    st.subheader('色分け')    
    color = st.selectbox('分類を選択してください',
                      ['性別', '年齢層', '季節'])  
    if color == '性別':
        color = 'sex'
    elif color == '年齢層':
        color = 'age'
    else:
        color = 'season'

# st.write(f'{color}が選択されました')
#test

df = df[df['prod_category'].isin(prod_category)]
df = df[df['media']==media]

# st.dataframe(df)

fig = px.scatter(df, 
                 x='ad_expense', 
                 y='sales',
                 color=color,
                 labels={'sales':'売上 (万円)', 'ad_expense':'広告費 (万円)'},
                 range_x=[0, df['ad_expense'].max()*1.1],
                 range_y=[0, df['sales'].max()*1.1],
                 trendline='ols'
                )
st.plotly_chart(fig)