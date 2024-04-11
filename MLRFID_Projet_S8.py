#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import warnings 
warnings.filterwarnings("ignore")
import datetime


# 

# In[2]:



# Définition du chemin d'accès au dossier contenant les données anonymes
pathfile = r'data_anonymous'

# Création d'un dataframe reflist pour stocker la liste des EPC de chaque box
reflist = pd.DataFrame()

# Parcours des fichiers du dossier pour récupérer les données reflist
files = os.listdir(pathfile)
for file in files:
    print(file)
    if file.startswith('reflist_'):
        temp = pd.read_csv(os.path.join(pathfile, file), sep=',').reset_index(drop=True)[['Epc']]
        temp['refListId'] = file.split('.')[0]
        reflist = reflist._append(temp)

# Renommage de la colonne refListId en refListId_actual
reflist = reflist.rename(columns={'refListId': 'refListId_actual'})

# Conversion de la chaîne de caractères de refListId_actual en un entier
reflist['refListId_actual'] = reflist['refListId_actual'].apply(lambda x: int(x[8:]))

# Calcul du nombre d'EPC uniques par refListId_actual
Q_refListId_actual = reflist.groupby('refListId_actual')['Epc'].nunique().rename('Q refListId_actual').reset_index(drop=False)

# Fusion des dataframes reflist et Q_refListId_actual sur la colonne refListId_actual
reflist = pd.merge(reflist, Q_refListId_actual, on='refListId_actual', how='left')

# Affichage des premières lignes du dataframe reflist
reflist.head()


# 

# In[3]:


# pathfile: chemin du dossier contenant les fichiers de lecture RFID
# df: lectures RFID
df = pd.DataFrame()

# Liste des fichiers dans le dossier pathfile
files = os.listdir(pathfile)

# Boucle à travers les fichiers pour extraire les lectures RFID
for file in files:
    print(file)
    if file.startswith('ano_APTags'):
        temp = pd.read_csv(os.path.join(pathfile, file), sep=',')
        df = df._append(temp)

# Conversion de la colonne "LogTime" en format datetime
df['LogTime'] = pd.to_datetime(df['LogTime'], format='%Y-%m-%d-%H:%M:%S')

# Conversion des colonnes "TimeStamp" et "Rssi" en type float
df['TimeStamp'] = df['TimeStamp'].astype(float)
df['Rssi'] = df['Rssi'].astype(float)

# Suppression des colonnes "Reader", "EmitPower" et "Frequency" du dataframe
df = df.drop(['Reader', 'EmitPower', 'Frequency'], axis=1).reset_index(drop=True)

# Réorganisation de l'ordre des colonnes dans le dataframe
df = df[['LogTime', 'Epc', 'Rssi', 'Ant']]

# Les antennes 1 et 2 font face à la boîte lorsqu'elles sont près de la cellule photoélectrique IN
# Les antennes 3 et 4 font face à la boîte lorsqu'elles sont près de la cellule photoélectrique OUT
Ant_loc = pd.DataFrame({'Ant':[1,2,3,4],'loc':['in','in','out','out']})
df = pd.merge(df, Ant_loc, on=['Ant'])

# Tri des données dans l'ordre croissant en fonction de l'heure de lecture "LogTime"
df = df.sort_values('LogTime').reset_index(drop=True)

# Affichage des 5 premières lignes du dataframe "df"
df.head()




# In[4]:


df_reflist = pd.merge(df , reflist , on='Epc', how='left')
df_reflist =df_reflist[['Epc', 'LogTime', 'Rssi', 'loc', 'refListId_actual', 'Q refListId_actual']]
df_reflist.head()


# In[5]:


# timing: photocells a time window for each box: start/stop (ciuchStart, ciuchStop)
# Définition du nom du fichier CSV contenant les données de timing
file=r'ano_supply-process.2019-11-07-CUT.csv'

# Lecture du fichier CSV à l'aide de la bibliothèque pandas
timing=pd.read_csv(os.path.join(pathfile,file),sep=',')

# Ajout de deux colonnes 'file' et 'date' au DataFrame 'timing'
timing['file']=file
timing['date']=pd.to_datetime(timing['date'],format='%d/%m/%Y %H:%M:%S,%f')

# Conversion des valeurs de la colonne 'ciuchStart' en format datetime et stockage dans une nouvelle colonne 'ciuchStart'
timing['ciuchStart']=pd.to_datetime(timing['ciuchStart'],format='%d/%m/%Y %H:%M:%S,%f')

