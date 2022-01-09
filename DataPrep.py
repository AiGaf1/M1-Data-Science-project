import pandas 
from sklearn.decomposition import KernelPCA

def readData(dataCSV):
    df = pandas.read_csv(dataCSV, encoding='ISO-8859-1')
    df = df.drop(['X'], axis=1) #removed column of indexes 
    df = df.rename(columns={'bpm':'beats per minute',
                        'top.genre':'genre','nrgy':'energy','dnce':'danceability', 'dB':'loudness dB',
                        'spch':'speechiness','live':'liveness','val':'valence','dur':'duration','acous':'acousticness',
                        'pop':'popularity', 'emo' : 'bad feeling', 'ins': 'instrumentalness'})
    return df

def removeRedundant(dataframe, list):
    for e in list:
        dataframe.pop(e)
        

def dropOutlier(dataframe, index):
    dataframe.drop([index])

def fixNanWithMedian(dataframe):
    for i in range(3, 14): # Nan values are changed to a mean value that depends from genre name #until 'pop' columns 
        df_nan = dataframe[dataframe.iloc[:, i].isna()]
        df_nan = df_nan.loc[:, ['genre']]
        
        for j in range(len(df_nan)):
            artist_genre = df_nan.iloc[j].values
            df_artist_genre = dataframe[dataframe.loc[:, ['genre']].isin(artist_genre).all(axis=1)]
            meadian = df_artist_genre.iloc[:, i].dropna().median() # Why is here not mean? Beacuase I have outliers in the dataset and also distribution is not simmetrical   
            index = df_artist_genre[df_artist_genre.iloc[:, i].isna()].index
            dataframe.iloc[index, i] = meadian #

def fillMissingValue(dataframe, index , feature , filler):
    dataframe.iloc[index, feature] = filler 

def normalize(dataframe):
    df_norm = dataframe.copy()
    def min_max_scaling(series):
        return ((series - series.min())/(series.max()-series.min()))
    columns = dataframe.columns[4:]
    columns = df_norm.groupby("year")[columns].median().loc[2010].sort_values(ascending = False).index # sort columns by meadian value of 2010 year
    for col in columns:
        df_norm[col] = min_max_scaling(dataframe[col].values) 
    return df_norm

def doAllMedianNaanFix(dataCSV):
    df = readData(dataCSV)
    removeRedundant(df, ["instrumentalness", "bad feeling"])
    dropOutlier(df, 442)
    fixNanWithMedian(df)
    fillMissingValue(df, index = 273, feature = 4, filler = 129) 
    return normalize(df)

def kpca_reduction(dataframe):
    kpca = KernelPCA(n_components=2)
    return kpca.fit_transform(dataframe)

def get_top_df(df, top = 10): #change 'top' value to see another top 

    top_lst = df.iloc[:]['genre'].value_counts().index[top:]
    df_other = df.replace(top_lst, 'Other')
    order_lst = list(df_other['genre'].value_counts().index)
    order_lst.remove('Other') #remove first 'Other'
    order_lst.append('Other') #append to the end 'Other'

    return df_other, order_lst