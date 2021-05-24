import pandas as pd
import numpy as np
from pylab import *

def load_data(file_name,):
    df = pd.read_excel(file_name, engine = 'openpyxl')
    virables = df.columns.to_list()
    for i in removed_features:
        virables.remove(i)
    df_used = df[virables] 
    return df_used

def plot_pcc_correlation_map(data,x_label,label_high_correlation=True,show_color_bar = True,
                             label_text_size=20,x_label_size=18,dot_size=4500):
    pccdata = data.corr()
    z = np.array(pccdata)
    n = data.shape[1]
    plt.figure(figsize=(10,10)) 
    plt.ylim([-.5,n-.5])
    plt.xlim([-.5,n-.5])
    plot_setting()
    plt.xticks([i for i in range(n)], data.columns.to_list(), rotation=0,size = 20)
    plt.yticks([i for i in range(n)], data.columns.to_list()[::-1], rotation=0,size = 20)
    cm = plt.cm.RdBu
    
    x_pos = []
    y_pos_temp = []
    for i in range(n-1,-1,-1):
        x_pos.append([i]*n)
    for i in range(n):    
        y_pos_temp.append(i)
    y_pos  = []
    for i in range(n):
        y_pos.append(y_pos_temp)
    plt.xlabel(x_label,size=x_label_size,labelpad=12)

    if label_high_correlation:
        for i in range(z.shape[0]):
            for j in range(z.shape[1]-1,-1,-1):
                num = abs(round(z[i][j],2))
                if num >= .9 and num<.99999:
                    plt.scatter(i,z.shape[0]-1-j,marker = 's',s=900,c='white',edgecolors='darkgreen',linewidths=2)
                    plt.text(i,z.shape[0]-1-j,'%.2f'%round(z[i][j],2),verticalalignment="center",
                             horizontalalignment="center",color='white',size=label_text_size)
 
    # 画散点图和分隔线
    for i in range(z.shape[0]):
        for j in range(z.shape[1]-1,-1,-1):
            num = abs(round(z[i][j],2))
    
    plt.scatter(y_pos,x_pos,s=abs(z)*dot_size,c=np.array(z),vmin=-1,vmax=1,cmap = cm)
    for i in range(n):
        plt.vlines(i+.5, -1, n,lw=.5,color='grey',alpha=0.6)
        plt.hlines(i+.5, -1, n,lw=.5,color='grey',alpha=0.6)
        
    # 保存图片
    if show_color_bar:
        cb = plt.colorbar(pad=0.03,aspect=30)
        cb.ax.tick_params(labelsize=20) #设置colorbar字体大小
    plt.tight_layout()
    plt.savefig('pcc_correlation.pdf',dpi = 900)

def plot_setting():
    ax=plt.gca()
    plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True
    plt.tick_params(which='major',length=7,width=2)
    bwith = 2
    ax.spines['bottom'].set_linewidth(bwith)    
    ax.spines['top'].set_linewidth(bwith)
    ax.spines['left'].set_linewidth(bwith)  
    ax.spines['right'].set_linewidth(bwith)
        
def plot_pcc_correlation_bar(data,target_name,x_label,x_label_size=18):
    bar_data = abs(data.corr()[target_name]).sort_values(ascending = True)[:-1]
    plt.figure(figsize=(11,10.5))
    plot_setting()
    plt.yticks(rotation=0,size = 22)
    plt.xticks(rotation=0,size = 32)
    plt.xlabel(x_label,size=x_label_size,labelpad=12)
    Colors =[]
    for i in data.corr()[target_name].index:
        if data.corr()[target_name][i] > 0:
            Colors.append('darkblue')
        else:
            Colors.append('darkred')
    plt.ylim([-.8,len(bar_data)-.2])
    plt.barh(bar_data.index,width=bar_data,color=Colors)

    plt.tight_layout()
    plt.savefig('pccbar.pdf',dpi = 900)

n = 1
data = load_data(f'interface-{n}-interface energy.xlsx')
plot_pcc_correlation_bar(data,target_name='RIE',
                         x_label=f'Interface {n} pearson correlation coefficient between RIE and virables')

plot_pcc_correlation_map(data,show_color_bar =False,
                         x_label = f'Interface {n} pearson correlation coefficient among all virables')
