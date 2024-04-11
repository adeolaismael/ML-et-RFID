#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime
import warnings
warnings.filterwarnings('ignore')


# 

# In[15]:



pathfile=r'data_anonymous'

# reflist: list of epc in each box
reflist=pd.DataFrame()
# On extrait tous les fichier dans le répertoir data_anonymous
files=os.listdir(pathfile)
for file in files:
    if file.startswith('reflist_'):
        # Ouvrir les fichier refList et les convertir en dataframe
        temp=pd.read_csv(os.path.join(pathfile,file),sep=',').reset_index(drop=True)[['Epc']]
        temp['refListId']=file.split('.')[0]
        reflist=reflist._append(temp)
reflist=reflist.rename(columns={'refListId':'refListId_actual'})
reflist['refListId_actual']=reflist['refListId_actual'].apply(lambda x:int(x[8:]))
# Q_reflistID infome du nombre d'epc dans chaque boite
Q_refListId_actual=reflist.groupby('refListId_actual')['Epc'].nunique().rename('Q refListId_actual').reset_index(drop=False)
reflist=pd.merge(reflist,Q_refListId_actual,on='refListId_actual',how='left')


# 

# In[16]:


# pathfile=r'data_anonymous'
# 
# df : rfid readings
df=pd.DataFrame()
# 
files=os.listdir(pathfile)
for file in files:
    if file.startswith('ano_APTags'):
        temp=pd.read_csv(os.path.join(pathfile,file),sep=',')
        df=df._append(temp)
df['LogTime']=pd.to_datetime (df['LogTime'] ,format='%Y-%m-%d-%H:%M:%S') 
df['TimeStamp']=df['TimeStamp'].astype(float)
df['Rssi']=df['Rssi'].astype(float)
df=df.drop(['Reader','EmitPower','Frequency'],axis=1).reset_index(drop=True)
df=df[['LogTime', 'Epc', 'Rssi', 'Ant']]
# antennas 1 and 2 are facing the box when photocell in/out 
# Il y a 4 antennes "Ant" car les 2 1er antennes out se font faces et les 2e antennes in se font aussi face.
# Ca à de l'influence si la tapis n'est pas une ligne droite or nous supposons qu'on a une ligne droite donc seul 2 antennes nous est nécessaire.
Ant_loc=pd.DataFrame({'Ant':[1,2,3,4],'loc':['in','in','out','out']})
df=pd.merge(df,Ant_loc,on=['Ant'])
df=df.sort_values('LogTime').reset_index(drop=True)


# In[17]:


df_reflist =pd.merge(df, reflist, on = 'Epc', how = 'left')
df_reflist = df_reflist[['Epc','LogTime','Rssi','loc','refListId_actual','Q refListId_actual']]


# In[18]:


# timing: photocells a time window for each box: start/stop (ciuchStart, ciuchStop)
# Converti un fichier CSV en dataframe et on prend seuelement les colonnes d'id de l'epc, le moment ou il passe le start et le stop
file=r'ano_supply-process.2019-11-07-CUT.csv'
timing=pd.read_csv(os.path.join(pathfile,file),sep=',')
timing['file']=file
timing['date']=pd.to_datetime(timing['date'],format='%d/%m/%Y %H:%M:%S,%f')
timing['ciuchStart']=pd.to_datetime(timing['ciuchStart'],format='%d/%m/%Y %H:%M:%S,%f')
timing['ciuchStop']=pd.to_datetime(timing['ciuchStop'],format='%d/%m/%Y %H:%M:%S,%f')
timing['timestampStart']=timing['timestampStart'].astype(float)
timing['timestampStop']=timing['timestampStop'].astype(float)
timing=timing.sort_values('date')
timing.loc[:,'refListId']=timing.loc[:,'refListId'].apply(lambda x:int(x[8:]))
timing=timing[['refListId', 'ciuchStart', 'ciuchStop']]


# In[19]:


