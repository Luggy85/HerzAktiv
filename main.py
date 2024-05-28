import streamlit as st
import pandas as pd
import read_data as rd
from PIL import Image
import Leistungsanalyse as la
import traceback
import BMI

# Setze das Seitenlayout auf "wide"
st.set_page_config(layout="wide")

# CSS-Stile definieren
st.markdown("""
<style>
.big-font {
    font-size: 40px !important;
    font-weight: bold;
}
.custom-font {
    font-size: 50px !important;
    font-weight: bold;
    color: darkred;
}
.custom-position1 {
    margin-top: 20px;
    margin-left: -50px;
}
.custom-position2 {
    margin-top: -40px;
    margin-left: 200px;
    position: absolute;
}

</style>
""", unsafe_allow_html=True)

# Callback-Funktion für Radiobutton-Auswahl
def callback_function():
    print(f"The user has changed to {st.session_state.current_user}")

# Toggle-Buttons aktualisieren
def update_toggles(toggled_key):
    if toggled_key == 'toggle_1' and st.session_state.toggle_1:
        st.session_state.toggle_2 = False
        st.session_state.toggle_3 = False
        st.session_state.diagram = 1
    elif toggled_key == 'toggle_2' and st.session_state.toggle_2:
        st.session_state.toggle_1 = False
        st.session_state.toggle_3 = False
        st.session_state.diagram = 2
    elif toggled_key == 'toggle_3' and st.session_state.toggle_3:
        st.session_state.toggle_1 = False
        st.session_state.toggle_2 = False
        st.session_state.diagram = 3
    else:
        st.session_state.diagram = None

# Diagramm anzeigen
def show_diagram():
    if 'max_heartrate' not in st.session_state:
        st.session_state['max_heartrate'] = 200

    max_heartrate = st.session_state['max_heartrate']

    if st.session_state.get('diagram') == 1:
        if max_heartrate is not None:
            st.plotly_chart(la.plot_leistung_herzfrequenz(la.activity_data, max_heartrate))
    elif st.session_state.get('diagram') == 2:
        st.write('Kein Diagramm ausgewählt')

# Daten anzeigen
def show_data():
    if st.session_state.get('diagram') == 1:
        max_heartrate = st.slider('Maximale Herzfrequenz', min_value=100, max_value=220, step=1, value=st.session_state.get('max_heartrate', 200))
        st.session_state['max_heartrate'] = max_heartrate

        # Spalten für die Kennzahlen
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Mittelwert der Leistung", value=f"{la.mittelwert_leistung} Watt")
        with col2:
            st.metric(label="Maximalwert der Leistung", value=f"{la.maximalwert_leistung} Watt")

        zeit_in_zonen = la.analyze_heart_zones(max_heartrate)

        # Weitere Spalten für die Zeit in Zonen
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Zeit in Zone 1", value=f"{zeit_in_zonen['Z1']} s")
            st.metric(label="Zeit in Zone 2", value=f"{zeit_in_zonen['Z2']} s")
            st.metric(label="Zeit in Zone 3", value=f"{zeit_in_zonen['Z3']} s")
        with col2:
            st.metric(label="Zeit in Zone 4", value=f"{zeit_in_zonen['Z4']} s")
            st.metric(label="Zeit in Zone 5", value=f"{zeit_in_zonen['Z5']} s")

def analyse_bmi():
    if st.session_state.get('diagram') == 3:
        weight = st.number_input('Gewicht (kg)', min_value=0.0, max_value=200.0, value=70.0)
        height = st.number_input('Größe (m)', min_value=0.0, max_value=2.5, value=1.75)
        bmi, category = BMI.calculate_bmi(weight, height)
        st.write(f"Ihr BMI beträgt {bmi}. Sie befinden sich in der Kategorie '{category}'.")


# Initialisiere die Toggle-Buttons im Session State
if 'toggle_1' not in st.session_state:
    st.session_state.toggle_1 = False
if 'toggle_2' not in st.session_state:
    st.session_state.toggle_2 = False
if 'toggle_3' not in st.session_state:
    st.session_state.toggle_3 = False
if 'diagram' not in st.session_state:
    st.session_state.diagram = None

# Seitenleiste
with st.sidebar:
    # Logo und Titel
    col1, col2 = st.columns(2)
    with col1:
        st.image('/Users/lukas/Documents/MCI/Software_engineering/HerzAktiv/Logo2.jpeg', width=100)
    with col2:
        st.markdown('<p class="custom-position1 big-font">HerzAktiv</p>', unsafe_allow_html=True)
    st.write('Webseite zur Visualisierung der Leistungs- und EKG-Daten.')

    # Toggle-Buttons
    Leistungs_button = st.toggle('Leistungs-Analyse', value=st.session_state.toggle_1, key='toggle_1', on_change=update_toggles, args=('toggle_1',))
    BMI_button = st.toggle('BMI-Analyse', value=st.session_state.toggle_3, key='toggle_3', on_change=update_toggles, args=('toggle_3',))
    EKG_button = st.toggle('EKG-Analyse', value=st.session_state.toggle_2, key='toggle_2', on_change=update_toggles, args=('toggle_2',))

    # Radiobuttons für Versuchsperson-Auswahl bei aktivierter EKG-Analyse
    if st.session_state.toggle_2:
        if 'current_user' not in st.session_state:
            st.session_state.current_user = 'None'

        person_dict = rd.load_person_data()
        person_names = rd.get_person_list(person_dict)

        st.session_state.current_user = st.radio(
            'Versuchsperson',
            options=person_names, key="sbVersuchsperson", on_change=callback_function
        )

# Überschrift und Datenanzeige basierend auf der Auswahl
header_html = ""
if st.session_state.get('diagram') == 1:
    header_html = '<p class="custom-position2 custom-font">Leistungsdaten</p>'
    st.markdown(header_html, unsafe_allow_html=True)
    show_data()
elif st.session_state.get('diagram') == 2:
    header_html = '<p class="custom-position2 custom-font">EKG-Daten</p>'
    st.markdown(header_html, unsafe_allow_html=True)
elif st.session_state.get('diagram') == 3:
    header_html = '<p class="custom-position2 custom-font">BMI-Analyse</p>'
    st.markdown(header_html, unsafe_allow_html=True)
    analyse_bmi()
elif st.session_state.get('diagram') is None:
    header_html = '<p class="custom-position2 custom-font">HerzAktiv <3</p>'
    st.markdown(header_html, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col2:
        image = Image.open("/Users/lukas/Documents/MCI/Software_engineering/HerzAktiv/data/pictures/sila_lukas.png")
        st.image(image, caption="Erstellt von Sila und Lukas", width=350)

# Bild und Datenanzeige bei ausgewählter EKG-Analyse
if st.session_state.get('diagram') == 2:
    col1, col2 = st.columns([1, 2])
    with col1:
        if 'picture_path' not in st.session_state:
            st.session_state.picture_path = 'data/pictures/none.jpg'

        if st.session_state.current_user in person_names:
            st.session_state.picture_path = rd.find_person_data_by_name(st.session_state.current_user)['picture_path']
        image = Image.open("/Users/lukas/Documents/MCI/Software_engineering/HerzAktiv/" + st.session_state.picture_path)
        st.image(image, caption=f"{st.session_state.current_user} ({rd.find_age(st.session_state.current_user)})")
    with col2:
        st.write('Keine Daten vorhanden')

# Diagramm am Ende des Skripts aufrufen
if 'diagram' in st.session_state:
    try:
        show_diagram()
    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {e}")
        st.text('Fehler-Traceback:')
        st.text(traceback.format_exc())
