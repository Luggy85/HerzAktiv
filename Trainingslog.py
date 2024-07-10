import pandas as pd
import streamlit as st
import json
from datetime import datetime
import plotly.express as px
import os

class CSVUploader:
    
    def read_csv_file(self, file_path):
        """Liest eine CSV-Datei sicher ein und erstellt sie bei Bedarf."""
        if not os.path.exists(file_path):
            # Erstellt eine leere CSV-Datei mit Spaltenköpfen, wenn sie nicht existiert
            df = pd.DataFrame(columns=['ID', 'Name', 'Alter', 'Trainingsart', 'Datum', 'Gewicht', 'Größe', 'Datei'])
            df.to_csv(file_path, index=False)
            st.info("Eine neue Trainingslog-Datei wurde erstellt.")
            return df
        else:
            try:
                df = pd.read_csv(file_path)
                if df.empty:
                    st.warning("CSV-Datei ist leer.")
                return df
            except pd.errors.EmptyDataError:
                st.error("Die CSV-Datei ist leer und hat keine Spalten zu lesen.")
                return None
            except Exception as e:
                st.error(f"Ein Fehler ist beim Lesen der CSV-Datei aufgetreten: {e}")
                return None
            
    def __init__(self):
        self.result_file_path = "Trainingslog.csv"
        self.check_or_create_csv()

    def check_or_create_csv(self):
        if not os.path.exists(self.result_file_path):
            # Erstellen einer neuen leeren DataFrame mit den notwendigen Spalten
            df = pd.DataFrame(columns=["ID", "Name", "Alter", "Trainingsart", "Datum", "Gewicht", "Größe", "Datei"])
            df.to_csv(self.result_file_path, index=False)
            print("Eine neue Trainingslog-Datei wurde erstellt.")
        else:
            print("Eine existierende Trainingslog-Datei wird verwendet.")

    def reset_session_state(self):
        st.session_state['data_saved'] = False
        st.session_state['json_data'] = None
        st.session_state['file_name'] = None
        st.session_state['file_uploaded'] = False
        st.session_state['new_data'] = None

    def upload_file(self):
        uploaded_file = st.file_uploader("Wähle eine JSON Datei", type="json")
        if uploaded_file is not None:
            # Prüfe auf Duplikate, bevor du versuchst, die Datei zu laden
            if self.is_duplicate_file(uploaded_file.name):
                st.error("Diese Datei wurde bereits verwendet.")
                return None, None
            
            self.reset_session_state()

            # Stellen Sie sicher, dass die JSON-Datei korrekt gelesen und geparst wird
            try:
                self.json_data = json.load(uploaded_file)
                st.session_state['json_data'] = self.json_data
                st.session_state['file_name'] = uploaded_file.name
                st.session_state['file_uploaded'] = True
                st.info("Hochgeladene JSON Datei wurde erfolgreich verarbeitet.")
                return self.json_data, uploaded_file.name
            except json.JSONDecodeError as e:
                st.error(f"Fehler beim Lesen der JSON-Datei: {e}")
                return None, None
        return None, None

    def is_duplicate_file(self, file_name):
        result_file_path = "Trainingslog.csv"
        if os.path.exists(result_file_path):
            try:
                existing_df = pd.read_csv(result_file_path, on_bad_lines='skip')
                if file_name in existing_df['Datei'].values:
                    return True
            except pd.errors.EmptyDataError:
                st.warning("CSV-Datei ist leer. Es wird kein Duplikat erkannt.")
            except Exception as e:
                st.error(f"Fehler beim Lesen der CSV-Datei: {e}")
        return False

    def is_duplicate_id(self, person_id, name):
        result_file_path = "Trainingslog.csv"
        if os.path.exists(result_file_path):
            existing_df = pd.read_csv(result_file_path, on_bad_lines='skip')
            if person_id in existing_df['ID'].values and name != existing_df[existing_df['ID'] == person_id]['Name'].values[0]:
                return True
        return False

    def add_person_data(self, person_id, name, age, training_type, weight=None, height=None):
        training_date = None
        if self.json_data:
            first_workout = self.json_data['data']['workouts'][0]
            training_date = datetime.strptime(first_workout['start'], "%Y-%m-%d %I:%M:%S %p %z").date()

        new_data = {
            "ID": person_id,
            "Name": name,
            "Alter": age,
            "Trainingsart": training_type,
            "Datum": training_date,
            "Gewicht": weight,
            "Größe": height,
            "Datei": st.session_state['file_name']
        }
        st.session_state['new_data'] = new_data
        return new_data

