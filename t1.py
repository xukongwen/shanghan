import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import json
import os
import collections
# 血壓圖

df = pd.read_csv('t.csv', sep=' ', header=None, index_col=0, names=['date', '高压', '低压'])
st.line_chart(df)

# 臨時
df = pd.read_csv('t2.csv', sep=' ', header=None, names=['word', 'count'])
df.sort_values('count', ascending=False, inplace=True)
st.write(df)
st.write(alt.Chart(df).mark_bar().encode(x=alt.X('word', sort=None), y='count'))

# 畫排列圖
def huabar(a,b):
    st.write(alt.Chart(data).mark_bar(size=30).encode(
        x=alt.X(a, sort=None),
        y=b,
        color=alt.Color(b, scale=alt.Scale(domain=(100, -100), scheme="redyellowgreen"))
        ).properties(
            width=alt.Step(40),
            height=600)
        )



st.write(pd.DataFrame({
    '藥': [1, 2, 3, 4],
    '用量': [10, 20, 30, 40]
}))

# 方子查詢
st.title('经方查询')

shdata = json.load(open(os.path.expanduser('./data/SH_ty2.json'), 'r', encoding='utf-8'))
shdata = {(val["名"] + '-' + key): val for key, val in shdata.items()}  # dict



text = st.text_area('输入查询的方子名称')
if st.button('查询'):
    fname = text.strip()
    for key in shdata.keys():
        if fname in key:
            fdata = shdata[key]
            st.text(fdata["方"])
            st.table(pd.DataFrame(
            fdata["方"]))
            st.subheader('方劑組成')

            st.subheader('對應症狀')
            for i in fdata["证"]["体证"]:
                st.text(i)
            st.subheader('六經所在')
            st.text(fdata["经"])
            st.subheader('傷寒原文')
            st.text(fdata["原文"])
            #st.markdown("**证:** " + "; ".join(["{}: {}".format(key, ",".join(val)) for key, val in fdata["证"].items()]))
            break
    else:
        st.write("没有找到方剂 '%s'" % fname)


#=====================
st.title('伤寒论药物用量排名')
yao_list = []
for fang in shdata.values():
    yao_list.extend(fang["方"].keys())

c = collections.Counter(yao_list)
data = pd.DataFrame({"fname": c.keys(), "fcount": c.values()})
data.sort_values('fcount', ascending=False, inplace=True)

# 畫漸變顏色bar圖
st.write(alt.Chart(data).mark_bar(size=30).encode(
    x=alt.X('fname', sort=None),
    y='fcount',
    color=alt.Color("fcount", scale=alt.Scale(domain=(100, 1), scheme="redyellowgreen"))
    ).properties(
        width=alt.Step(40),
        height=600)
    )

st.write(data)


st.title('伤寒论方剂使用次数排名')
fang_list = [val['名'] for val in shdata.values()]
c = collections.Counter(fang_list)
data = pd.DataFrame({"fname": c.keys(), "fcount": c.values()})
data.sort_values('fcount', ascending=False, inplace=True)

huabar('fname','fcount')

#st.write(alt.Chart(data).mark_bar().encode(x=alt.X('fname', sort=None), y='fcount'))

st.write(data)
