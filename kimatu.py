import streamlit as st
import pandas as pd
import plotly.express as px

st.title('日本の給与所得者数と平均所得の関係')
df = pd.read_csv('FEH_00351000_260121151701.csv')

# サイトの説明
st.write('このサイトは日本と給与所得者数と平均所得の関係を2つのグラフを用いて比較ができるサイトです。サイドバーで職種とそのデータを集計した年を選択してください。')
st.write('※選択したデータは表で確認できます。')

# csvのクリーニング
for col in df.columns:
    if '【' in col:
        df[col] = df[col].astype(str).str.replace(',', '').replace('-', '0').astype(float)

df['年_数値'] = df['年'].str.replace('年', '').astype(int)

# サイドバーの表示
with st.sidebar:
    selected_year = st.multiselect('年を選択してください（複数選択可）',
                          df['年'].unique())
    selected_job = st.selectbox('業種を選んでください',
                          df['業種（2008年～）'].unique())
    st.subheader('色分け')
    month = st.selectbox('集計月を選択してください',
                                     options=['給与所得者数(３月末)【人】','給与所得者数(６月末)【人】','給与所得者数(９月末)【人】','給与所得者数(１２月末)【人】'])
    if month == '給与所得者数(３月末)【人】':
      month = '給与所得者数(３月末)【人】'
    elif month == '給与所得者数(６月末)【人】':
      month = '給与所得者数(６月末)【人】'
    elif month == '給与所得者数(９月末)【人】':
     month = '給与所得者数(９月末)【人】'
    else:
     month = '給与所得者数(１２月末)【人】'

    # 授業で習っていないコード1
    if not df.empty:
      me1, me2 = st.columns(2)
      me1.metric("平均給与額", f'{df['給与額(平均)【千円】'].mean():.1f}千円')
      me2.metric("最大所得者", f'{df['給与所得者数(年間月平均)【人】'].max():,.0f}人')

# 講義で習っていないコード2
with st.expander("選択内容の表示"):
   selected_count = len(selected_year)

   if selected_count > 0:
      st.write(f'選択された業種：{selected_job}')
      st.write(f'選択された年数{selected_count}件数')
      st.info(f'選択された年：{','.join(map(str, sorted(selected_year)))}')
   else:
    st.warning('年が選択されていません。')

# 表の表示
df = df[df['年'].isin(selected_year)]
df = df[df['業種（2008年～）'] == selected_job]

# 授業で習ってないコード3
csv = df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
   label='選択したデータのダウンロード。',
   data=csv,
   file_name='selected_data.csv',
   mime='text/csv'
)

st.dataframe(df,width=600,height=300)

# グラフの出力
fig = px.bar(df,
                 x='年_数値',
                 y= '給与所得者数(年間月平均)【人】',
                 color='年_数値',
                 labels={'年_数値':'集計年【年】', '給与所得者数(年間月平均)【人】':'年間の平均給与所得者数【人】'}
                 )
st.plotly_chart(fig)

fig = px.scatter(df, 
                 x='給与所得者数(年間月平均)【人】', 
                 y=month,
                 color=month,
                 labels={'給与所得者数(年間月平均)【人】':'年間の平均給与所得者数【人】', '給与額(平均)【千円】':'平均給与額【千円】'},
                 range_x=[0, df['給与所得者数(年間月平均)【人】'].max()*1.1],
                 range_y=[0, df['給与所得者数(３月末)【人】'].max()*1.5],
                 trendline='ols'
                )
st.plotly_chart(fig)
