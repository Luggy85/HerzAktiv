import streamlit as st
import pandas as pd
from PIL import Image
import Leistungsanalyse as la
import Powercurve as pc
import traceback
import BMI
from ekg_daten import EKGAnalyzer
import os
import json
from Trainingslog import DataUploader  # Importieren Sie die neue Klasse

# Erstelle eine Instanz von DataUploader
uploader = DataUploader()

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

# Initialisiere die Zählvariable
if 'i' not in st.session_state:
    st.session_state['i'] = 0

# Toggle-Buttons aktualisieren
def update_toggles(toggled_key):
    if toggled_key == 'toggle_1' and st.session_state.toggle_1:
        st.session_state.toggle_2 = False
        st.session_state.toggle_3 = False
        st.session_state.toggle_4 = False
        st.session_state.diagram = 1
    elif toggled_key == 'toggle_2' and st.session_state.toggle_2:
        st.session_state.toggle_1 = False
        st.session_state.toggle_3 = False
        st.session_state.toggle_4 = False
        st.session_state.diagram = 2
    elif toggled_key == 'toggle_3' and st.session_state.toggle_3:
        st.session_state.toggle_1 = False
        st.session_state.toggle_2 = False
        st.session_state.toggle_4 = False
        st.session_state.diagram = 3
    elif toggled_key == 'toggle_4' and st.session_state.toggle_4:
        st.session_state.toggle_1 = False
        st.session_state.toggle_2 = False
        st.session_state.toggle_3 = False
        st.session_state.diagram = 4
    else:
        st.session_state.diagram = None

# Initialisiere die Toggle-Buttons im Session State
if 'toggle_1' not in st.session_state:
    st.session_state.toggle_1 = False
if 'toggle_2' not in st.session_state:
    st.session_state.toggle_2 = False
if 'toggle_3' not in st.session_state:
    st.session_state.toggle_3 = False
if 'toggle_4' not in st.session_state:
    st.session_state.toggle_4 = False
if 'diagram' not in st.session_state:
    st.session_state.diagram = None

# Diagramm anzeigen
def show_diagram():
    if st.session_state.get('diagram') == 1:
        max_heartrate = st.session_state.get('max_heartrate', 200)
        tab1, tab2 = st.tabs(['Leistungszonen', 'Power Curve'])
        with tab1:
            st.plotly_chart(la.plot_leistung_herzfrequenz(la.activity_data, max_heartrate))
        with tab2:
            st.plotly_chart(pc.plot_powercurve())
    elif st.session_state.get('diagram') == 2:
        person_data = EKGAnalyzer.load_person_data('data/person_db.json')
        ekg_type = st.selectbox('EKG-Typ', ['Ruhe-EKG', 'Belastungs-EKG'], index=0, key='selected_ekg_type')
        ekg_file_path = uploader.get_ekg_file_path(st.session_state.current_user_name, ekg_type)
        if ekg_file_path:
            st.write(f"EKG-Dateipfad: {ekg_file_path}")
            fig, mean_hr, max_hr = EKGAnalyzer.analyze_and_plot_ekg(ekg_file_path)
            if fig:
                st.plotly_chart(fig)
                return mean_hr, max_hr
            else:
                st.write('Keine gültigen RR-Intervalle gefunden.')
        else:
            st.write('Keine EKG-Daten für die ausgewählte Person und den EKG-Typ gefunden.')

# Daten der Leistungsanalyse anzeigen
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
        st.plotly_chart(BMI.create_bmi_chart(bmi, category))

def trainingslog():
    if st.session_state.get('diagram') == 4:
        uploaded_file = st.file_uploader("Wähle eine JSON Datei", type="json")
        if uploaded_file is not None:
            json_data = json.load(uploaded_file)
            uploader.process_json_data(json_data, uploaded_file.name)  # Verarbeitet und speichert Daten
            st.session_state['file_uploaded'] = True
            st.success("Datei wurde erfolgreich hochgeladen und verarbeitet.")
        else:
            st.error("Keine Datei hochgeladen.")

