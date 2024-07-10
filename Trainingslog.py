import sqlite3
import streamlit as st
import json
from datetime import datetime
import plotly.express as px
import pandas as pd

class DataUploader:
    
    def __init__(self):
        self.db_file_path = "Trainingslog.db"
        self.create_table()

    def create_connection(self):
        """Erstellt eine Verbindung zur SQLite-Datenbank."""
        try:
            conn = sqlite3.connect(self.db_file_path)
            return conn
        except Exception as e:
            st.error(f"Verbindung zur Datenbank konnte nicht hergestellt werden: {e}")

    def create_table(self):
        """Erstellt die Tabelle, wenn sie noch nicht existiert."""
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS training_data (
                    ID TEXT PRIMARY KEY,
                    Name TEXT,
                    Alter INTEGER,
                    Trainingsart TEXT,
                    Datum TEXT,
                    Gewicht REAL,
                    Groesse REAL,
                    Datei TEXT
                )
            ''')
            conn.commit()
        except sqlite3.OperationalError as e:
            st.error(f"Ein Fehler ist aufgetreten: {e}")
        finally:
            conn.close()

    def insert_data(self, data):
        """Fügt neue Trainingsdaten in die Datenbank ein, falls keine Duplikate vorhanden sind."""
        if not self.is_duplicate_id(data['ID']):
            conn = self.create_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO training_data (ID, Name, Alter, Trainingsart, Datum, Gewicht, Groesse, Datei)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (data['ID'], data['Name'], data['Alter'], data['Trainingsart'], data['Datum'],
                  data['Gewicht'], data['Groesse'], data['Datei']))
            conn.commit()
            conn.close()
            return True
        else:
            st.error("Ein Datensatz mit dieser ID existiert bereits.")
            return False

    def is_duplicate_id(self, person_id):
        """Überprüft, ob eine ID bereits in der Datenbank vorhanden ist."""
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ID FROM training_data WHERE ID = ?", (person_id,))
        exists = cursor.fetchone()
        conn.close()
        return exists is not None

    def get_training_list(self, person_id):
        """Holt Trainingsdaten für eine spezifische Person aus der Datenbank."""
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM training_data WHERE ID = ?", (person_id,))
        records = cursor.fetchall()
        conn.close()
        return records

    def analyze_training_data(self, person_id):
        """Führt eine Analyse der Trainingsdaten durch und generiert einen Plot."""
        records = self.get_training_list(person_id)
        if not records:
            st.error("Keine Trainingsdaten gefunden.")
            return

        df = pd.DataFrame(records, columns=['ID', 'Name', 'Alter', 'Trainingsart', 'Datum', 'Gewicht', 'Groesse', 'Datei'])
        fig = px.scatter(df, x='Datum', y='Gewicht', color='Trainingsart', title='Gewicht über Zeit')
        st.plotly_chart(fig)
        
    def upload_file(self):
        """Lädt eine Datei hoch und verarbeitet sie."""
        uploaded_file = st.file_uploader("Wähle eine JSON Datei", type="json")
        if uploaded_file is not None:
            try:
                json_data = json.load(uploaded_file)
                st.session_state['json_data'] = json_data
                st.session_state['file_name'] = uploaded_file.name
                st.session_state['file_uploaded'] = True
                st.info("Hochgeladene JSON Datei wurde erfolgreich verarbeitet.")
                return json_data, uploaded_file.name
            except json.JSONDecodeError as e:
                st.error(f"Fehler beim Lesen der JSON-Datei: {e}")
                return None, None
        return None, None

    def display_form(self):
        """Zeigt ein Formular zur Dateneingabe und speichert die Daten."""
        st.subheader("Zusätzliche Daten eingeben")
        person_id = st.text_input("Person ID (z.B. Geburtsdatum)", key="person_id")
        person_name = st.text_input("Name der Person")
        person_age = st.number_input("Alter der Person", min_value=0, max_value=120)
        training_type = st.selectbox("Trainingsart", ["Krafttraining", "Ausdauertraining"])
        person_weight = st.number_input("Gewicht der Person (kg)", min_value=0, max_value=300)
        person_height = st.number_input("Größe der Person (cm)", min_value=0, max_value=250)

        if st.button("Daten speichern"):
            data = {
                "ID": person_id,
                "Name": person_name,
                "Alter": person_age,
                "Trainingsart": training_type,
                "Datum": datetime.now().strftime("%Y-%m-%d"),
                "Gewicht": person_weight,
                "Groesse": person_height,
                "Datei": st.session_state.get('file_name', 'manual_input')
            }
            if self.insert_data(data):
                st.success('Daten wurden gespeichert und Analyse kann durchgeführt werden.')