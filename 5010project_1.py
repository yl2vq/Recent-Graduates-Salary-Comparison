import numpy as np

import pandas as pd

import matplotlib.pyplot as plt



grads = pd.read_csv('recent-grads.csv')

pd.options.display.max_columns = None #display all columns in Jupyter Notebook


## Data cleaning
# Change column names to lowercase
grads.columns = map(str.lower, grads.columns)

# Change major and major_category to lowercase
grads['major'] = grads['major'].str.lower()
grads['major_category'] = grads['major_category'].str.lower()


## Data analysis
## part 1

#####pie chart of proportion of major categories

grads[['total']].groupby(grads['major_category']).sum().plot.pie(subplots=True, figsize=(12,12), fontsize=12)
plt.axis('off')



#####job quality ratio stacked barplot

grads['job total'] = grads['college_jobs'] + grads['non_college_jobs'] #make job total column adding college job and noncollege job

grads['collegejobp'] = grads['college_jobs'] / grads['job total']# find the ratio of college job

grads['noncollegejobp'] = grads['non_college_jobs'] / grads['job total']#find the ratio of noncollege job

grads[['collegejobp','noncollegejobp']].groupby(grads['major_category']).mean().sort_values(by='noncollegejobp',ascending=True).plot(kind='barh', figsize=(12,6), fontsize=12, title='college jobs vs non-college jobs',color=['darksalmon','grey'],stacked=True)







#####gender ratio stacked barplot

grads['male Prop'] = grads['men'] / (grads['total']) #create men ratio column

grads['female Prop'] = grads['women'] / (grads['total']) #create women ratio column

grads[['male Prop','female Prop']].groupby(grads['major_category']).mean().sort_values(by='male Prop').plot(kind='barh',figsize=(12,6), fontsize=12, title='Average Gender Proportion for Each Category', color=['navy','orange'],stacked=True)

plt.xlim(0, 1)



#####scatter plot of salary vs gender ratio 

x=grads['male Prop'] #define x as gender ratio

y=grads['median']  #define y as median salary

colors = pd.Series(len(x)*['orange'])

listm = list(np.unique(grads['major_category'])) #list of major groups

listc = ['grey','grey','grey','grey','grey','grey','blue','red','grey','grey','grey','grey','grey','grey','grey','grey']

#list of colors

for i in listm: #apply color to corresponding major groups

    colors[grads['major_category']==i] = listc[listm.index(i)]

plt.figure(figsize=(12,6)) #change the size of plot

plt.title('median salaries for each major categories') #make title

plt.xlabel('male Prop') #make x label

plt.ylabel('median Salary') #make y label

plt.scatter(x, y, c=colors)   #make scatter plot

plt.show()



## part2

mu = grads[['major', 'major_category', 'unemployment_rate']]

mutop5 = mu.sort_values(ascending=False, by='unemployment_rate')[:5] ## top5 unemployment

mutop5.set_index('major', inplace=True) # set index with major

mutop5.sort_values(ascending=True, by='unemployment_rate').plot(kind='barh', title='Top5 unemployment Rate by major', color = ['y']) ## top5 ur by major



mubot5 = mu.sort_values(ascending=True, by='unemployment_rate')[:5] ## bottom 5 unemployment 

mubot5.set_index('major', inplace=True) # set index with major

mubot5.sort_values(ascending=True, by='unemployment_rate').plot(kind='barh', title='Bottom5 unemployment Rate by major') ## bot5 ur by major





grads['unemployment_rate'].groupby(grads['major_category']).mean().sort_values(ascending=True).plot(kind='barh', title='unemployment Rate by major Category', colormap='Paired') ## major_category unemploy rates





PSur = mu[mu['major_category'] == 'physical sciences'] ## physical science unemploy 

PSur.set_index('major', inplace=True) # set index with major



SSur = mu[mu['major_category'] == 'social science'] ## social science unemploy

SSur.set_index('major', inplace=True) # set index with major



PSur.sort_values(ascending=True, by='unemployment_rate').plot(kind='barh', title='unemployment Rate by major (physical science)', color=['r'] ) ## PS -> major

SSur.sort_values(ascending=True, by='unemployment_rate').plot(kind='barh', title='unemployment Rate by major (Sosical science)', color=['g']) ## SS -> major



## part3



## list for STEM degree

stemlist = ['biology & life science','computers & mathematics','engineering','physical sciences','agriculture & natural resources','health','physical sciences']



## add 'STEM' column in the original dataset

def stem(df):

    if df['major_category'] in stemlist:

        return 'STEM'

    else:

        return 'non-STEM'



## apply 'ste, function 

