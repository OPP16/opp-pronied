import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import plotly.express as px

st.markdown("""
    <link rel='stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'>
    <style>
        /* Tu estilo personalizado si es necesario */
    </style>
""", unsafe_allow_html=True)

# ---- LEER EXCEL ----
@st.cache_data
def get_data_from_excel():
    # Leer el archivo Excel
    df = pd.read_excel(
        io="data/excel/EJECUCION 2023.xlsx",
        engine="openpyxl",
        sheet_name="2023",
        header=0,
    )
    return df  # Devolver el DataFrame

# Obtener los datos del archivo Excel
df = get_data_from_excel()

################################
#CARD
################################
# Calcular los totales
total_mto_pia = df['mto_pia'].sum()
total_mto_pim = df['mto_pim'].sum()
total_mto_certificado = df['mto_certificado'].sum()
total_mto_compro_anual = df['mto_compro_anual'].sum()

# Estilo para las columnas (con clases de Bootstrap)
column_style = "display: inline-block; padding: 1rem; width: 100%;"

# Crear las columnas con estilo de tarjeta y borde azul
st.markdown("## Resumen Financiero")
st.markdown(f"""
<div class="row">
    <div class="col-md-4">
        <div class="card text-white bg-dark mb-3" style="{column_style}">
            <div class="card-body">
                <strong class="card-title text-primary">PIA</strong>
                <p class="card-text">S/{total_mto_pia:,.2f}</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-white bg-dark mb-3" style="{column_style}">
            <div class "card-body">
                <strong class="card-title text-primary">PIM</strong>
                <p class="card-text">S/{total_mto_pim:,.2f}</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-white bg-dark mb-3" style="{column_style}">
            <div class="card-body">
                <strong class="card-title text-primary">CERTIFICADO</strong>
                <p class="card-text">S/{total_mto_certificado:,.2f}</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-white bg-dark mb-3" style="{column_style}">
            <div class="card-body">
                <strong class="card-title text-primary">COMPROMETIDO</strong>
                <p class="card-text">S/{total_mto_compro_anual:,.2f}</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

################################


################################
#FILTROS
################################
st.sidebar.header("Filtros:")

if not df.empty:
    # Agregar la opción "Todos" a cada selectbox
    t1 = st.sidebar.selectbox(
        "Selecciona el T1:",
        options=['Todos'] + df["programa_pptal"].unique().tolist(),
    )

    t2 = st.sidebar.selectbox(
        "Selecciona el Tipo de Cliente:",
        options=['Todos'] + df["tipo_prod_proy"].unique().tolist(),
    )

    t3 = st.sidebar.selectbox(
        "Selecciona el T3:",
        options=['Todos'] + df["tipo_act_obra_ac"].unique().tolist(),
    )

    t4 = st.sidebar.selectbox(
        "Selecciona el T4:",
        options=['Todos'] + df["activ_obra_accinv"].unique().tolist(),
    )

    t5 = st.sidebar.selectbox(
        "Selecciona el T5:",
        options=['Todos'] + df["funcion"].unique().tolist(),
    )

    # Filtrar el DataFrame según los valores seleccionados en la barra lateral
    if t1 != 'Todos':
        df_selection = df[df["programa_pptal"] == t1]
    else:
        df_selection = df.copy()

    if t2 != 'Todos':
        df_selection = df_selection[df_selection["tipo_prod_proy"] == t2]

    if t3 != 'Todos':
        df_selection = df_selection[df_selection["tipo_act_obra_ac"] == t3]

    if t4 != 'Todos':
        df_selection = df_selection[df_selection["activ_obra_accinv"] == t4]

    if t5 != 'Todos':
        df_selection = df_selection[df_selection["funcion"] == t5]

    # Mostrar los datos filtrados en una tabla
    st.write("Datos Filtrados:")
    st.dataframe(df_selection)  # Utiliza st.dataframe para mostrar la tabla

else:
    st.warning("Los datos del archivo Excel no se han cargado correctamente.")

################################
#GRAFICO 1
################################
meses_numeros = range(1, 13)
total_mensual = []

for mes_numero in meses_numeros:
    mes_columna = f'mto_devenga_{mes_numero:02}'  # Genera el nombre de la columna
    total_mensual.append(df_selection[mes_columna].sum() / 1e6)

# Nombres de los meses para etiquetas en el gráfico
meses = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SET', 'OCT', 'NOV', 'DIC']

# Crear un DataFrame con los totales mensuales
df_mensual = pd.DataFrame({'Mes': meses, 'Total_Mensual (en millones)': total_mensual})

# Crear un gráfico de barras con las barras en vertical
fig = px.bar(
    df_mensual,
    x='Mes',
    y='Total_Mensual (en millones)',
    labels={'Total_Mensual (en millones)': 'Devengado Mensual (en millones)'},
    title='Total Devengado Mensual por Mes',
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)