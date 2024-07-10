import streamlit as st
import pandas as pd
import read_data as rd
from PIL import Image
import Leistungsanalyse as la
import Powercurve as pc
import traceback
import BMI
from ekg_daten import EKGAnalyzer
import os
from Trainingslog import CSVUploader


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


# Callback-Funktion für Radiobutton-Auswahl
def callback_function():
    print(f"The user has changed to {st.session_state.current_user_name}")

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

# Initialisiere den Zustand nur, wenn er noch nicht vorhanden ist
if 'selected_ekg_type' not in st.session_state:
    st.session_state['selected_ekg_type'] = 'Ruhe-EKG'

# Funktion zur Aktualisierung der Daten basierend auf der EKG-Typ Auswahl
def update_data():
    ekg_type = st.session_state['selected_ekg_type']




# Diagramm anzeigen
def show_diagram():

    if st.session_state.get('diagram') == 1:
        if 'max_heartrate' not in st.session_state:
            st.session_state['max_heartrate'] = 200

        max_heartrate = st.session_state['max_heartrate']

        tab1, tab2 = st.tabs(['Leistungszonen', 'Power Curve'])
        with tab1:
            if max_heartrate is not None:
                st.plotly_chart(la.plot_leistung_herzfrequenz(la.activity_data, max_heartrate))
        with tab2:
            st.plotly_chart(pc.plot_powercurve())

    elif st.session_state.get('diagram') == 2:
        # Laden der Personendaten
        person_data = EKGAnalyzer.load_person_data('data/person_db.json')

        # Auswahl des EKG-Typs über eine SelectBox
        ekg_type = st.selectbox('EKG-Typ', ['Ruhe-EKG', 'Belastungs-EKG'], index=0, key='selected_ekg_type', on_change=update_data)

        # Ermittle den Pfad der EKG-Datei basierend auf der ausgewählten Person und dem EKG-Typ
        ekg_file_path = None
        selected_person = None
        if st.session_state.current_user_name:
            selected_person = next((person for person in person_data if f"{person['firstname']} {person['lastname']}" == st.session_state.current_user_name), None)
            
            if selected_person and 'ekg_tests' in selected_person:
                test = next((test for test in selected_person['ekg_tests'] if test['type'] == ekg_type), None)
                if test:
                    ekg_file_path = test['result_link']

        st.session_state['ekg_file_path'] = ekg_file_path

        if ekg_file_path:
            st.write(f"EKG-Dateipfad: {ekg_file_path}")
            analyzer = EKGAnalyzer()
            fig, mean_hr, max_hr = analyzer.analyze_and_plot_ekg(st.session_state.current_user_name, ekg_file_path)
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

# Initialisiere Session-State-Variablen
if 'new_data' not in st.session_state:
    st.session_state['new_data'] = {}
if 'json_data' not in st.session_state:
    st.session_state['json_data'] = None
if 'file_name' not in st.session_state:
    st.session_state['file_name'] = None
if 'data_saved' not in st.session_state:
    st.session_state['data_saved'] = False
if 'file_uploaded' not in st.session_state:
    st.session_state['file_uploaded'] = False


def read_csv_file(file_path):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        st.error("Die hochgeladene Datei ist leer oder existiert nicht.")
        return None
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            st.error("Die Datei enthält keine Daten.")
            return None
        return df
    except Exception as e:
        st.error(f"Fehler beim Lesen der Datei: {e}")
        return None
    


def trainingslog():
    if st.session_state.get('diagram') == 4:
        uploader = CSVUploader()
        try:
            upload_result = uploader.upload_file()
            if upload_result is not None:
                uploaded_file, file_path = upload_result
                if uploaded_file is not None:
                    df = uploader.read_csv_file(file_path)
                    if df is not None and not df.empty:
                        st.success("Daten erfolgreich geladen und bereit zur weiteren Verarbeitung.")
                        uploader.display_form()
                    else:
                        st.warning("Keine verwertbaren Daten in der Datei gefunden.")
                else:
                    st.warning("Es wurde keine Datei hochgeladen.")
            else:
                st.error("Fehler beim Hochladen der Datei.")
        except Exception as e:
            st.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")