# ciuchStart_up starts upstream ciuchStart, half way in between the previous stop and the actual start
# La boite est au milieu des détecteurs on défini le startup
timing[['ciuchStop_last']]=timing[['ciuchStop']].shift(1)
timing[['refListId_last']]=timing[['refListId']].shift(1)
timing['ciuchStartup']=timing['ciuchStart'] - (timing['ciuchStart'] - timing['ciuchStop_last'])/2
# timing start: 10sec before timing
timing.loc[0,'refListId_last']=timing.loc[0,'refListId']
timing.loc[0,'ciuchStartup']=timing.loc[0,'ciuchStart']-datetime.timedelta(seconds=10)
timing.loc[0,'ciuchStop_last']=timing.loc[0,'ciuchStartup']-datetime.timedelta(seconds=10)
timing['refListId_last']=timing['refListId_last'].astype(int)
# timing stop: 10sec après le timing
timing['ciuchStopdown']= timing['ciuchStartup'].shift(-1)
timing.loc[len(timing)-1,'ciuchStopdown']=timing.loc[len(timing)-1,'ciuchStop']+datetime.timedelta(seconds=10)
timing=timing[['refListId', 'refListId_last','ciuchStartup', 'ciuchStart','ciuchStop','ciuchStopdown']]


# In[20]:


# t0_run = a new run starts when box 0 shows up
t0_run=timing[timing['refListId']==0] [['ciuchStartup']]
t0_run=t0_run.rename(columns={'ciuchStartup':'t0_run'})
t0_run=t0_run.groupby('t0_run').size().cumsum().rename('run').reset_index(drop=False)
t0_run=t0_run.sort_values('t0_run')
# 
# each row in timing is merged with a last row in t0_run where t0_run (ciuchstart) <= timing (ciuchstart)
timing=pd.merge_asof(timing,t0_run,left_on='ciuchStartup',right_on='t0_run', direction='backward')
timing=timing.sort_values('ciuchStop')
# run correspond au nombre de passage de la boite, si les epc ne correspondent pas la boite repasse les détecteurs
timing=timing[['run', 'refListId', 'refListId_last', 'ciuchStartup','ciuchStart','ciuchStop','ciuchStopdown','t0_run']]


# In[21]:


#  full window (ciuchStartup > ciuchStopdown) is sliced in smaller slices
# ciuchStartup > ciuchStart: 11 slices named up_0, up_1, ..., up_10
# ciuchStart > ciuchStop: 11 slices named mid_0, mid_1, ... mid_10
# ciuchStop > ciuchStopdown: 11 slices names down_0, down_1, ... down_10
slices=pd.DataFrame()
for i, row in timing .iterrows():
    ciuchStartup=row['ciuchStartup']
    ciuchStart=row['ciuchStart']
    ciuchStop=row['ciuchStop']
    ciuchStopdown=row['ciuchStopdown']
    steps=4
#     
    up=pd.DataFrame(index=pd.date_range(start=ciuchStartup, end=ciuchStart,periods=steps))        .reset_index(drop=False).rename(columns={'index':'slice'})
    up.index=['up_'+str(x) for x in range(steps)]
    slices=slices._append(up)
#     
    mid=pd.DataFrame(index=pd.date_range(start=ciuchStart, end=ciuchStop,periods=steps))        .reset_index(drop=False).rename(columns={'index':'slice'})
    mid.index=['mid_'+str(x) for x in range(steps)]
    slices=slices._append(mid)
#     
    down=pd.DataFrame(index=pd.date_range(start=ciuchStop, end=ciuchStopdown,periods=steps,))        .reset_index(drop=False).rename(columns={'index':'slice'})
    down.index=['down_'+str(x) for x in range(steps)]
    slices=slices._append(down)
