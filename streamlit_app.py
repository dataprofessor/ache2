import streamlit as st
import pandas as pd
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, matthews_corrcoef
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
from PIL import Image

st.markdown('# 💊 AChEpred')
st.info('Prediction of Acetylcholinesterase inhibitors and non-inhibitors')
st.markdown('- [**Link to Paper**](https://peerj.com/articles/2322/)')
