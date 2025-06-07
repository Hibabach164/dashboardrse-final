
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# --- Logo ---
logo = Image.open("logo_rse_streamlit.png")
st.image(logo, width=120)

# --- Titre principal ---
st.markdown("<h1 style='text-align: center; color: #6a0dad;'>🌿 Dashboard RSE interactif</h1>", unsafe_allow_html=True)

# --- Chargement du fichier CSV (encodage compatible) ---
try:
    df = pd.read_csv("donnees_rse_1.csv", encoding="utf-8-sig", sep=";")
except Exception as e:
    st.error(f"Erreur de lecture CSV : {e}")
    st.stop()
df.columns = df.columns.str.strip()
st.write("Colonnes chargées :", df.columns.tolist())



# --- Nettoyage éventuel des colonnes (strip espaces) ---
df.columns = df.columns.str.strip()

# --- Vérification & renommage ---
if "Entreprises" in df.columns:
    df.rename(columns={"Entreprises": "Entreprise"}, inplace=True)

# --- Filtres interactifs dans la sidebar ---
with st.sidebar:
    st.header("🔎 Filtres interactifs")
    themes = st.multiselect("🎯 Thème RSE", options=df["Thème RSE"].unique(), default=df["Thème RSE"].unique())
    entreprises = st.multiselect("🏢 Entreprises", options=df["Entreprise"].unique(), default=df["Entreprise"].unique())
    score_min = st.slider("🌡️ Score RSE minimal", min_value=0, max_value=100, value=50)

# --- Filtrage des données ---
df_filtre = df[
    (df["Thème RSE"].isin(themes)) &
    (df["Entreprise"].isin(entreprises)) &
    (df["Score RSE"] >= score_min)
]

# --- Aperçu ---
st.subheader("📑 Aperçu des données filtrées")
st.dataframe(df_filtre)

# --- Moyennes par entreprise ---
score_moy = df_filtre.groupby("Entreprise")["Score RSE"].mean().reset_index().sort_values(by="Score RSE", ascending=False)

# --- Graphique barres ---
st.subheader("📈 Score RSE moyen par entreprise")
fig = px.bar(score_moy, x="Entreprise", y="Score RSE", color="Score RSE", color_continuous_scale="greens")
st.plotly_chart(fig, use_container_width=True)

# --- Jauge ---
st.subheader("🎯 Score RSE moyen global")
moyenne_globale = round(score_moy["Score RSE"].mean(), 2)
fig_jauge = px.pie(values=[moyenne_globale, 100 - moyenne_globale], names=["Score Moyen", "Reste"], hole=0.7,
                   color_discrete_sequence=["#6a0dad", "#e8e8e8"])
fig_jauge.update_traces(textinfo='percent+label')
st.plotly_chart(fig_jauge, use_container_width=True)

# --- Export CSV ---
csv_export = score_moy.to_csv(index=False).encode("utf-8")
st.download_button("📥 Exporter les résultats", csv_export, "scores_rse_filtrés.csv", "text/csv")

# --- Footer ---
st.markdown("<hr><p style='text-align: center;'>🚀 Mémoire Data Analytics | Hibat Allah Bachterzi | 2025</p>", unsafe_allow_html=True)
