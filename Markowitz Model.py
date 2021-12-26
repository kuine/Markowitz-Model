# Dash Bot (To plot graph of Markowitz Model)
import numpy as np
import matplotlib.pyplot as plt

#Data address
import csv
key=["BSE 500","TATA MOTORS","Akzo Nobel","Indian Hotel Co.","Biocon"]
index="C:\\Users\\ASUS\\OneDrive - Sardar Vallabhai National Institute of Technology\\Desktop\\Dash BOT\\Indices-BSE (2016-2020)\\BSE 500.csv"
stock1="C:\\Users\\ASUS\\OneDrive - Sardar Vallabhai National Institute of Technology\\Desktop\\Dash BOT\\Stock ((2016-2021)\\500570.csv"
stock2="C:\\Users\\ASUS\\OneDrive - Sardar Vallabhai National Institute of Technology\\Desktop\\Dash BOT\\Stock ((2016-2021)\\500710.csv"
stock3="C:\\Users\\ASUS\\OneDrive - Sardar Vallabhai National Institute of Technology\\Desktop\\Dash BOT\\Stock ((2016-2021)\\500850.csv"
stock4="C:\\Users\\ASUS\\OneDrive - Sardar Vallabhai National Institute of Technology\\Desktop\\Dash BOT\\Stock ((2016-2021)\\532523.csv"

#Markowitz Distribution
import itertools
p=int(input("Resolution "))
l=[]
for x in range(0,101,p):
    l.append(x)
cases=[q for q in itertools.product(l, repeat=5) if sum(list(q))==100]
print("Number of cases",len(cases))

#Data to list
wb=open(index)
data = csv.reader(wb)
index_data=list(data)
wb=open(stock1)
data = csv.reader(wb)
stock_data_1=list(data)
wb=open(stock2)
data = csv.reader(wb)
stock_data_2=list(data)
wb=open(stock3)
data = csv.reader(wb)
stock_data_3=list(data)
wb=open(stock4)
data = csv.reader(wb)
stock_data_4=list(data)

#Functions
#1:Change
def change(data,index):
    change=[]
    for x in range(1,len(data)-1):
        y=(float(data[x+1][index])-float(data[x][index]))/float(data[x][index])
        change.append(y)
    return change
#2:Mean
def mean(data):
    mean=0
    for x in data:
        mean=mean+x
    mean=mean/len(data)
    return mean
#3:Variance
def var(data):
    var=0
    mean_temp=mean(data)
    for x in data:
        var=var+(x-mean_temp)**2
    var=var/len(data)
    return var
#4:Standard Deviation
def stddev(data):
    std=pow(var(data),0.5)
    return std
#5:Covariance
def covar(data1,data2):
    mean1=mean(data1)
    mean2=mean(data2)
    covar=0
    for x in range(len(data1)):
        covar=covar+(data1[x]-mean1)*(data2[x]-mean2)/len(data1)
    return covar            
#6:Coefficient of correlation
def correl(data1,data2):
    covar1=covar(data1,data2)
    std1=stddev(data1)
    std2=stddev(data2)
    correl=covar1/(std1*std2)
    return correl
#7:Markowitz Return
def ret(case,data1,data2,data3,data4,data5):
    ret=(case[0]*mean(data1)+case[1]*mean(data2)+case[2]*mean(data3)+case[3]*mean(data4)+case[4]*mean(data5))
    return ret
#8:Markowitz Risk
def risk(case,correl):
    temp=np.dot(case,correl)
    risk=np.dot(temp,case)
    return risk
#9:Sharpe Ratio
def shrp(data1,data2,rf):
    sharpe=(data1-rf)/data2
    return sharpe
                 
#Data
#1:Change
index_change=change(index_data,1)
stock_1_change=change(stock_data_1,1)
stock_2_change=change(stock_data_2,1)
stock_3_change=change(stock_data_3,1)
stock_4_change=change(stock_data_4,1)
data=[index_change,stock_1_change,stock_2_change,stock_3_change,stock_4_change]

#2:Correlation Matrix
correl_mat=[[],[],[],[],[]]
for x in range(5):
    for y in range (5):
        correl_mat[x].append(covar(data[x],data[y]))
correl_mat=np.array(correl_mat)

#Output
#1:List of Markowitz return
ret_final=[]
for x in cases:
    ret_final.append(ret(x,index_change,stock_1_change,stock_2_change,stock_3_change,stock_4_change))

#2:List of Markowitz risks
risk_final=[]
for x in cases:
    risk_final.append(risk(x,correl_mat))

#3:Sharpe Analysis
rf=float((input("Risk free return ")))
ret_max=[0]
risk_max=[0]
sharpe_max=[0]
temp1=list(ret_final)
temp2=list(risk_final)
for x in range(len(temp1)):
    sharpe=shrp(temp1[x],temp2[x],rf)
    if sharpe>sharpe_max[0]:
        ret_max[0]=temp1[x]
        risk_max[0]=temp2[x]
        sharpe_max[0]=sharpe
np.array(ret_max)
np.array(risk_max)
#4:Graph (Scatter Plot)
plt.scatter(risk_final,ret_final)
plt.scatter(risk_max,ret_max,c='#FF0000')
plt.xlabel("Risk")
plt.ylabel("Return")
plt.show()

#5:Optimal Portfolio
x=ret_final.index(float(ret_max[0]))
print(cases[x])
a={}
for y in range(5):
    a[key[y]]=cases[x][y]
print(a)
        
        


       