import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import json
import os

df = pd.read_csv('t.csv', sep=' ', header=None, index_col=0, names=['date', '高压', '低压'])
st.line_chart(df)

df = pd.read_csv('t2.csv', sep=' ', header=None, names=['word', 'count'])
df.sort_values('count', ascending=False, inplace=True)
st.write(df)
st.write(alt.Chart(df).mark_bar().encode(x=alt.X('word', sort=None), y='count'))


st.title('经方查询')

# 下面这样可以读取和显示json

shdata = json.load(open(os.path.expanduser('./data/SH_ty2.json'), 'r', encoding='utf-8'))
shdata = {(val["名"] + '-' + key): val for key, val in shdata.items()}  # dict
# st.write(shdata)

# st.json(shdata)

# st.write(shdata)

# t2 = pd.DataFrame(shdata)
# t2.columns = t2.iloc[0]
# t2 = t2.iloc[1:]
# st.write(t2)

text = st.text_area('输入查询的方子名称')
if st.button('查询'):
    fname = text.strip()
    for key in shdata.keys():
        if fname in key:
            fdata = shdata[key]
            st.write(fdata["证"]["体证"])
            st.write(fdata["经"])
            st.write(fdata["方"])
            st.write(fdata["原文"])
            st.markdown("**证:** " + "; ".join(["{}: {}".format(key, ",".join(val)) for key, val in fdata["证"].items()]))
            break
    else:
        st.write("没有找到方剂 '%s'" % fname)

st.title('伤寒论药物用量排名')
yao_list = []
for fang in shdata.values():
    yao_list.extend(fang["方"].keys())
import collections
c = collections.Counter(yao_list)
data = pd.DataFrame({"fname": c.keys(), "fcount": c.values()})
data.sort_values('fcount', ascending=False, inplace=True)
st.write(data)
st.write(alt.Chart(data).mark_bar().encode(x=alt.X('fname', sort=None), y='fcount'))
st.title('伤寒论方剂使用次数排名')
fang_list = [val['名'] for val in shdata.values()]
c = collections.Counter(fang_list)
data = pd.DataFrame({"fname": c.keys(), "fcount": c.values()})
data.sort_values('fcount', ascending=False, inplace=True)
st.write(data)
st.write(alt.Chart(data).mark_bar().encode(x=alt.X('fname', sort=None), y='fcount'))
