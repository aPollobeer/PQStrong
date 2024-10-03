# -*- coding: UTF-8 -*-

import os
import copy
import time
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


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

