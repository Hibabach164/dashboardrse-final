
import pandas as pd
import numpy as np

np.random.seed(42)
entreprises = [f"Entreprise {i}" for i in range(1, 21)]
themes = ["Environnement", "Gouvernance", "Social"]
indicateurs = {
    "Environnement": ["Émissions CO2", "Gestion déchets", "Énergie renouvelable"],
    "Gouvernance": ["Éthique", "Transparence", "Conformité réglementaire"],
    "Social": ["Égalité H/F", "Conditions de travail", "Formation continue"]
}

data = []
for entreprise in entreprises:
    for theme in themes:
        for indicateur in indicateurs[theme]:
            score = np.random.randint(20, 91)
            score_rse = round(score * np.random.uniform(0.6, 1.1), 1)
            data.append([entreprise, theme, indicateur, score, score_rse])

df = pd.DataFrame(data, columns=["Entreprise", "Thème RSE", "Indicateur", "Score", "Score RSE"])
df.to_csv("donnees_rse_1.csv", index=False)
