import os
import streamlit as st

import os

# Ottieni la directory dello script corrente
script_directory = os.path.dirname(os.path.abspath(__file__))

# Imposta la directory di lavoro sulla posizione dello script
os.chdir(script_directory)


# Titolo dell'app
st.title("Benvenuto nella mia prima app con Streamlit!")

# Creazione di un widget di input di testo
nome = st.text_input("Qual è il tuo nome?")

# Creazione di un pulsante
if st.button("Saluta!"):
    st.write(f"Ciao, {nome}!")

# Grafici e visualizzazione di dati
import numpy as np
import pandas as pd

# Dati casuali
dati = pd.DataFrame(np.random.randn(10, 2), columns=["Colonna 1", "Colonna 2"])
st.line_chart(dati)

