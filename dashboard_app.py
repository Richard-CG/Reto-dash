import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="reto-dashboard-6ad18")
movies_ref = db.collection("movies")

docs = movies_ref.stream()

# Convertir los documentos en una lista de diccionarios
movies_data = [doc.to_dict() for doc in docs]
print(movies_data)

st.title('Streamlit con atributo cache')

# Función para cargar datos desde Firestore con caché
@st.cache_data
def load_data(nrows=None):

    df = pd.DataFrame(movies_data)
    
    # Limitar el número de filas si se especifica
    if nrows:
        df = df.head(nrows)
    
    return df

# Estado de carga
data_load_state = st.text("Cargando datos...")

# Llamar a la función para cargar los datos
df = load_data(100)
data_load_state.text("¡Datos cargados exitosamente! (usando st.cache)")





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
