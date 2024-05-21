import streamlit as st
import pandas as pd
import read_data as rd
from PIL import Image
import Leistungsanalyse as la
import traceback


st.set_page_config(layout="wide")
st.markdown("""
<style>
.big-font {
    font-size:40px !important;
    font-weight: bold;
}
.custom-font {
    font-size:50px !important;
    font-weight: bold;
}
.custom-position1 {
    margin-top: 20px;
    margin-left: -50px;
}
.custom-position2 {
    margin-top: -310px;
    margin-left: 200px;
}
</style>
""", unsafe_allow_html=True)

def callback_function():
    # Logging Message
    print(f"The user has changed to {st.session_state.current_user}")


# Funktion zum Aktualisieren der Toggle-Buttons basierend auf den Änderungen
def update_toggles(toggled_key):
    if toggled_key == 'toggle_1' and st.session_state.toggle_1:
        st.session_state.toggle_2 = False
        st.session_state.diagram = 1
    elif toggled_key == 'toggle_2' and st.session_state.toggle_2:
        st.session_state.toggle_1 = False
        st.session_state.diagram = 2

def show_diagram():
    if st.session_state.get('diagram') == 1:
        # Leistungsanalyse
        st.plotly_chart(la.plot_leistung_herzfrequenz(la.activity_data))
    elif st.session_state.get('diagram') == 2:
        st.write('Kein Diagramm ausgewählt')

def show_data():
    if st.session_state.get('diagram') == 1:
        # Leistungsanalyse
        max_heartrate = st.slider('Maximale Herzfrequenz', min_value=100, max_value=220, step=1)
        st.write(f"Mittelwert der Leistung: {la.mittelwert_leistung} Watt")
        st.write(f"Maximalwert der Leistung: {la.maximalwert_leistung} Watt")
        zeit_in_zonen = la.analyze_heart_zones(max_heartrate)
        st.write(f"Zeit in den Zonen: {zeit_in_zonen} Sekunden")
        
        return max_heartrate
   

    #elif st.session_state.get('diagram') == 2:
        # EKG-Analyse
        #st.plotly_chart(la.plot_ekg(la.activity_data))  # Annahme: es gibt eine entsprechende Funktion

 #Initialisiere die Toggle-Buttons im Session State
if 'toggle_1' not in st.session_state:
    st.session_state.toggle_1 = False
if 'toggle_2' not in st.session_state:
    st.session_state.toggle_2 = False

with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        #App Logo
        st.image('/Users/lukas/Documents/MCI/Software_engineering/HerzAktiv/Logo2.jpeg', width=100)
    with col2:
        # Eine Überschrift der ersten Ebene
        st.markdown('<p class="custom-position1 big-font">HerzAktiv</p>', unsafe_allow_html=True)
    st.write('Webseite zur Visualisierung der Leistungs- und EKG-Daten.')
    # Eine Überschrift der zweiten Ebene
    st.subheader("Versuchsperson auswählen:")

    # Session State wird leer angelegt, solange er noch nicht existiert
    if 'current_user' not in st.session_state:
        st.session_state.current_user = 'None'

    # Legen Sie eine neue Liste mit den Personennamen an indem Sie ihre Funktionen aufrufen
    person_dict = rd.load_person_data()
    person_names = rd.get_person_list(person_dict)

    st.session_state.current_user = st.radio(
        'Versuchsperson',
        options = person_names, key="sbVersuchsperson", on_change = callback_function)
    
    #st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)

    #st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    
    # Checkbox als Toggle-Button für die erste Option
    Leistungs_button = st.toggle('Leistungs-Analyse', value=st.session_state.toggle_1, key='toggle_1', on_change=update_toggles, args=('toggle_1',))

    # Checkbox als Toggle-Button für die zweite Option
    EKG_button = st.toggle('EKG-Analyse', value=st.session_state.toggle_2, key='toggle_2', on_change=update_toggles, args=('toggle_2',))

            


col1, col2 = st.columns([1,2]) 
# Eine Überschrift der ersten Ebene
if st.session_state.get('diagram') == 1:
    st.markdown('<p class="custom-position2 custom-font">Leistungsdaten</p>', unsafe_allow_html=True)
elif st.session_state.get('diagram') == 2:
    st.markdown('<p class="custom-position2 custom-font">EKG-Daten</p>', unsafe_allow_html=True)
elif st.session_state.get('diagram') == None:
    st.markdown('<p class="custom-position2 custom-font">HerzAktiv <3</p>', unsafe_allow_html=True)

with col1:
    # Anlegen des Session State. Bild, wenn es kein Bild gibt
    if 'picture_path' not in st.session_state:
        st.session_state.picture_path = 'data/pictures/none.jpg'

    # Suche den Pfad zum Bild, aber nur wenn der Name bekannt ist
    if st.session_state.current_user in person_names:
        st.session_state.picture_path = rd.find_person_data_by_name(st.session_state.current_user)['picture_path']

    # Öffne das Bild und Zeige es an
    image = Image.open("/Users/lukas/Documents/MCI/Software_engineering/HerzAktiv/" + st.session_state.picture_path)
    st.image(image, caption=st.session_state.current_user + '(' + str(rd.find_age(st.session_state.current_user)) + ')')

with col2:
    show_data()


if 'diagram' not in st.session_state:
    st.session_state.diagram = None

# Rufe show_diagram am Ende des Skripts auf
if 'diagram' in st.session_state:
    try:
        show_diagram()
        # Dein Code, der das Diagramm erzeugt
        #st.plotly_chart(la.plot_leistung_herzfrequenz(la.activity_data), theme = 'streamlit', use_container_width=True)
    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {e}")
        st.text('Fehler-Traceback:')
        st.text(traceback.format_exc())