import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('広告費の売り上げ')
df = pd.read_csv('ad_expense_sales.csv')

with st.sidebar:
    selected_cats = st.multiselect('製品を選択してください（複数選択可）',
                          df['prod_category'].unique())
    selected_media = st.selectbox('広告媒体を選んでください',
                          df['media'].unique())
    selected_label = st.selectbox('色分け',
                                  options=['性別','年齢層','季節'])
    if selected_label == '性別':
        color = 'sex'
    elif selected_label == '年齢層':
        color = 'age'
    elif selected_label == '季節':
        color = 'season'
  
df = df[df['prod_category'].isin(selected_cats)]
df = df[df['media'] == selected_media]

st.dataframe(df,width=600,height=200)

# 図の出力
plt.scatter(df['ad'],
            df['sales'],
            s=50,
            color='b',
            marker='o',
            alpha=0.3
            )
plt.title('ad_expanse', fontsie=16)
plt.xlabel('広告費', fontsize=16)
plt.ylabel('売上', fontsize=16)
plt.grid(True)
plt.tick_params(labelsize=12)
st.pyplot(plt.gcf())


