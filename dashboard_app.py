import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="reto-dashboard-6ad18")


st.title('Streamlit con atributo cache')

@st.cache
def load_data(nrows=None):

  movies_ref = db.collection("movies")
  docs = movies_ref.stream()
  movies_data = []
  for doc in docs:
      movies_data.append(doc.to_dict())
  df = pd.DataFrame(movies_data,nrows=nrows)

  return df
data_load_state=st.text("cargando data...")
df=load_data(100)
data_load_state.text("Bien!  (usando st.cache)")


# Checkbox para mostrar todos los filmes
if st.sidebar.checkbox("Mostrar todos los filmes"):
    st.write(df)

# Búsqueda de filmes por título
st.sidebar.write("Buscar filme por título:")
search_title = st.sidebar.text_input("Título del filme")
if st.sidebar.button("Buscar"):
    result = df[df["name"].str.contains(search_title, case=False, na=False)]
    st.write(result)

# Filtrado por director
st.sidebar.write("Filtrar por director:")
director = st.sidebar.selectbox("Selecciona un director", df["director"].unique())
if st.sidebar.button("Filtrar por director"):
    result = df[df["director"] == director]
    st.write(f"Total de filmes encontrados: {len(result)}")
    st.write(result)

# Formulario para insertar un nuevo filme
st.sidebar.write("Añadir un nuevo filme:")
new_company = st.sidebar.text_input("Compañía")
new_director = st.sidebar.text_input("Director")
new_genre = st.sidebar.text_input("Género")
new_name = st.sidebar.text_input("Nombre del filme")

if st.sidebar.button("Añadir filme"):
    # Insertar en Firestore
    db.collection("movies").add({
        "company": new_company,
        "director": new_director,
        "genre": new_genre,
        "name": new_name
    })
    st.sidebar.success("Filme añadido exitosamente.")
