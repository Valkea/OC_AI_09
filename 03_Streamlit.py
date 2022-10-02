import streamlit as st
import requests
import pandas as pd
import pathlib

# IMPORT Azure Function Key
try:
    with open("secrets.txt") as f:
        FUNCTION_KEY = f.readline().strip()
    azure_function_url = f"https://globo-reco.azurewebsites.net/api/HttpTrigger?code={FUNCTION_KEY}"
except FileNotFoundError:
    azure_function_url = "http://localhost:5000/api/HttpTrigger?"


data_train = pd.read_csv(pathlib.Path('data', 'data_train.csv'))


def main():
    st.set_page_config(page_title="Recommender System demo", page_icon="🤖")
    st.title("Get user's recommendations")

    # --- Load user's data
    users = pd.DataFrame(data_train.user_id.unique(), columns=['user_id'])[-100:]
    users.reset_index(inplace=True)
    # st.dataframe(users)

    # --- Initialize an number input to select the reco_size
    reco_size = st.number_input("Number of recommendations requested", value=5, min_value=1, max_value=20, key="reco_size")

    # --- Table header
    cols = st.columns((1, 1, 2, 4))
    fields = ["№", 'user_id', 'action', 'recommended article_id(s)']

    for col, field_name in zip(cols, fields):
        col.write(field_name)

    # --- Table rows
    for x, user in users.iterrows():

        col1, col2, col3, col4 = st.columns((1, 1, 2, 4))
        col1.write(x)  # index
        col2.write(user['user_id'])
        col4.empty()

        button_phold = col3.empty()  # create a placeholder
        do_action = button_phold.button("Recommend", key=x)

        if do_action:
            r = requests.get(f"{azure_function_url}&user_id={user['user_id']}&reco_size={reco_size}")
            col4.write(r.text)


if __name__ == '__main__':
    main()
