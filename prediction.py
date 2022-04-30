import streamlit as st
import pickle
import numpy as np
import time

yes_no = ["Yes", "No"]

gender_ls = ["Male", "Female", "Other"]

age_ls = ["Above", "Below"]

test_ls = ["Yes", "No", "Maybe"]


# load model
with open("random_forest_model.sav", "rb") as file:
    data = pickle.load(file)


# assign our XGB mode
model = data['model']


# function to return 1 or 0 based on yes or no answer
def yes_no_converter(answer):
    if answer == "Yes":
        return 1
    else:
        return 0


def make_prediction():
    st.title("COVID-19 PREDICTION")
    st.write("This is an online Covid-19 prediction web app. Prediction is made based on your response to the symptoms you seem to be experiencing. This web app was set up to complement a mid semester project in machine learning.")
    st.write("All you need to do is answer a few questions and get a feedback on your covid status i.e., whether you have it or not.")
    st.write("Let us begin shall we?")

    # user responses
    name = st.text_input(
        "Would you mind telling us your name?", value="Anonymous")

    st.subheader("Cough")
    cough = st.selectbox(
        "Do you happen to cough a lot or intensively?", yes_no)

    st.subheader("Fever")
    fever = st.radio(
        "Do you feel you have a fever or feel feverish?", yes_no)

    st.subheader("Sore Throat")
    sore_throat = st.radio("Are you experiencing a sore throat?", yes_no)

    st.subheader("Shortness of Breath")
    breath = st.selectbox(
        "Do you feel your breathing is short and rapid?", yes_no)

    st.subheader("Headache")
    headache = st.selectbox(
        "Are you experiencing a headache, be it mild or intense?", yes_no)

    st.subheader("Gender")
    gender = st.selectbox("Can you please identify your gender", gender_ls)

    st.subheader("Age")
    age = st.selectbox("Specify if you are above or below age 60", age_ls)

    st.subheader("Contact")
    contact = st.selectbox(
        "Do you remember being in contact with anyone showing any or most of the symptoms above?", test_ls)

    # prediction button
    predict = st.button("Predict", help="CLick here to get prediction")

    _cough = yes_no_converter(cough)
    _fever = yes_no_converter(fever)
    _sore_throat = yes_no_converter(sore_throat)
    _breath = yes_no_converter(breath)
    _headache = yes_no_converter(headache)

    # for gender
    if gender == "Male":
        _gender_male = 1
        _gender_female = 0
        _gender_other = 0
    elif gender == "Female":
        _gender_male = 0
        _gender_female = 1
        _gender_other = 0
    elif gender == "Other":
        _gender_male = 0
        _gender_female = 0
        _gender_other = 1

    # for age
    if age == "Above":
        _age_60_yes = 1
        _age_60_no = 0
    elif age == "Below":
        _age_60_yes = 0
        _age_60_no = 1

    # for contact
    if contact == "Yes":
        _test_abroad = 0
        _test_confirmed = 1
        _test_other = 0
    elif contact == "No":
        _test_abroad = 1
        _test_confirmed = 0
        _test_other = 0
    elif contact == "Maybe":
        _test_abroad = 0
        _test_confirmed = 0
        _test_other = 1

    # if prediction button is presses
    if predict:
        # convert the response to numpy array
        x = np.array([[_cough, _fever, _sore_throat, _breath, _headache, _gender_female, _gender_male,
                     _gender_other, _age_60_no, _age_60_yes, _test_abroad, _test_confirmed, _test_other]])

        x = x.astype(int)

        prediction = model.predict(x)

        with st.spinner('Wait for it...'):
            time.sleep(5)
            if prediction == 1:
                st.subheader("Hello " + name + ",")
                st.subheader("The system has confirmed your symptoms are that of Covid-19. Please find the closest health center to you and seek immediate treatment. While you're at it please try your best to avoid contact with other people. \nThank you 👍")
            elif prediction == 0:
                st.subheader("Hello " + name + ",")
                st.subheader(
                    "Your symptoms do not appear to be that of Covid-19 but you should still consider seeking medical treatment since your symptoms are that of another disease.")
