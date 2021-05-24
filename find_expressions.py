import pandas as pd
import numpy as np
import os
from sklearn import metrics
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from itertools import combinations

def load_data(file_name):
    df = pd.read_csv(file_name)
    virables = df.columns.to_list()
    for i in ['ELE']:
        virables.remove(i)
    df_used = df[virables] 
    return df_used

n = 1
df = load_data(f'interface{1}.csv')

def extract_virables(data,y_label):
    virable_names = data.drop(y_label,axis=1).columns.to_list()
    return virable_names

def initial_change(data,virables):
    for v in virables:
        data['1/'+v] = 1/data[v]
        data[v+'^2'] = np.power(data[v],2)
        data['1/('+v+'^2)'] = 1/(np.power(data[v],2))
        data[v+'^3'] = np.power(data[v],3)
        data['1/('+v+'^3)'] = 1/(np.power(data[v],3))
#         开根号和对数
        if min(df[v])>0:
            data[f'sqrt({v})'] = np.sqrt(data[v])
            data[f'1/sqrt({v})'] = 1/np.sqrt(data[v])
            data[f'log({v})'] = np.log(data[v])
            data[f'1/log({v})'] = 1/np.log(data[v])
            data[f'exp({v})'] = np.exp(data[v])
            data[f'1/exp({v})'] = 1/np.exp(data[v])
    return data

def combination_virables(data,virables,num_of_virables=2):
    for i in combinations(virables,num_of_virables):
        data[i[0]+'*'+i[1]] = data[i[0]]*data[i[1]]
    return data

virables = extract_virables(df,y_label='RIE')
df = initial_change(df,virables)

new_virables = extract_virables(df,y_label='RIE')
combination_virables(df,new_virables)
df.shape

viarables = []
formula = []
rmse = []
R2 = []
target = df['RIE']

for v in list(df.columns)[1:]:
    x = df[v].values.reshape(-1,1)
    model = LinearRegression()
    model.fit(x,target)
    viarables.append(v)
    if model.intercept_ > 0:
        formula.append(f'y = {round(model.coef_[0],3)}*x + {round(model.intercept_,3)}')
    else:
        formula.append(f'y = {round(model.coef_[0],3)}*x {round(model.intercept_,3)}')
    rmse.append(metrics.mean_squared_error(model.predict(x),target)**0.5)
    R2.append(r2_score(model.predict(x),target))

    
results = {
    'varables':viarables,
    'expressions':formula,
    'rmse':rmse,
    'R2':R2
}
    
re = pd.DataFrame(results)
re.sort_values(by="rmse" , inplace=True, ascending=True) 
re.to_csv(f'interface{n}_1term_regression_results.csv',index = None)

viarables = []
formula = []
rmse = []
R2 = []

for v in list(df.columns)[1:]:
    x = df[v].values.reshape(-1,1)
    model = LinearRegression()
    model.fit(x,target)
    viarables.append(v)
    if model.intercept_ > 0:
        formula.append(f'y = {round(model.coef_[0],3)}*x + {round(model.intercept_,3)}')
    else:
        formula.append(f'y = {round(model.coef_[0],3)}*x {round(model.intercept_,3)}')
    rmse.append(metrics.mean_squared_error(model.predict(x),target)**0.5)
    R2.append(r2_score(model.predict(x),target))


for v in combinations(list(df.columns)[1:],2):
    x = df[list(v)].values.reshape(-1,len(v))
    model = LinearRegression()
    model.fit(x,target)
    viarables.append(v)
    
    regression_formula = f"y = {round(model.coef_[0],3)}*x1 "
    if model.coef_[1] >= 0:
        regression_formula += f'+{round(model.coef_[1],3)}*x2 '
    else:
        regression_formula += f'{round(model.coef_[1],3)}*x2 '
    if model.intercept_ > 0:
        regression_formula += f'+{round(model.intercept_,3)}'
    else:
        regression_formula += f'{round(model.intercept_,3)}'

    formula.append(regression_formula)
    rmse.append(metrics.mean_squared_error(model.predict(x),target)**0.5)
    R2.append(r2_score(model.predict(x),target))
    
    
results = {
    'varables':viarables,
    'expressions':formula,
    'rmse':rmse,
    'R2':R2
}
    
re = pd.DataFrame(results)
re.sort_values(by="rmse" , inplace=True, ascending=True) 
re.to_csv(f'interface{n}_1and2term_regression_results.csv',index = None)