#     slices=slices.append(up)
slices=slices.reset_index(drop=False).rename(columns={'index':'slice_id'})
# 
timing_slices=pd.merge_asof(slices,timing,left_on='slice',right_on='ciuchStartup',direction='backward')
timing_slices=timing_slices[['run', 'refListId', 'refListId_last','slice_id','slice',                               'ciuchStartup', 'ciuchStart', 'ciuchStop', 'ciuchStopdown','t0_run']]


# In[22]:


# merge between df and timing
# merge_asof needs sorted df > df_ref
df=df[ (df['LogTime']>=timing['ciuchStartup'].min()) & (df['LogTime']<=timing['ciuchStopdown'].max())  ]
df=df.sort_values('LogTime')
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
df_timing_slices=df_timing_slices[['run', 'Epc','refListId', 'refListId_last', 'ciuchStartup','slice_id','slice','LogTime',                       'ciuchStart','ciuchStop', 'ciuchStopdown', 'Rssi', 'loc','t0_run','refListId_actual']]


# In[23]:


runs_out=df_timing_slices .groupby('run')['refListId'].nunique().rename('Q refListId').reset_index(drop=False)


# In[24]:


current_last_windows=timing_slices.drop_duplicates(['run','refListId','refListId_last'])
current_last_windows=current_last_windows[['run','refListId','refListId_last','ciuchStop']].reset_index(drop=True)


# In[25]:


# runs 16 23 32 40 have missing boxes: discarded
# also run 1 is the start, no previous box: discarded
# run 18: box 0 run at the end
# 
timing=timing[~timing['run'].isin([1,18,16,23,32,40])]
timing_slices=timing_slices[~timing_slices['run'].isin([1,18,16,23,32,40])]
df_timing_slices=df_timing_slices[~df_timing_slices['run'].isin([1,18,16,23,32,40])]

df_timing_slices=df_timing_slices.sort_values(['LogTime','Epc'])
# 


# In[26]:


# df_timing_slices['dt']=
df_timing_slices['dt']=(df_timing_slices['LogTime']-df_timing_slices['t0_run']).apply(lambda x:x.total_seconds())


# In[27]:


# 
# df_timing_threshold
# 


# In[28]:


rssi_threshold=-110
df_timing_slices_threshold=df_timing_slices[df_timing_slices['Rssi']>rssi_threshold]


# In[29]:


# readrate
# readrate
round(100*df_timing_slices_threshold.reset_index(drop=False).groupby(['run','loc'])['Epc'].nunique().groupby('loc').mean()    /reflist['Epc'].nunique(),2)


# # Script analytic

# In[30]:


# Pour le script analytique on doit associé le bon tag à la bonne boite
# La fonction prend comme arguments 2 dataframes 'tags' et 'subslices'
def analytical(tags, subslices):
    
# La fonction calcule la valeur maximale de Rssi pour chaque combinaison d''Epc', 'refListId', 'subslice_id' et 'loc' à partir du DataFrame tags. Les valeurs sont stockées dans un DataFrame nommé ana.
    ana = tags.groupby(['Epc','refListId','slice_id','loc'])['Rssi'].max()            .unstack('loc', fill_value=-110).reset_index(drop = False)
    
# La fonction crée un DataFrame nommé order contenant les valeurs uniques de 'subslice_id' et leur ordre d'apparition 'order'.  
    order = pd.DataFrame(subslices['slice_id'].unique(), columns = ['slice_id'])
    order['order'] = order.index
    
# La fonction fusionne le DataFrame ana avec le DataFrame order sur la colonne 'subslice_id' pour obtenir une colonne order dans ana.
    ana = pd.merge(ana, order, on = 'slice_id', how = 'left')
# La fonction fusionne le DataFrame ana avec le DataFrame order sur la colonne subslice_id pour obtenir une colonne order dans ana.
    ana = ana [['Epc','refListId','slice_id','in','out','order']]
    
# La fonction extrait le dernier 'subslice_id' avec une valeur de 'out' supérieure à 'in', et le premier 'subslice_id' avec une valeur de 'in' supérieure à 'out' à partir de ana. 
# Ces deux ensembles de données sont stockés dans les DataFrames 'ana_out' et 'ana_in'.
    