# Conversion des valeurs de la colonne 'ciuchStop' en format datetime et stockage dans une nouvelle colonne 'ciuchStop'
timing['ciuchStop']=pd.to_datetime(timing['ciuchStop'],format='%d/%m/%Y %H:%M:%S,%f')

# Conversion des valeurs de la colonne 'timestampStart' et 'timestampStop' en float
timing['timestampStart']=timing['timestampStart'].astype(float)
timing['timestampStop']=timing['timestampStop'].astype(float)

# Tri des données dans le DataFrame 'timing' par ordre croissant de la colonne 'date'
timing=timing.sort_values('date')


timing.loc[:,'refListId']=timing.loc[:,'refListId'].apply(lambda x:int(x[8:]))

# Extraction d'une sous-section du DataFrame 'timing' contenant les colonnes 'refListId', 'ciuchStart' et 'ciuchStop'
timing=timing[['refListId', 'ciuchStart', 'ciuchStop']]

# Affichage des 50 premières lignes du DataFrame 'timing'
timing[:50]




# In[6]:


# ciuchStart_up starts upstream ciuchStart, half way in between the previous stop and the actual start
# Définition de la fenêtre de capture de ciuchStart_up en amont, qui commence à mi-chemin entre le stop précédent et le début effectif
# Ajout des colonnes ciuchStop_last et refListId_last contenant les valeurs des colonnes ciuchStop et refListId respectivement décalées d'une ligne vers le haut
timing[['ciuchStop_last']]=timing[['ciuchStop']].shift(1)
timing[['refListId_last']]=timing[['refListId']].shift(1)

# Calcul de la valeur de la colonne ciuchStartup qui représente le début de la fenêtre de capture de ciuchStart_up
timing['ciuchStartup']=timing['ciuchStart'] - (timing['ciuchStart'] - timing['ciuchStop_last'])/2

# Ajout des colonnes ciuchStop_last et ciuchStartup à la première ligne du DataFrame 'timing'
timing.loc[0,'refListId_last']=timing.loc[0,'refListId']
timing.loc[0,'ciuchStartup']=timing.loc[0,'ciuchStart']-datetime.timedelta(seconds=10)
timing.loc[0,'ciuchStop_last']=timing.loc[0,'ciuchStartup']-datetime.timedelta(seconds=10)

# Conversion de la colonne refListId_last en integer
timing['refListId_last']=timing['refListId_last'].astype(int)

# Calcul de la valeur de la colonne ciuchStopdown qui représente la fin de la fenêtre de capture de ciuchStart_up
timing['ciuchStopdown']= timing['ciuchStartup'].shift(-1)

# Ajout de la valeur de la colonne ciuchStopdown à la dernière ligne du DataFrame 'timing'
timing.loc[len(timing)-1,'ciuchStopdown']=timing.loc[len(timing)-1,'ciuchStop']+datetime.timedelta(seconds=10)

# Extraction d'une sous-section du DataFrame 'timing' contenant les colonnes refListId, refListId_last, ciuchStartup, ciuchStart, ciuchStop, et ciuchStopdown
timing=timing[['refListId', 'refListId_last','ciuchStartup', 'ciuchStart','ciuchStop','ciuchStopdown']]

# Affichage des premières 12 lignes du DataFrame 'timing'
timing[:12]


# In[7]:


# t0_run = a new run starts when box 0 shows up
t0_run=timing[timing['refListId']==0] [['ciuchStartup']]
t0_run=t0_run.rename(columns={'ciuchStartup':'t0_run'})
t0_run=t0_run.groupby('t0_run').size().cumsum().rename('run').reset_index(drop=False)
t0_run=t0_run.sort_values('t0_run')
# 
# each row in timing is merged with a last row in t0_run where t0_run (ciuchstart) <= timing (ciuchstart)
timing=pd.merge_asof(timing,t0_run,left_on='ciuchStartup',right_on='t0_run', direction='backward')
timing=timing.sort_values('ciuchStop')
timing=timing[['run', 'refListId', 'refListId_last', 'ciuchStartup','ciuchStart','ciuchStop','ciuchStopdown','t0_run']]
timing.head()
timing[:12]


# In[8]:


# box 0 always starts
timing[timing['refListId']==0].head()


# In[9]:


# Création d'une figure de taille 12x6 pouces
plt.figure(figsize=(12,6))

# Calcul des durées en secondes pour chaque étape, en utilisant des expressions lambda pour convertir des Timedelta en secondes
up=(timing['ciuchStart']-timing['ciuchStartup']).apply(lambda x:x.total_seconds())
mid=(timing['ciuchStop']-timing['ciuchStart']).apply(lambda x:x.total_seconds())
down=(timing['ciuchStopdown']-timing['ciuchStop']).apply(lambda x:x.total_seconds())

