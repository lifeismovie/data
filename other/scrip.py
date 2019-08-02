# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 14:43:37 2019

@author: x
"""

import xlwings as xw
import openpyxl
import pandas as pd
import datetime
from pandas.tseries.offsets import Day
import os,win32com.client


##相关参数
date_Y = (datetime.datetime.now() - 1 * Day()).strftime('%Y') 
date_M = (datetime.datetime.now() - 1 * Day()).strftime('%m') 
date_D = (datetime.datetime.now() - 1 * Day()).strftime('%d')
date_W = datetime.datetime.now().strftime('%w')

daban = 'filepath'.format(Y = date_Y,M = date_M, D = date_D)
daban_cut = 'filepath'.format(Y = date_Y,M = date_M, D = date_D)
xiaoban = 'filepath'.format(Y = date_Y,M = date_M, D = date_D)
check_1 = 'filepath'.format(Y = date_Y,M = date_M, D = date_D)
check_2 = 'filepath'.format(Y = date_Y,M = date_M, D = date_D)
check_3 = 'filepath'.format(Y = date_Y,M = date_M, D = date_D)

col_name = ['col1_name','col2_name',.....]#成单所需要的字段


##定义函数
def copy():#从大版复制到小版
    global daban,daban_cut,xiaoban
   
    #移除大版文件密码保护
    
    xcl = win32com.client.Dispatch("Excel.Application")
    pw_str = '123abc' # pw_str为打开密码, 若无 访问密码, 则设为 ''
    filename = daban
    wb = xcl.Workbooks.Open(filename, False, False, None,pw_str)
    xcl.DisplayAlerts = False
    wb.SaveAs(filename, None, '', '')# 保存时可设置访问密码.
    xcl.Quit()
    
    #筛选客服部断点大版成单
    
    df = pd.read_excel(daban,sheet_name='col3_name',header=2)
    df = df[df['col3_name'] == 'xx']
    df.drop('col4_name',axis=1,inplace=True)
    df.to_excel(daban_cut,index=False)
    
    #复制客服部断点大版成单到小版
    
    app = xw.App(visible=False,add_book=False)#启动excel程序
    app.display_alerts = False
    app.screen_updating = False
 
    wb1 = app.books.open(daban_cut)# 打开xlsx
    wb2 = app.books.open(xiaoban)

    sht1 = wb1.sheets[0]#获取sheet
    sht2 = wb2.sheets[0]

    max_row = sht1.used_range.last_cell.row # 获取sheet中最大行列数
    max_column = sht1.used_range.last_cell.column
    
    max_column = openpyxl.cell.cell.get_column_letter(max_column)# 数值转化为EXCEL行序号

    sht2.range('F2:%s%d'%('BK',max_row+1)).value = sht1.range('A1:%s%d'%(max_column,max_row)).value

    wb2.save(xiaoban)

    wb1.close()
    wb2.close()

    app.quit()
    
    #删除大版修改表
    
    path = daban_cut
    if os.path.exists(path):  # 如果文件存在
        os.remove(path)
    # os.unlink(path)
    else:
        print('no such file')  # 则返回文件不存在

def output_23():#导出二组三组成单
    global df_xiaoban,check_2,check_3,col_name
    df_2 = df_xiaoban[df_xiaoban['col5_name']=='是'][col_name]
    df_3 = df_xiaoban[df_xiaoban['col6_name']=='是'][col_name]
    df_2.to_excel(check_2,index=False)
    df_3.to_excel(check_3,index=False)
def output_1():#导出一组成单
    global df_xiaoban,check_1,col_name
    df_1 = df_xiaoban[df_xiaoban['col7_name']=='是'][col_name]
    df_1_2 = df_xiaoban[(df_xiaoban['col8_name']=='xx-xxxx') & (df_xiaoban['col9_name']=='xxx') & (df_xiaoban['col10_name']=='xx')][col_name]
    with pd.ExcelWriter(check_1) as writer:#写进一张excel中不同的sheet
        df_1.to_excel(writer, sheet_name='sheet1',index=False)
        df_1_2.to_excel(writer, sheet_name='sheet2',index=False)

##分星期数调用函数
if date_W == 4:
    print(datetime.datetime.now())
    
    copy()
    
    df_xiaoban = pd.read_excel(xiaoban,header=1)
    
    output_1()
    
    print(datetime.datetime.now())
else:
    print(datetime.datetime.now())
    copy()
    
    df_xiaoban = pd.read_excel(xiaoban,header=1)
    
    output_1()
    
    output_23()
    print(datetime.datetime.now())