# Last subslice_id with out>in (pas encore à l'intérieur)
    ana_out = ana[ana['out']>ana['in']].sort_values(['Epc','refListId','order'], ascending = False).drop_duplicates(['Epc','refListId'])

# First subslice_id with in>out (à dépasser l'intérieur)
    ana_in = ana[ana['in']>ana['out']].sort_values(['Epc','refListId','order'], ascending = True).drop_duplicates(['Epc','refListId'])

# La fonction fusionne les DataFrames ana_in et ana_out sur les colonnes Epc et refListId en utilisant une jointure interne (inner join). Le résultat est stocké dans le DataFrame ana.
# Rajoute un _in en suffix pour les élements fusionnés venant de anna_in et réciproquement avec _out
    ana = pd.merge(ana_in, ana_out, on=['Epc', 'refListId'], suffixes=['_IN', '_OUT'], how = 'inner')             .sort_values(['Epc'])
# La fonction fusionne le DataFrame ana avec un autre DataFrame nommé reflist sur la colonne Epc en utilisant une jointure gauche (left join). Le résultat est stocké dans le DataFrame ana.
    ana = pd.merge(ana, reflist, on = 'Epc', how = 'left')

# La fonction ajoute une colonne 'pred_ana_bool' à ana qui contient la valeur booléenne True si la partie initiale de la chaîne 'refListId' (avant le premier caractère "_") est égale à la valeur de la colonne box de ana.
    ana['pred_ana_bool'] = ana['refListId'] == ana['refListId_actual']

#  Nombre de ligne pour la colonne 'pred_ana_bool' dans le df ana
    value_counts = ana['pred_ana_bool'].value_counts()
    
# On calcul le poucentage de true dans 'pred_ana_bool' donc le nombre de prédiction vrai
    true_percentage = value_counts[True] / value_counts.sum()*100

# La fonction retourne le poucentage de prédiction vraie
    return true_percentage

# # Script analytic

# In[31]:

def result():
    return analytical(df_timing_slices, timing_slices)


# In[32]:


subslices_test = df_timing_slices.loc[:,['refListId','run','ciuchStartup','slice_id']]
subslices_test['run'] = subslices_test['run'].astype(str)
subslices_test['refListId'] = subslices_test['refListId'].astype(str)
subslices_test['window_run_id'] = subslices_test[['refListId','run']].apply('_'.join, axis=1)
subslices_test = subslices_test.drop(['refListId'], axis=1)
subslices_test['window_run_id'] = subslices_test['window_run_id'].apply(lambda x: 'box' + x)
subslices_test = subslices_test.rename(columns={'run': 'runs', 'ciuchStartup': 'subsliceStart'})


# In[33]:


tags_test = df_timing_slices.loc[:,['Epc', 'LogTime','Rssi','loc','refListId']]


# In[34]:


# analytical(df_timing_slices, timing_slices)


# # Machine learning

# In[35]:


# sample: one tag in one window

def dataset(tags, windows, rssi_quantile):
    ds_rssi = tags.groupby(['Epc', 'refListId','refListId_actual', 'slice_id', 'loc'])['Rssi'].quantile(rssi_quantile)            .unstack(['slice_id','loc'], fill_value=-110)
    ds_rssi.columns = [x[0]+'_'+x[1] for x in ds_rssi.columns]
    ds_rssi = ds_rssi.reset_index(drop=False)
#
    ds_rc = tags.groupby(['Epc', 'refListId','refListId_actual', 'slice_id', 'loc']).size().unstack(['slice_id', 'loc'], fill_value=0)
    ds_rc.columns = [x[0]+'_'+x[1] for x in ds_rc.columns]
    ds_rc = ds_rc.reset_index(drop=False)
#
    ds= pd.merge(ds_rssi, ds_rc, on =['Epc', 'refListId', 'refListId_actual'], suffixes=['_rssi', '_rc'])  
