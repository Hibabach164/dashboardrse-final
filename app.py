
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titre de l'application
st.set_page_config(page_title="Dashboard RSE", layout="wide")
st.title("Tableau de bord - Score RSE des entreprises")

# Lecture des données avec encodage UTF-8 explicite
try:# Lecture des données avec gestion de l'encodage et du séparateur
try:
    df = pd.read_csv("donnees_rse_1.csv", encoding="utf-8", sep=';')
except UnicodeDecodeError:
    df = pd.read_csv("donnees_rse_1.csv", encoding="ISO-8859-1", sep=';')


# Nettoyage de colonnes avec des NaN potentiels
df.dropna(subset=["Entreprise", "Pilier", "Score"], inplace=True)

# Filtres
entreprises = st.sidebar.multiselect("Choisir une ou plusieurs entreprises :", df["Entreprise"].unique(), default=df["Entreprise"].unique())
piliers = st.sidebar.multiselect("Choisir un ou plusieurs piliers RSE :", df["Pilier"].unique(), default=df["Pilier"].unique())
seuil = st.sidebar.slider("Seuil de performance RSE :", min_value=0, max_value=100, value=70)

df_filtered = df[(df["Entreprise"].isin(entreprises)) & (df["Pilier"].isin(piliers))]

# KPI
moyenne_score = round(df_filtered["Score"].mean(), 2)
st.metric("Score RSE moyen", moyenne_score)

# Histogramme
st.subheader("Répartition des scores RSE par entreprise")
fig, ax = plt.subplots()
df_filtered.groupby("Entreprise")["Score"].mean().sort_values().plot(kind="barh", ax=ax)
ax.axvline(seuil, color="red", linestyle="--", label="Seuil de performance")
ax.set_xlabel("Score moyen")
ax.set_ylabel("Entreprise")
ax.set_title("Score RSE moyen par entreprise")
ax.legend()
st.pyplot(fig)

# Jauge et tableau
st.subheader("Données détaillées")
st.dataframe(df_filtered.reset_index(drop=True))
