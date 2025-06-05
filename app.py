
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Chargement des données
df = pd.read_csv("donnees_rse_1.csv", encoding="utf-8-sig")
df.columns = df.columns.str.strip()

# Configuration de la page
st.set_page_config(page_title="Dashboard RSE", layout="wide")

# Logo et titre
logo = Image.open("logo_rse_streamlit.png")
st.image(logo, width=100)
st.title("📊 Tableau de bord RSE - Visualisation interactive")

# Filtres
entreprises = ["Toutes"] + sorted(df["Entreprise"].unique())
themes = ["Tous"] + sorted(df["Thème RSE"].unique())
col1, col2, col3 = st.columns(3)
selected_entreprise = col1.selectbox("Choisir une entreprise", entreprises)
selected_theme = col2.selectbox("Choisir un thème RSE", themes)
seuil = col3.slider("Seuil de performance", 0, 100, 50)

# Filtrage des données
filtered_df = df.copy()
if selected_entreprise != "Toutes":
    filtered_df = filtered_df[filtered_df["Entreprise"] == selected_entreprise]
if selected_theme != "Tous":
    filtered_df = filtered_df[filtered_df["Thème RSE"] == selected_theme]

# KPI
col_kpi1, col_kpi2 = st.columns(2)
col_kpi1.metric("Score RSE moyen", f"{filtered_df['Score RSE'].mean():.2f}")
col_kpi2.metric("Seuil de performance", seuil)

score_moyen = filtered_df["Score RSE"].mean()
if score_moyen < seuil:
    st.warning(f"⚠️ Seuil non atteint : le score moyen RSE est de {score_moyen:.2f}, inférieur au seuil de {seuil}.")

# Graphique: Moyenne par entreprise
st.subheader("Classement des entreprises selon leur Score RSE moyen")
mean_scores = df.groupby("Entreprise")["Score RSE"].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 4))
sns.barplot(x=mean_scores.index, y=mean_scores.values, palette="viridis", ax=ax)
ax.axhline(seuil, ls="--", color="red")
ax.set_title("Score RSE moyen par entreprise")
ax.set_ylabel("Score RSE moyen")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)
