# -*- coding: UTF-8 -*-

import os
import copy
import time
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np


def get_file_list(suffix,path):
    '''
    获取当前目录所有指定后缀名的文件名列表、绝对路径列表
    :param suffix:后缀名
    :param path:目录路径
    :return:返回文件名列表、绝对路径列表
    '''
    input_template_all=[]
    input_template_all_path =[]
    for root,dirs,files in os.walk(path,topdown=False) :
        for name in files:
            if os.path.splitext(name)[1]==suffix:
                input_template_all.append(name)
                input_template_all_path.append(os.path.join(root,name))
    return input_template_all, input_template_all_path

st.set_page_config(layout='wide')



st.title("普强项目管理数据看板")
input_folder = st.sidebar.text_input("输入数据文件所在的目录",value = os.path.abspath('.'),key = None)
print(input_folder)
path = input_folder
file = st.sidebar.file_uploader(".xlsx")



char_options = ['多线图','散点图','气泡图','柱状图']
char_type = st.sidebar.selectbox('请选择绘图类型',char_options,placeholder='选择一个类型')

if char_type == '气泡图':
    # chart_data = pd.DataFrame([[4,4,4],[3,3,3],[2,2,2],[4,4,4,],[3,3,3],[2,2,2]],columns=['张三','李四','王五'])
    # st.scatter_chart(chart_data,x_label="日期",y_label="可用人天")
    x = ['1号', '2号', '3号','4号','5号','6号','7号','8号','9号','10号','11号','12号','13号','14号','15号','16号','17号','18号','19号','20号','21号','22号','23号','24号','25号','26号','27号','28号','29号','30号','31号']
    y1 = [5, 4, 3]
    y2 = [4, 3, 2]
    y3 = [5, 4.5, 4]
    trace1 = go.Scatter(
        x=x,
        y=y1,
        mode="markers+lines",
        name='张三',
        marker={"size":8,"symbol":"square"}
    )
    trace2 = go.Scatter(
        x=x,
        y=y2,
        mode='markers+lines',
        name='李四',
        marker={"size":8,"symbol":"square"}
    )
    trace3 = go.Scatter(
        x=x,
        y=y3,
        mode='markers+lines',
        name='王五',
        marker={"size":8,"symbol":"square"}
    )
    fig = go.Figure(data=[trace1, trace2, trace3],
                    layout={"title": "本月可用资源燃尽图（数据为示意）", "xaxis_title": "日期", "yaxis_title": "可用人天","xaxis":{"tickangle":-60}})
    st.plotly_chart(fig, theme='streamlit')

if file:
    #st.write('你选择的文件是：',file)
    # 提取数据
    @st.cache_data
    def load_data(path):
        df_ = pd.read_excel(path)
        df_.columns = df_.columns.str.lower()
        return df_
    df = load_data(file)
    col_list = df.columns
    col_list = col_list.to_list()  # 将DF数据转为列表
    col_list_bak = copy.deepcopy(col_list)  # 备份
    column0_list = df[col_list[0]]
    column1_list = df[col_list[1]]
    print(column0_list)
    print(column1_list)


    if char_type=='柱状图':
        if len(col_list) > 1:
            #采用streamlit方式绘制
            chart_data = pd.DataFrame({"月份":column0_list,"交付总成本（元）":column1_list})
            st.bar_chart(chart_data,x="月份",y="交付总成本（元）")

    if char_type =='多线图':
        if len(col_list) > 1:
            sub_df = df[col_list_bak]
            sub_df = sub_df.drop(df.columns[[0]], axis=1)
            col_list_bak.pop(0)
            #'''采用plotly方式绘制'''
            fig = px.line(sub_df, x=df['time'], y="交付总成本", width=1080, height=550)
            fig.update_layout(legend=dict(orientation="h", ))  # 开启水平显示
            st.plotly_chart(fig, theme='streamlit')
            print(sub_df)
    if char_type == '散点图':
        if len(col_list) > 1:
            sub_df = df[col_list_bak]
            sub_df = sub_df.drop(df.columns[[0]], axis=1)
            col_list_bak.pop(0)
            # 采用go.方式绘制
            trace1 = go.Bar(x=column0_list, y=column1_list, name='需验收总额（元）')
            fig = go.Figure(data=[trace1], layout={"template": "plotly_dark"})
            st.plotly_chart(fig, theme='streamlit')


else:
    st.title('请上传文件！')


with st.empty():
    for seconds in range(60):
        st.write(f"{seconds} seconds has passed")
        time.sleep(1)
    st.write(f"1 minutes over!")

