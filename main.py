import streamlit as st
from prediction import make_prediction


st.sidebar.subheader('Predict')
explore_predict = st.sidebar.selectbox('Choose page to view', ['Predict'])


if explore_predict == 'Predict':
    make_prediction()