def analyse_training():
    if st.session_state.get('diagram') == 4:
        uploader = CSVUploader()
        if st.session_state['new_data'] and st.session_state['json_data'] is not None:
            additional_data = st.session_state['new_data']
            result_df = uploader.analyze_json(st.session_state['json_data'], additional_data)
            st.write("Ergebnisse:")
            st.dataframe(result_df)
            st.session_state['new_data'].update(result_df.iloc[0].to_dict())  # Update the new_data with analysis results

def compare_training():
    if st.session_state.get('diagram') == 4:
        uploader = CSVUploader()
        if 'new_data' in st.session_state and st.session_state['new_data']:
            person_id = st.session_state['new_data']['ID']
            training_list = uploader.get_training_list(person_id)

            if training_list.empty:
                st.write("Keine vergleichbaren Trainingsdaten gefunden.")
                return

            st.subheader("Vergleich der Trainingsdaten")

            col1, col2 = st.columns(2)

            with col1:
                st.write("Aktuelles Training")
                current_training = st.session_state['new_data']
                st.write(f"ID: {current_training['ID']}")
                st.write(f"Name: {current_training['Name']}")
                st.write(f"Trainingsart: {current_training['Trainingsart']}")
                st.write(f"Datum: {current_training['Datum']}")
                st.write(f"Gewicht: {current_training['Gewicht']} kg")
                st.write(f"Größe: {current_training['Größe']} cm")
                st.write(f"Durchschnittliche Herzfrequenz: {current_training.get('Durchschnittliche Herzfrequenz', 'N/A')} BPM")
                st.write(f"Maximale Herzfrequenz: {current_training.get('Maximale Herzfrequenz', 'N/A')} BPM")
                st.write(f"Minimale Herzfrequenz: {current_training.get('Minimale Herzfrequenz', 'N/A')} BPM")
                st.write(f"Trainingsdauer: {current_training.get('Trainingsdauer (Minuten)', 'N/A')} Minuten")
                st.write(f"Kalorienverbrauch: {current_training.get('Kalorienverbrauch', 'N/A')} kcal")
                st.write(f"Schritte: {current_training.get('Schritte', 'N/A')}")
                st.write(f"Durchschnittliche Intensität: {current_training.get('Durchschnittliche Intensität', 'N/A')} kcal/hr·kg")

            with col2:
                st.write("Vergleichbares Training auswählen")
                selected_date = st.selectbox("Wähle ein Training zum Vergleich", training_list['Datum'], key="compare_training_selectbox_{person_id}")
                if selected_date:
                    selected_training = training_list[training_list['Datum'] == selected_date].iloc[-1]
                    st.write(f"ID: {selected_training['ID']}")
                    st.write(f"Name: {selected_training['Name']}")
                    st.write(f"Trainingsart: {selected_training['Trainingsart']}")
                    st.write(f"Datum: {selected_training['Datum']}")
                    st.write(f"Gewicht: {selected_training['Gewicht']} kg")
                    st.write(f"Größe: {selected_training['Größe']} cm")
                    st.write(f"Durchschnittliche Herzfrequenz: {selected_training['Durchschnittliche Herzfrequenz']} BPM")
                    st.write(f"Maximale Herzfrequenz: {selected_training['Maximale Herzfrequenz']} BPM")
                    st.write(f"Minimale Herzfrequenz: {selected_training['Minimale Herzfrequenz']} BPM")
                    st.write(f"Trainingsdauer: {selected_training['Trainingsdauer (Minuten)']} Minuten")
                    st.write(f"Kalorienverbrauch: {selected_training['Kalorienverbrauch']} kcal")
                    st.write(f"Schritte: {selected_training['Schritte']}")
                    st.write(f"Durchschnittliche Intensität: {selected_training['Durchschnittliche Intensität']} kcal/hr·kg")