def save_data(self, new_data):
    if os.path.exists(self.result_file_path):
        existing_df = pd.read_csv(self.result_file_path)
        final_df = pd.concat([existing_df, pd.DataFrame([new_data])], ignore_index=True)
    else:
        final_df = pd.DataFrame([new_data])
    
    final_df.to_csv(self.result_file_path, index=False)
    print(f"Daten wurden erfolgreich in {self.result_file_path} gespeichert")

    def is_duplicate_id(self, person_id, name):
        result_file_path = "Trainingslog.csv"
        if os.path.exists(result_file_path) and os.path.getsize(result_file_path) > 0:
            try:
                existing_df = pd.read_csv(result_file_path, on_bad_lines='skip')
                if person_id in existing_df['ID'].values and name != existing_df.loc[existing_df['ID'] == person_id, 'Name'].values[0]:
                    return True
            except pd.errors.EmptyDataError:
                st.warning("CSV-Datei ist leer. Es wird kein Duplikat erkannt.")
            except Exception as e:
                st.error(f"Fehler beim Lesen der CSV-Datei: {e}")
        return False

    def display_form(self):
        st.subheader("Zusätzliche Daten eingeben")
        person_id = st.text_input("Person ID (z.B. Geburtsdatum)", key="person_id")
        person_name = st.text_input("Name der Person")
        person_age = st.number_input("Alter der Person", min_value=0, max_value=120,value=None)
        training_type = st.selectbox("Trainingsart", ["Krafttraining", "Ausdauertraining"])
        person_weight = st.number_input("Gewicht der Person (kg) - optional", min_value=0, max_value=300, value=None)
        person_height = st.number_input("Größe der Person (cm) - optional", min_value=0, max_value=250, value=None)

        if st.button("Daten speichern"):
            if not self.is_duplicate_id(person_id, person_name):
                self.add_person_data(person_id, person_name, person_age, training_type, person_weight, person_height)
                st.success('Daten wurden gespeichert und Analyse kann durchgeführt werden.')
            else:
                st.error("Diese ID wurde bereits mit einem anderen Namen verwendet.")

    def analyze_json(self, json_data, additional_data):
        heart_rate_data = []
        durations = []
        calories_burned = []
        steps_data = []
        intensity_data = []

        for workout in json_data['data']['workouts']:
            start_time = datetime.strptime(workout['start'], "%Y-%m-%d %I:%M:%S %p %z")
            end_time = datetime.strptime(workout['end'], "%Y-%m-%d %I:%M:%S %p %z")
            duration = (end_time - start_time).total_seconds() / 60  # Dauer in Minuten
            durations.append(duration)
            
            if 'activeEnergyBurned' in workout:
                calories_burned.append(workout['activeEnergyBurned']['qty'])
            if 'stepCount' in workout:
                steps_data.append(sum([step['qty'] for step in workout['stepCount']]))
            if 'intensity' in workout:
                intensity_data.append(workout['intensity']['qty'])
            
            for hr_data in workout['heartRateData']:
                hr_data['datetime'] = datetime.strptime(hr_data['date'], "%Y-%m-%d %I:%M:%S %p %z")
                heart_rate_data.append(hr_data)

        # In DataFrame umwandeln
        hr_df = pd.DataFrame(heart_rate_data)
        duration_df = pd.DataFrame(durations, columns=['Dauer (Minuten)'])

        # Einige Analysen durchführen
        avg_hr = round(hr_df['Avg'].mean(), 2)
        max_hr = round(hr_df['Max'].max(), 2)
        min_hr = round(hr_df['Min'].min(), 2)
        avg_duration = round(duration_df['Dauer (Minuten)'].mean(), 2)
        total_calories = sum(calories_burned)
        total_steps = sum(steps_data)
        avg_intensity = round(sum(intensity_data) / len(intensity_data), 2) if intensity_data else None

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Durchschnittliche Herzfrequenz:", value=f'{avg_hr} BPM')
            st.metric(label="Maximale Herzfrequenz:", value=f'{max_hr} BPM')
            st.metric(label="Minimale Herzfrequenz:", value=f'{min_hr} BPM')
            st.metric(label="Trainingsdauer:", value=f'{avg_duration} Minuten')
        with col2:
            st.metric(label="Kalorienverbrauch:", value=f'{total_calories} kcal')
            st.metric(label="Schritte:", value=f'{total_steps}')
            if avg_intensity:
                st.metric(label="Durchschnittliche Intensität:", value=f'{avg_intensity} kcal/hr·kg')

        # Daten kombinieren
        combined_data = additional_data.copy()
        combined_data.update({
            "Durchschnittliche Herzfrequenz": avg_hr,
            "Maximale Herzfrequenz": max_hr,
            "Minimale Herzfrequenz": min_hr,
            "Trainingsdauer (Minuten)": avg_duration,
            "Kalorienverbrauch": total_calories,
            "Schritte": total_steps,
            "Durchschnittliche Intensität": avg_intensity,
        })

        # Plotly Visualisierung
        fig = px.line(hr_df, x='datetime', y='Avg', title='Herzfrequenz über die Zeit')
        st.plotly_chart(fig)

        # Ergebnis in DataFrame speichern
        result_file_path = "Trainingslog.csv"
        if os.path.exists(result_file_path):
            existing_df = pd.read_csv(result_file_path, on_bad_lines='skip')
            final_df = pd.concat([existing_df, pd.DataFrame([combined_data])], ignore_index=True)
        else:
            final_df = pd.DataFrame([combined_data])
        
        final_df.to_csv(result_file_path, index=False)
        st.success(f"Analysierte Daten wurden in {result_file_path} gespeichert")

        return final_df

    def get_training_list(self, person_id):
        result_file_path = "Trainingslog.csv"
        if os.path.exists(result_file_path):
            df = pd.read_csv(result_file_path, on_bad_lines='skip')
            return df[df['ID'] == person_id]
        return pd.DataFrame()