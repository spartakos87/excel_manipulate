from xlrd import open_workbook
import json
from collections import OrderedDict
from idx import lst
from idx import paths
from glob import glob as g
from pprint import pprint as pp
import os
from create_total import main as ct
import multiprocessing as m

def x(g,wb,sheet_n,lst_idx):
    #excel_n is the excel file
    # g a list with the range
    # sheet_n , the sheet's name
#    wb= open_workbook(excel_n)
    b= wb.sheet_by_name(sheet_n)
    l=[]
    for k,i in enumerate(range(g[0],g[-1])):
                t=b.row(i)
                d=OrderedDict()
                d['technology']=t[lst_idx[0]].value.strip()
                d['2015']=round(t[lst_idx[1]].value,1)
                d['2020']=round(t[lst_idx[2]].value,1)
                d['2030']=round(t[lst_idx[3]].value,1)
                d['2050']=round(t[lst_idx[-1]].value,1)
                d['position']=20*k
                l.append(d) 
    return l


def xx(g,excel_n,sheet_n,lst_idx):
    dd={}
    wb= open_workbook(excel_n)
    dd['Piechart']=x(g,wb,sheet_n,lst_idx)
    return dd


def save(g,excel_n,sheet_n,name,path,idx_name=0,idx15=4,idx20=5,idx30=7,idx50=11):
    lst_idx=[idx_name,idx15,idx20,idx30,idx50]
    with open('JSON_DATA/'+path+'/'+name+'.json','w') as o:
         json.dump(xx(g,excel_n,sheet_n,lst_idx),o,sort_keys=False, indent=4,ensure_ascii=False)




def energy_cost(excel_n,path,idx_name=0,idx15=6,idx20=7,idx30=8,idx50=12):
    name ="Energy_costs"
    g=[94,98]
    sheet_n="EU28"
    #CLIMA....xls
    lst_idx=[idx_name,idx15,idx20,idx30,idx50]
    with open('JSON_DATA/'+path+'/'+name+'.json','w') as o:
         json.dump(xx(g,excel_n,sheet_n,lst_idx),o,sort_keys=False, indent=4,ensure_ascii=False)


def system_cost(excel_n,path,idx_name=0,idx15=6,idx20=7,idx30=8,idx50=12):
    name = "System_costs"
    g=[104,107] # 105 = 105-107
    sheet_n="EU28"
    #CLIMA....xls
    lst_idx=[idx_name,idx15,idx20,idx30,idx50]
    out_put=xx(g,excel_n,sheet_n,lst_idx)
#    pp(out_put['Piechart'][0]['technology'])
#    pp(out_put['Piechart'][1]['technology'])
#    pp(out_put['Piechart'][-1]['technology'])
    system_ETS=out_put['Piechart'][0]
    Auction=out_put['Piechart'][-1]
    for i in ['2015','2020','2030','2050']:
        system_ETS[i]=system_ETS[i]-Auction[i]
    out_put['Piechart'][0]=system_ETS
    with open('JSON_DATA/'+path+'/'+name+'.json','w') as o:
         json.dump(out_put,o,sort_keys=False, indent=4,ensure_ascii=False)

def find_files(localtion):
    l = g(localtion+'/*xlsx')
    clima=[i for i in l if "VCLIMA" in i][0]
    new = [i for i in l if "_new-"+localtion.split('/')[-1] in i][0]
    return [new,clima]

def create_folder(folder):
    if not os.path.exists("JSON_DATA/"+folder):
       os.makedirs("JSON_DATA/"+folder)

def main(localtion):
    new,clima = find_files(localtion)
#    print(new)
    path=new.split('-')[-1].split('.')[0]
#    print(path)
    create_folder(path)
#   list(map(lambda y:save(y[1],new,y[-1],y[0],path),lst))
    energy_cost(clima,path)
    system_cost(clima,path)
    list(map(lambda y:save(y[1],new,y[-1],y[0],path),lst))
    ct("JSON_DATA/"+path+"/")

def multi_foders():
#   list(map(lambda y: main(y),paths))
    for i in paths:
       print(i)
       main(i)