#Seitenleiste
with st.sidebar:
    # Logo und Titel
    col1, col2 = st.columns(2)
    with col1:
        st.image('data/pictures/Logo2.jpeg', width=100)
    with col2:
        st.markdown('<p class="custom-position1 big-font">HerzAktiv</p>', unsafe_allow_html=True)
    st.write('Webseite zur Visualisierung der Leistungs- und EKG-Daten.')

    # Toggle-Buttons
    Leistungs_button = st.toggle('Leistungs-Analyse', value=st.session_state.toggle_1, key='toggle_1', on_change=update_toggles, args=('toggle_1',))
    BMI_button = st.toggle('BMI-Analyse', value=st.session_state.toggle_3, key='toggle_3', on_change=update_toggles, args=('toggle_3',))
    EKG_button = st.toggle('EKG-Analyse', value=st.session_state.toggle_2, key='toggle_2', on_change=update_toggles, args=('toggle_2',))
    Trainingslog_button = st.toggle('Trainingslog', value=st.session_state.toggle_4, key='toggle_4', on_change=update_toggles, args=('toggle_4',))

    # Radiobuttons für Versuchsperson-Auswahl bei aktivierter EKG-Analyse
    if st.session_state.toggle_2:
        if 'current_user_name' not in st.session_state:
            st.session_state.current_user_name = 'None'

        person_dict = rd.Person.load_person_data()
        person_names = rd.Person.get_person_list(person_dict)

        st.session_state.current_user_name = st.radio(
            'Versuchsperson',
            options=person_names, key="sbVersuchsperson", on_change=callback_function
        )
        st.session_state.current_user = rd.Person(rd.Person.find_person_data_by_name(st.session_state.current_user_name))

# Überschrift und Datenanzeige basierend auf der Auswahl
header_html = ""
if st.session_state.get('diagram') == 1:
    header_html = '<p class="custom-position2 custom-font">Leistungsdaten</p>'
    st.markdown(header_html, unsafe_allow_html=True)
    show_data()
    show_diagram()
elif st.session_state.get('diagram') == 2:
    header_html = '<p class="custom-position2 custom-font">EKG-Daten</p>'
    st.markdown(header_html, unsafe_allow_html=True)

elif st.session_state.get('diagram') == 3:
    header_html = '<p class="custom-position2 custom-font">BMI-Analyse</p>'
    st.markdown(header_html, unsafe_allow_html=True)
    analyse_bmi()

elif st.session_state.get('diagram') == 4:
    header_html = '<p class="custom-position2 custom-font">Trainingslog</p>'
    st.markdown(header_html, unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(['Daten-Import', 'Daten-Analyse', 'Daten-Vergleich'])
    with tab1:
        trainingslog()
    with tab2: 
        analyse_training()
    with tab3:
        compare_training()



elif st.session_state.get('diagram') is None:
    header_html = '<p class="custom-position2 custom-font">HerzAktiv <3</p>'
    st.markdown(header_html, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col2:
        image = Image.open("data/pictures/sila_lukas.png")
        st.image(image, caption="Erstellt von Sila und Lukas", width=350)

# Bild und Datenanzeige bei ausgewählter EKG-Analyse
if st.session_state.get('diagram') == 2:
    col1, col2 = st.columns([1, 2])
    with col1:
        if 'picture_path' not in st.session_state:
            st.session_state.picture_path = 'data/pictures/none.jpg'

        if st.session_state.current_user_name in person_names:
            st.session_state.picture_path = rd.Person.find_person_data_by_name(st.session_state.current_user_name)['picture_path']
        image = Image.open(st.session_state.picture_path)
        st.image(image, caption=f"{st.session_state.current_user_name} ({st.session_state.current_user.find_age()})")

    mean_hr, max_hr = show_diagram()  # Hier wird show_diagram aufgerufen und die Herzfrequenzmetriken werden zurückgegeben
    
    if mean_hr is not None and max_hr is not None:
        mean_hr = round(mean_hr, 2)
        max_hr = round(max_hr, 2)
        with col2:
            st.metric(label='Mittlere Herzfrequenz im Zeitraum', value=f'{mean_hr} BPM')
            st.metric(label='Maximale Herzfrequenz im Zeitraum', value=f'{max_hr} BPM')