# Création d'un graphique , avec les durées pour chaque étape, et des labels pour chaque boîte
plt.boxplot([up,mid,down],labels=['ciuchStartup > ciuchStart','ciuchStart > ciuchStop','ciuchStop > ciuchStopdown'])

# Activation de la grille
plt.grid()

# Ajout d'un titre au graphique
plt.title('durations: Startup>Start, Start>Stop, Stop>Stopdown',size=16)

# Affichage du graphique
plt.show()







# In[10]:


# Création d'un DataFrame vide pour stocker les tranches de temps
slices = pd.DataFrame()

# Pour chaque intervalle de temps entre deux points de référence de temps
for i, row in timing.iterrows():
    
    # Récupération des points de référence de temps
    ciuchStartup = row['ciuchStartup']
    ciuchStart = row['ciuchStart']
    ciuchStop = row['ciuchStop']
    ciuchStopdown = row['ciuchStopdown']
    
    # Définition du nombre de tranches à créer entre chaque point de référence
    steps = 4
    
    # Création d'un DataFrame contenant "steps" tranches équidistantes entre ciuchStartup et ciuchStart
    up = pd.DataFrame(index=pd.date_range(start=ciuchStartup, end=ciuchStart, periods=steps))            .reset_index(drop=False).rename(columns={'index': 'slice'})
    up.index = ['up_'+str(x) for x in range(steps)]
    slices = slices._append(up)
    
    # Création d'un DataFrame contenant "steps" tranches équidistantes entre ciuchStart et ciuchStop
    mid = pd.DataFrame(index=pd.date_range(start=ciuchStart, end=ciuchStop, periods=steps))             .reset_index(drop=False).rename(columns={'index': 'slice'})
    mid.index = ['mid_'+str(x) for x in range(steps)]
    slices = slices._append(mid)
    
    # Création d'un DataFrame contenant "steps" tranches équidistantes entre ciuchStop et ciuchStopdown
    down = pd.DataFrame(index=pd.date_range(start=ciuchStop, end=ciuchStopdown, periods=steps ))              .reset_index(drop=False).rename(columns={'index': 'slice'})
    down.index = ['down_'+str(x) for x in range(steps)]
    slices = slices._append(down)

# Renommage de la colonne 'index' en 'slice_id' et fusion avec le DataFrame 'timing'
slices = slices.reset_index(drop=False).rename(columns={'index':'slice_id'})
timing_slices = pd.merge_asof(slices, timing, left_on='slice', right_on='ciuchStartup', direction='backward')

# Sélection des colonnes souhaitées pour le résultat final
timing_slices = timing_slices[['run', 'refListId', 'refListId_last', 'slice_id', 'slice', 'ciuchStartup', 'ciuchStart', 'ciuchStop', 'ciuchStopdown', 't0_run']]

timing_slices.head()



# In[11]:


# merge between df and timing
# merge_asof needs sorted df > df_ref
df_reflist=df_reflist[ (df_reflist['LogTime']>=timing['ciuchStartup'].min()) & (df_reflist['LogTime']<=timing['ciuchStopdown'].max())  ]
df_reflist=df_reflist.sort_values('LogTime')
# 
# each row in df_ref is merged with the last row in timing where timing (ciuchstart_up) < df_ref (logtime)
# 
# df_timing=pd.merge_asof(df_ref,timing,left_on=['LogTime'],right_on=['ciuchStartup'],direction='backward')
# df_timing=df_timing.dropna()
# df_timing=df_timing.sort_values('LogTime').reset_index(drop=True)
# df_timing=df_timing[['run', 'Epc','refListId', 'refListId_last', 'ciuchStartup',\
#                      'LogTime', 'ciuchStop', 'ciuchStopdown','Rssi', 'loc', 'refListId_actual']]
# 
# each row in df_ref is merged with the last row in timing_slices where timing (slice) < df_ref (logtime)
# 
df_timing_slices=pd.merge_asof(df_reflist,timing_slices,left_on=['LogTime'],right_on=['slice'],direction='backward')
df_timing_slices=df_timing_slices.dropna()
df_timing_slices=df_timing_slices.sort_values('slice').reset_index(drop=True)
df_timing_slices=df_timing_slices[['run', 'Epc','refListId', 'refListId_last', 'ciuchStartup','slice_id','slice','LogTime',                       'ciuchStart','ciuchStop', 'ciuchStopdown', 'Rssi', 'loc','t0_run']]
df_timing_slices.head()


# In[12]:


# 


# In[13]:


# df_timing_slices=pd.merge(df_timing_slices, reflist, on='Epc',how='left')
# df_timing_slices = df_timing_slices [ ~((df_timing_slices['refListId']==0) & (df_timing_slices['refListId_actual']==9)) ]
# # 
# df_timing_slices = df_timing_slices [ ~((df_timing_slices['refListId']==9) & (df_timing_slices['refListId_actual']==0)) ]
# # # 
# # df_timing_slices = df_timing_slices [ ~((df_timing_slices['refListId']==0) | (df_timing_slices['refListId_actual']==0)) ]

# df_timing_slices=df_timing_slices.drop(['refListId_actual','Q refListId_actual'],axis=1)


# In[ ]:





# In[14]:


runs_out=df_timing_slices .groupby('run')['refListId'].nunique().rename('Q refListId').reset_index(drop=False)
runs_out[runs_out['Q refListId']!=10]


# In[15]:


current_last_windows=timing_slices.drop_duplicates(['run','refListId','refListId_last'])
current_last_windows=current_last_windows[['run','refListId','refListId_last','ciuchStop']].reset_index(drop=True)
current_last_windows[:1]


# In[16]:


# runs 16 23 32 40 have missing boxes: discarded
# also run 1 is the start, no previous box: discarded
# run 18: box 0 run at the end
# 
timing=timing[~timing['run'].isin([1,18,16,23,32,40])]
timing_slices=timing_slices[~timing_slices['run'].isin([1,18,16,23,32,40])]
df_timing_slices=df_timing_slices[~df_timing_slices['run'].isin([1,18,16,23,32,40])]

df_timing_slices=df_timing_slices.sort_values(['LogTime','Epc'])
# 



# In[17]:




def analytical(tags , subslices):
# Groupement des données par 'Epc', 'refListId', 'slice_id' et 'loc', et obtention de la valeur maximale de 'Rssi'
    ana = tags.groupby(['Epc', 'refListId', 'slice_id', 'loc'])['Rssi'].max()            .unstack('loc',fill_value=-110).reset_index(drop=False)

# Création d'un DataFrame qui contient les ID de tranche uniques et leur ordre respectif
    order = pd.DataFrame(subslices['slice_id'].unique(),columns=['slice_id'])
    order['order']= order.index

# Jointure des données de 'ana' et 'order' sur la colonne 'slice_id', en conservant uniquement les colonnes nécessaires
    ana = pd.merge(ana , order, on='slice_id' , how='left')
    ana = ana [['Epc', 'refListId', 'slice_id', 'in', 'out', 'order']]

# Sélection de la dernière ID de tranche pour laquelle 'out' est supérieur à 'in', pour chaque combinaison de 'Epc' et 'refListId', triée par ordre décroissant
    ana_out = ana [ ana['out']>ana['in'] ].sort_values(['Epc', 'refListId', 'order'],ascending=False).drop_duplicates(['Epc', 'refListId'])

# Sélection de la première ID de tranche pour laquelle 'in' est supérieur à 'out', pour chaque combinaison de 'Epc' et 'refListId', triée par ordre croissant
    ana_in = ana [ ana['in']>ana['out'] ].sort_values(['Epc', 'refListId', 'order'],ascending=True).drop_duplicates(['Epc', 'refListId'])

# Jointure des données de 'ana_in' et 'ana_out' sur les colonnes 'Epc' et 'refListId', avec des suffixes '_IN' et '_OUT', en conservant toutes les colonnes
    ana = pd.merge(ana_in , ana_out , on=['Epc', 'refListId'], suffixes=['_IN', '_OUT'], how='inner')            .sort_values(['Epc', 'refListId'])

# Jointure des données de 'ana' et 'reflist' sur la colonne 'Epc', en conservant toutes les colonnes
    ana = pd.merge(ana , reflist , on ='Epc', how='left')

# Ajout d'une colonne booléenne qui indique si 'refListId' est égal à 'refListId_actual'
    ana['pred_ana_bool']= ana['refListId'] == ana['refListId_actual']

# Calcul de la fréquence de chaque valeur unique dans la colonne 'pred_ana_bool'
    value_counts = ana['pred_ana_bool'].value_counts()

# Calcul du pourcentage de la fréquence de la valeur "True"
    true_percentage = value_counts[True] / value_counts.sum() * 100

# Affichage du pourcentage de la fréquence de la valeur "True" avec deux décimales
    print('Pourcentage de la fréquence de True dans pred_ana_bool: {:.2f}%'.format(true_percentage))
    
    return true_percentage


# In[18]:


analytical(df_timing_slices, timing_slices )

