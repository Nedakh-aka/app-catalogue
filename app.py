import streamlit as st
import pandas as pd
import math
# from datetime import datetime

_FICHIER = "data/livres_poetry.csv"

st.set_page_config(page_title="Catalogue", page_icon="📚", layout="wide")

@st.cache_data
def charger_donnees(chemin):
    return pd.read_csv(chemin)


st.title("Catalogue de livres")
st.caption("Explorez notre catalogue de livres, filtrez selon vos préférences et découvrez les mieux notés.")

df = charger_donnees(_FICHIER)

with st.sidebar:
    st.header("Filtres")
    note_minimal = st.slider("Note minimale", 1, 5, 1)
    minimum = 0.0
    maximum = float(math.ceil(df["prix_gbp"].max()))
    print(maximum)
    prix_min, prix_max = st.slider("Fourchette de prix", minimum, maximum, (minimum, maximum))
    recherche = st.text_input("Le titre contient")
    categories = list(df["categorie"].unique())
    categories = st.multiselect("Categories", categories)

df_selection = df.copy()
if categories:
    df_selection = df_selection[df_selection["categorie"].isin(categories)]
if recherche:
    df_selection = df_selection[df_selection["titre"].str.contains(recherche, case=False, regex=False)]

df_selection = df_selection[df_selection["prix_gbp"] >= prix_min]
df_selection = df_selection[df_selection["prix_gbp"] <= prix_max]
df_selection = df_selection[df_selection["note"] >= note_minimal]

st.dataframe(df_selection)