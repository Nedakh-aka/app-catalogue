import math

import pandas as pd
import streamlit as st


_FICHIER = "data/livres_poetry.csv"


@st.cache_data
def _charger_donnees(chemin):
    """
    Charge un fichier CSV dans un DataFrame Pandas.

    Args:
        chemin (str): Chemin du fichier CSV à charger.

    Returns:
        pd.DataFrame: Données contenues dans le fichier CSV.
    """

    return pd.read_csv(chemin)


def _afficher_filtres(df):
    """
    Affiche les filtres de recherche dans la barre latérale.

    Args:
        df (pd.DataFrame): Catalogue complet des livres.

    Returns:
        tuple: Valeurs sélectionnées pour les filtres :
            - note_min (int): Note minimale.
            - prix_min (float): Prix minimum.
            - prix_max (float): Prix maximum.
            - recherche (str): Texte recherché dans les titres.
            - categories_selectionnees (list): Catégories sélectionnées.
    """

    with st.sidebar:
        st.header("Filtres")
        note_min = st.slider("Note minimale", 1, 5, 1)
        minimum = 0.0
        maximum = 50.0 if df.empty else float(math.ceil(df["prix_gbp"].max()))
        prix_min, prix_max = st.slider(
            "Fourchette de prix",
            minimum,
            maximum,
            (minimum, maximum)
        )
        recherche = st.text_input("Le titre contient")
        categories_disponibles = list(df["categorie"].unique())
        categories_selectionnees = st.multiselect(
            "Catégories",
            categories_disponibles
        )

    return note_min, prix_min, prix_max, recherche, categories_selectionnees


def _filtrer_donnees(df, note_min, prix_min, prix_max, recherche, categories):
    """
    Filtre le catalogue de livres selon les critères sélectionnés.

    Args:
        df (pd.DataFrame): Catalogue complet des livres.
        note_min (int): Note minimale acceptée.
        prix_min (float): Prix minimum accepté.
        prix_max (float): Prix maximum accepté.
        recherche (str): Texte recherché dans les titres.
        categories (list): Catégories sélectionnées.
            Si la liste est vide, toutes les catégories sont conservées.

    Returns:
        pd.DataFrame: Catalogue filtré selon les critères.
    """

    df_filtre = df.copy()
    if categories:
        df_filtre = df_filtre[df_filtre["categorie"].isin(categories)]
    if recherche:
        df_filtre = df_filtre[df_filtre["titre"].str.contains(
            recherche,
            case=False,
            regex=False,
            na=False
        )]

    df_filtre = df_filtre[df_filtre["prix_gbp"] >= prix_min]
    df_filtre = df_filtre[df_filtre["prix_gbp"] <= prix_max]
    df_filtre = df_filtre[df_filtre["note"] >= note_min]

    return df_filtre


def _afficher_indicateurs(df, df_filtre):
    """
    Affiche les indicateurs statistiques du catalogue filtré.

    Args:
        df (pd.DataFrame): Catalogue complet des livres.
        df_filtre (pd.DataFrame): Catalogue filtré.
    """

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Livres retenus", f"{df_filtre.shape[0]} / {df.shape[0]}")
    col2.metric("Prix moyen", f"{df_filtre["prix_gbp"].mean():.2f} £")
    col3.metric("Note moyenne", f"{df_filtre["note"].mean():.2f} / 5")
    col4.metric("Exemplaires en stock", df_filtre["stock"].sum())


def _afficher_palmares(df):
    """
    Affiche les palmarès des livres selon leur note et leur prix.

    Args:
        df (pd.DataFrame): Catalogue filtré des livres.
    """

    gauche, droite = st.columns(2)

    with gauche:
        df_mieux_note = df.nlargest(5, "note")[["titre", "note"]]
        st.subheader(f"Les {df_mieux_note.shape[0]} mieux notés")
        st.dataframe(df_mieux_note)

    with droite:
        df_moins_cher = df.nsmallest(5, "prix_gbp")[["titre", "prix_gbp"]]
        st.subheader(f"Les {df_moins_cher.shape[0]} moins chers")
        st.dataframe(df_moins_cher)


def main():
    """
    Orchestre le chargement, le filtrage et l'affichage du catalogue.
    """

    st.set_page_config(page_title="Catalogue", page_icon="📚", layout="wide")
    st.title("Catalogue de livres")
    st.caption(
        "Explorez notre catalogue de livres, filtrez selon vos préférences "
        "et découvrez les mieux notés."
    )

    df_brute = _charger_donnees(_FICHIER)
    selection = _afficher_filtres(df_brute)
    df_selection = _filtrer_donnees(df_brute, *selection)

    if df_selection.shape[0] == 0:
        st.warning("Aucun livre ne correspond à ces critères.")
    else:
        _afficher_indicateurs(df_brute, df_selection)
        st.dataframe(df_selection)
        _afficher_palmares(df_selection)

    with st.expander("Voir les données complètes"):
        st.dataframe(df_brute)


if __name__ == "__main__":
    main()