# window_width
    ds = pd.merge(ds, windows[['refListId', 'timing_width']], on = 'refListId', how='left')
# Epcs_window
    Q_Epcs_window = tags.groupby(['refListId'])['Epc'].nunique().rename('Epcs_window').reset_index(drop=False)
    ds = pd.merge(ds, Q_Epcs_window, on='refListId', how='left')
# reads_window
    Q_reads_window = tags.groupby(['refListId']).size().rename('reads_window').reset_index(drop=False)
    ds = pd.merge(ds, Q_reads_window, on='refListId', how='left')
    return ds


# Fonction "dataset" qui renvoie un nouveau DataFrame avec des colonnes qui sont une combinaison des noms de colonnes originaux et des valeurs de slice_id et loc ainsi que la fusion du dataframe "windows" sur Epc et refListId. 

# In[36]:


# Rajout de la colonne timing_width qui est le temps que mets la boite pour passer une fenêtre
timing_slices['timing_width'] = (timing_slices['ciuchStopdown']-timing_slices['ciuchStartup']).apply(lambda x:x.total_seconds())


# In[37]:


ds = dataset(df_timing_slices,timing_slices,1)


# In[38]:


# y est la colonne refListId_actual
y = ds['refListId_actual']
X =ds.drop('refListId_actual', axis=1)


# In[39]:


# retravailler le dataset pour avoir le bon format
X['Epc'] = X['Epc'].str.replace('epc_', '')
X['Epc'] = X['Epc'].astype(int)


# GridSearchCV sert à calculer les meilleurs hyperparamètres parmis une liste

# In[40]:


# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import GridSearchCV
# from sklearn.datasets import make_classification

# # les données de test sont X et y

# # Définir les hyperparamètres à ajuster
# param_grid = { 'n_estimators': [50, 100, 200], 'max_depth': [5, 10, 15]}

# # Créer un objet de modèle
# rf = RandomForestClassifier(random_state=42)

# # Créer un objet GridSearchCV great_search = gs
# gs = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, scoring='accuracy', n_jobs=-1)

# # Exécuter la recherche sur grille
# gs.fit(X, y)

# # Afficher les meilleurs hyperparamètres et la meilleure performance de validation croisée
# print("Meilleurs hyperparamètres: ", gs.best_params_)
# print("Meilleure performance de validation croisée: ", gs.best_score_)


# Avoir un dataframe pred_ml avec les résultats de test du randomForest

# In[41]:


# # retester avec le dataframe ds, objectif : identifier les Epcs erreurs

# # classifier parameters extracted from gs
# from sklearn.datasets import make_classification
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import MinMaxScaler

# clf = RandomForestClassifier(n_estimators = gs.best_params_['n_estimators'], max_depth = gs.best_params_['max_depth'],)
# #clf = RandomForestClassifier(n_estimators =100, max_depth = 10,)

# # pred_ml stores prediction results: [Epc, window_run_id actual, pred_ml]
# pred_ml = pd.DataFrame()
# retries = 3
# for retry in range(retries):
#     Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, train_size=0.8, stratify = y)
    
#     scaler = MinMaxScaler()
#     scaler.fit(Xtrain)
#     Xtrain_std = scaler.transform(Xtrain)
#     Xtest_std = scaler.transform(Xtest)
    
#     clf.fit(Xtrain_std, ytrain)
    
#     ypred = clf.predict(Xtest_std)
    
#     print(retry, (ytest==ypred).mean())
#     ypred_series = pd.Series(ypred, index = ytest.index, name = 'pred_ml')
#     # 'actual' valeur réel de la cible
#     temp = ds.loc[ytest.index, ['Epc', 'refListId', 'refListId_actual']]
#     temp = temp.join(ypred_series)
#     temp.loc[:, 'retry'] = retry
#     pred_ml = pred_ml.append(temp)