def analyse_training():
    if st.session_state.get('diagram') == 4:
        person_id = st.text_input("Gib die ID der Person ein, deren Daten analysiert werden sollen")
        if person_id:
            results = uploader.analyze_training_data(person_id)
            if results:
                st.write("Ergebnisse:")
                st.dataframe(results)
            else:
                st.write("Keine Daten gefunden für die angegebene ID.")

def compare_training():
    if st.session_state.get('diagram') == 4:
        person_id = st.text_input("Gib die ID der Person ein, deren Trainingsdaten verglichen werden sollen")
        if person_id:
            training_sessions = uploader.get_training_list(person_id)
            if training_sessions:
                # Auswahl der Sitzung für den Vergleich
                session_dates = [session['Datum'] for session in training_sessions]
                selected_date = st.selectbox("Wähle eine Trainingssitzung zum Vergleich", session_dates)
                current_session = training_sessions[0]  # Nehmen Sie an, dass dies die aktuellsten Daten sind
                selected_session = next((session for session in training_sessions if session['Datum'] == selected_date), None)

                # Anzeigen der ausgewählten und aktuellen Trainingsdaten
                if selected_session:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Aktuelle Trainingsdaten")
                        for key, value in current_session.items():
                            st.text(f"{key}: {value}")
                    with col2:
                        st.subheader("Vergleichs-Trainingsdaten")
                        for key, value in selected_session.items():
                            st.text(f"{key}: {value}")
            else:
                st.write("Keine Trainingsdaten gefunden für die angegebene ID.")

# Seitenleiste mit Toggle-Buttons und Radiobuttons für Versuchsperson-Auswahl
with st.sidebar:
    # Logo und Titel
    col1, col2 = st.columns(2)
    with col1:
        st.image('data/pictures/Logo2.jpeg', width=100)
    with col2:
        st.markdown('<p class="custom-position1 big-font">HerzAktiv</p>', unsafe_allow_html=True)

    # Toggle-Buttons
    st.toggle('Leistungs-Analyse', value=st.session_state.toggle_1, key='toggle_1', on_change=update_toggles, args=('toggle_1',))
    st.toggle('BMI-Analyse', value=st.session_state.toggle_3, key='toggle_3', on_change=update_toggles, args=('toggle_3',))
    st.toggle('EKG-Analyse', value=st.session_state.toggle_2, key='toggle_2', on_change=update_toggles, args=('toggle_2',))
    st.toggle('Trainingslog', value=st.session_state.toggle_4, key='toggle_4', on_change=update_toggles, args=('toggle_4',))

    # Radiobuttons für Versuchsperson-Auswahl
    if st.session_state.toggle_2:
        if 'current_user_name' not in st.session_state:
            st.session_state.current_user_name = 'None'
        person_names = uploader.get_person_names()
        st.session_state.current_user_name = st.radio('Versuchsperson', options=person_names, key="sbVersuchsperson")

# Anzeigen von Diagrammen und Daten basierend auf der ausgewählten Option in der Seitenleiste
if st.session_state.get('diagram') is not None:
    if st.session_state.get('diagram') == 1:
        show_data()
        show_diagram()
    elif st.session_state.get('diagram') == 2:
        show_diagram()
    elif st.session_state.get('diagram') == 3:
        analyse_bmi()
    elif st.session_state.get('diagram') == 4:
        trainingslog()

# Bild und Datenanzeige bei ausgewählter EKG-Analyse
if st.session_state.get('diagram') == 2:
    with st.container():
        image_path = uploader.get_person_image_path(st.session_state.current_user_name)
        image = Image.open(image_path)
        st.image(image, caption=f"{st.session_state.current_user_name}")
        mean_hr, max_hr = show_diagram()
        if mean_hr is not None and max_hr is not None:
            st.metric('Mittlere Herzfrequenz im Zeitraum', f'{mean_hr} BPM')
            st.metric('Maximale Herzfrequenz im Zeitraum', f'{max_hr} BPM')