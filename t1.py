import streamlit as st
import pandas as pd
import numpy as np
import json
import os

st.title('试验一下是吗')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('获取数据')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("完成! (using st.cache)")

st.subheader('Raw data')
st.write(data)

hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)

# 这个貌似是某种万能将数据显示成表格的框架
df = pd.DataFrame({'col1': [1,2,3]})
df  # <-- Draw the dataframe

x = 10
'x', x  # <-- Draw the string 'x' and then the value of x


st.title('试验json')

# 下面这样可以读取和显示json

shdata = json.load(open(os.path.expanduser('./data/SH_ty2.json'), 'r', encoding='utf-8'))

# st.json(shdata)

# st.write(shdata)

t2 = pd.DataFrame(shdata)
t2

st.write(t2)

st.text_area('输入查询的方子名称')

st.button('查询')

st.text_input('Enter some text')
# checkbox
if st.checkbox('显示内容'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    st.line_chart(chart_data)
# 选择
option = st.selectbox(
    '选择',
     df['col1'])

'你选择了: ', option

left_column, right_column = st.beta_columns(2)
pressed = left_column.button('Press me?')
if pressed:
    right_column.write("Woohoo!")

expander = st.beta_expander("显示更多")
expander.write("更长的内容")