# # les résultats des tests sont stockés dans un dataFrame pred_ml
# pred_ml.loc[:, 'pred_ml_bool'] = (pred_ml.loc[:, 'refListId_actual']==pred_ml.loc[:, 'pred_ml'])
# pred_ml = pred_ml [['Epc', 'refListId', 'refListId_actual', 'pred_ml', 'pred_ml_bool', 'retry']]


# In[42]:


from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score

# n_estimators est le nombre d'arbres de décision dans la forêt aléatoire. Controle la complexité et sa performance. 
# Plus on augmente plus temps de calcul long et risque de surapprentissage.

# max_depth c'est la profondeur maximale de chaque arbre de décision dans la forêt. 
# Il contrôle la complexité de chaque arbre individuel dans la forêt.
# max_depth plus grand capture plus de relations complexes entre les variables d'entrée, 
# mais augmente le risque de surapprentissage et réduit la capacité de généralisation.

def RandomForestML(nb_arbre, max_profondeur):
    #  classificateur randomForest
    clf = RandomForestClassifier(n_estimators = nb_arbre, max_depth = max_profondeur)

    # entrainement des données
    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, train_size=0.8, random_state=42)
    
    # mise à l'échelle
    scaler = MinMaxScaler()
    scaler.fit(Xtrain)
    Xtrain_std = scaler.transform(Xtrain)
    Xtest_std = scaler.transform(Xtest)

    clf.fit(Xtrain_std, ytrain)
    
    # prédiction de la boite
    ypred = clf.predict(Xtest_std)
    # renvoie la moyenne de réussite d'identification des boites
    # return (ytest==ypred).mean()
    return accuracy_score(ytest, ypred)





# In[43]:

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

def logistic_regression(régularisation, C, algo_résolution):

    # Diviser les données en ensemble d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normaliser les données
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Créer un objet LogisticRegression avec les hyperparamètres
    logreg = LogisticRegression(penalty= régularisation, C= C, solver= algo_résolution)

    # Entraîner le modèle sur les données d'entraînement
    logreg.fit(X_train, y_train)

    # Faire des prédictions sur les données de test
    y_pred = logreg.predict(X_test)

    # Évaluer la précision du modèle
    accuracy = logreg.score(X_test, y_test)

    return accuracy




#In[44]:

from sklearn.svm import SVC

def train_svc_model(kernel, C_marge_er, flexibilite, degree_pol, coeficient, tolerance):

    # Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 100000 - 4mins
    X_train = X_train[:10000]
    y_train = y_train[:10000]
    
    # Créer un objet StandardScaler
    scaler = StandardScaler()

    # Normaliser les données d'entraînement
    X_train = scaler.fit_transform(X_train)

    # Normaliser les données de test en utilisant les paramètres de normalisation appris sur les données d'entraînement
    X_test = scaler.transform(X_test)

    # Créer un modèle SVC avec les hyperparamètres définis
    svc = SVC(kernel='rbf', C= C_marge_er, gamma= flexibilite, degree = degree_pol, coef0= coeficient, tol = tolerance)

    # Entraîner le modèle avec les données d'entraînement
    svc.fit(X_train, y_train)

    # Faire des prédictions sur l'ensemble de test
    y_pred = svc.predict(X_test)

    # Évaluer la précision du modèle sur l'ensemble de test
    accuracy = svc.score(X_test, y_test)
    return accuracy




#In[45]:

from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris

def knn_classifier(k, metrique, poids, algorithme):
    
    # Division des données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Normalisation des données et les mettre à l'échelle
    scaler = MinMaxScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    # Création d'une instance du classificateur KNN avec les hyperparamètres spécifiés
    knn = KNeighborsClassifier(n_neighbors=k, metric= metrique, weights= poids, algorithm=algorithme)

    # Entraînement du modèle
    knn.fit(X_train, y_train)

    # Prédictions sur les données de test
    y_pred = knn.predict(X_test)

    # Évaluation des performances
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy









