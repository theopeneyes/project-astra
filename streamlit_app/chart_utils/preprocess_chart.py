from typing import List 
from gensim.models import Word2Vec
from sklearn.decomposition import PCA 

import numpy as np 
import pandas as pd 

items: List[str] = ["Canadian Football","Green Infrastructure","Energy Efficiency","Extraction","Basketball Teams","Association Football","Waste Management","Defensive Strategy","Refining","Baseball","Gaelic Football","Associated minerals","Rugby Union","Rugby","Carburetors","Fuel Mixture","Fuel Injection","Rugby League","Geology","Professional Football Associations","Crystal Formation","Soccer Teams","Air-Fuel Mixture Control","Indoor Activities","Engine Performance","Baseball Teams","Crystallography","Extraction methods","American Football","Public Transportation","Galena discovery","Housing Affordability","Football","Outdoor Activities","Sulfide minerals","Silver extraction","Mineralogy","Fuel Injection Systems","Individual Sports","Engine Types","Australian Rules Football","Fuel Systems","Hockey","Sedimentary deposits","Soccer","Offensive Strategy","Lead-zinc deposits","Basketball","Carrying codes","Medieval Football","Kicking codes","Hydrothermal deposits","Engine Components","Team Sports","Historical mining sites","Competition","Chemical Engineering","Health and Fitness","Strategic Planning","Physical Education","Economics","Metallurgy","Cultural Studies","Urban Planning","Geology","Sports History","Sports","Environmental Science","Team Dynamics","Ball Sports","Globalization","Automotive Engineering","Mineralogy","Recreation","Sports Management","Military Tactics","Mining","Engine Technology","Sports Analytics","Team Sports","Organizational Structure","Ore Deposits","Minerals","Canadian Football","Green Infrastructure","Energy Efficiency","Extraction","Basketball Teams","Association Football","Waste Management","Defensive Strategy","Refining","Baseball","Gaelic Football","Associated minerals","Rugby Union","Rugby","Carburetors","Fuel Mixture","Fuel Injection"]

def visualizer(items: List[str]) -> pd.DataFrame: 
    # this function converts a list of topics to semantic vectors 
    items = [item for item in items if isinstance(item, str)]
    tokenized_list = [item.split() for item in items]
    model = Word2Vec(sentences=tokenized_list, vector_size=100, window=5, min_count=1, workers=4)

    word_vectors = []
    for word in items: 
        sentence_vector = np.zeros((100,)) 
        for token in word.split(" "): 
            sentence_vector += model.wv[token] 
        word_vectors.append(sentence_vector)

    # returns a dataframe to plot as a scatter plot 
    pca = PCA(n_components=2)

    #vectors 
    vectors = np.vstack(word_vectors)
    
    embeds = pca.fit_transform(vectors) 
    df: pd.DataFrame = pd.DataFrame(embeds, columns=["x", "y"])
    df["labels"] = items 
    return df  





        