import pandas as pd
import pickle as pkl
from matplotlib import pyplot as plt
from random import randint
import streamlit as st
import networkx as nx
from pyprocessmacro import Process

df = pd.read_feather('data')
feature_cats = {'internal': ['internal-count',
  'internal-negative-count',
  'internal-negative-percent'],
 'media': ['media-count', 'media-negative-count', 'media-negative-percent'],
 'toxic': ['comment-toxicity-percent',
  'post-toxicity-percent',
  'comment-toxicity-score',
  'post-toxicity-score',
  'comment-popular-toxicity-percent'],
 'popularity': ['popularity']}

def mediation(df, x, m, y):
    p = Process(data=df, model=4, x=x, y=y, m=[m], suppr_init=True)

    y_score = p.outcome_models[y].coeff_summary()[['coeff', 'p']].round(3)
    m_score = p.outcome_models[m].coeff_summary()[['coeff', 'p']].round(3)

    y_score = y_score.to_dict('index')
    m_score = m_score.to_dict('index')

    scores = dict()
    scores['x-m'] = m_score[x]
    scores['m-y'] = y_score[m]
    scores["x-y"] = y_score[x]

    G = nx.Graph()
    G.add_node(x,pos=(10,10), name=x)
    G.add_node(m,pos=(20, 13), name=y)
    G.add_node(y,pos=(30,10), name=m)

    G.add_edge(x, y, weight=4, )
    G.add_edge(x, m, weight=2)
    G.add_edge(m, y, weight=2)
    pos=nx.get_node_attributes(G,'pos')


    plt.figure(figsize=(18, 8))    
    plt.margins(x=0.2, y=0.2)
    labels={node:node for node in G.nodes()}
    nx.draw(G,pos,edge_color='lightgrey',width=1,linewidths=1, node_size=1300,node_color='pink', labels=labels, node_shape='s', font_size=21)
    nx.draw_networkx_edge_labels(G,pos,edge_labels={(x, y):scores['x-y'], (x, m):scores['x-m'],(m, y):scores['m-y']},font_color='red', font_size=21)

    plt.axis('off')
    return plt


features = []
for f in feature_cats:
    features += feature_cats[f]


st.write('# Select X')
X = st.selectbox('', features, 7)
st.write('# Select M')
M = st.selectbox(' ', features, 2)
st.write('# Select Y')
Y = st.selectbox('  ', features, 5)

plt = mediation(df, X, M, Y)
st.pyplot(plt)