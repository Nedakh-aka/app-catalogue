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

col1, col2, col3, col4 = st.columns(4)

col1.metric("Livres retenus", f"{df_selection.shape[0]} / {df.shape[0]}")
col2.metric("Prix moyen", f"{df_selection["prix_gbp"].mean():.2f} £")
col3.metric("Note moyenne", f"{df_selection["note"].mean():.2f} / 5")
col4.metric("Exemplaires en stock", df_selection["stock"].sum())

st.dataframe(df_selection)

gauche, droite = st.columns(2)

with gauche:
    df_mieux_note = df_selection.nlargest(5, "note")[["titre", "note"]]
    st.subheader(f"Les {df_mieux_note.shape[0]} mieux notés")
    st.dataframe(df_mieux_note)

with droite:
    df_moins_cher = df_selection.nsmallest(5, "prix_gbp")[["titre", "prix_gbp"]]
    st.subheader(f"Les {df_moins_cher.shape[0]} moins cher")
    st.dataframe(df_moins_cher)