grads['STEM']=grads.apply(stem,axis =1)



stem_grads = grads.loc[grads['STEM']=='STEM']





## subset non-STEM data

non_stem_grads = grads.loc[grads['STEM']=='non-STEM']



##  groupby 'STEM'

grads_by_stem = grads.groupby('STEM')



## median Salary by STEM vs non-STEM

grads_by_stem['median'].mean().sort_values(ascending = False).plot(kind='barh', figsize=(12,6), fontsize=12, title='median Salary by STEM vs non-STEM')

plt.ylabel('')

plt.rcParams.update({'font.size': 20})

grads_by_stem['median'].mean()



## unemployment rate STEM vs non-STEM

grads_by_stem['unemployment_rate'].mean().sort_values(ascending = True).plot(kind='barh', figsize=(12,6), fontsize=12, title='unemployment Rate by STEM vs non-STEM')

plt.ylabel('')

plt.rcParams.update({'font.size': 20})

grads_by_stem['unemployment_rate'].mean()



## college job vs non-college job by STEM vs non-STEM 

grads_by_stem['college_jobs', 'non_college_jobs'].mean().sort_values(by='college_jobs').plot(kind='barh', figsize=(12,6), fontsize=12, title='college_job vs non_college_job  by STEM vs non-STEM')

plt.ylabel('')

plt.rcParams.update({'font.size': 20})





## Explore STEM major grads ##



## group stem grads by major category

stem_grads_by_cat = stem_grads.groupby(by='major_category')

## The number of students in STEM major category

stem_grads_by_cat['total'].sum().sort_values(ascending = True).plot(kind='barh', figsize=(12,6), fontsize=12, title='Number of graduates by major Category ')

plt.ylabel('')

plt.rcParams.update({'font.size': 20})



## median Salary by STEM major category

stem_grads_by_cat['median'].mean().sort_values(ascending =True).plot(kind='barh', figsize=(12,6), fontsize=12, title='median Income by major Category ')

plt.ylabel('')

plt.rcParams.update({'font.size': 20})



## unemployment rate by STEM major category

stem_grads_by_cat['unemployment_rate'].mean().sort_values().plot(kind='barh', figsize=(12,6), fontsize=12, title='unemployment Rate by major Category')

plt.ylabel('')

plt.rcParams.update({'font.size': 20})





## explore DS ##



## Computer & Mathematics major category subset

cm = stem_grads.loc[stem_grads['major_category']=='Computers & Mathematics']



## Top 5 unemployment rate comparison in Computer & Mathematics moajor category 

cm_top5 = cm.loc[cm['unemployment_rate'] >0 ].sort_values(ascending = False, by='unemployment_rate')[0:5]

cm_top5[['major','unemployment_rate']]







## college job vs non-college job comparison in Computer & Mathematics moajor category 

stem_grads_by_cat['college_jobs', 'non_college_jobs'].mean().sort_values(by='college_jobs').plot(kind='barh', figsize=(12,6), fontsize=12, title='college job vs non-college job by major Category')





## DS major proxies 

proxies = ['COMPUTER PROGRAMMING AND DATA PROCESSING', 'COMPUTER AND INFORMATION SYSTEMS', 'INFORMATION sciENCES', 'STATISTICS AND DECISION sciENCE']

ds_grad = stem_grads.loc[grads['major'].isin(proxies)]

## non-DS 

non_ds_grad = stem_grads.loc[~grads['major'].isin(proxies)]

non_ds_grad.head()





## created column 'DS' in the orifinal dataframe 

def ds(df):

    if df['major'] in proxies:

        return 'DS'

    else:

        return 'non-DS'



stem_grads['DS']=stem_grads.apply(ds,axis =1)

stem_grads.head()







## group STEM degree by 'DS'

stem_grads_by_ds = stem_grads.groupby(by='DS')



## unemployment rate by DS vs non-DS

stem_grads_by_ds['unemployment_rate'].mean().sort_values(ascending = False).plot(kind='barh', figsize=(12,6), fontsize=12, title='unempolyment rate by DS vs non-DS')

plt.ylabel('')

plt.rcParams.update({'font.size': 20})





## median Income by DS vs non-DS 

stem_grads_by_ds['median'].mean().sort_values().plot(kind='barh', figsize=(12,6), fontsize=12, title='median Income by DS vs non-DS')

plt.ylabel('')

plt.rcParams.update({'font.size': 20})



## DS major subset

ds_major = stem_grads.loc[stem_grads['DS']=='DS']

ds_major

ds_major[['major','major_category','sample_size','median','p25th','p75th','unemployment_rate']]





 

