# EKGAnalyzer.py
import pandas as pd
import plotly.graph_objs as go
from scipy.signal import find_peaks
import numpy as np
import json

class EKGAnalyzer:
    def __init__(self):
        pass

    @staticmethod
    def load_person_data(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error reading JSON file: {e}")
            raise e

    @staticmethod
    def load_ekg_data(file_path):
        """
        Lädt die EKG-Daten aus einer Datei.

        :param file_path: Pfad zur EKG-Datendatei
        :return: Pandas DataFrame mit den EKG-Daten
        """
        return pd.read_csv(file_path, delimiter='\t', header=None)

    @staticmethod
    def detect_peaks(data, height=None, distance=None):
        """
        Identifiziert Peaks in den EKG-Daten.

        :param data: EKG-Daten
        :param height: Mindesthöhe der Peaks
        :param distance: Mindestabstand zwischen Peaks
        :return: Indizes der Peaks
        """
        peaks, _ = find_peaks(data, height=340, distance=distance)
        return peaks

    @staticmethod
    def calculate_heart_rate(peaks, fs=1000):
        """
        Berechnet die mittlere und maximale Herzfrequenz basierend auf den Peaks.

        :param peaks: Indizes der Peaks
        :param fs: Abtastfrequenz (Standard: 1000 Hz)
        :return: Mittlere Herzfrequenz, maximale Herzfrequenz
        """
        peak_times = peaks / fs
        rr_intervals = np.diff(peak_times)
        hr = 600 / rr_intervals
        return np.mean(hr), np.max(hr)

    @staticmethod
    def plot_ekg(data, peaks):
        """
        Erstellt ein Plotly-Diagramm der EKG-Daten und markiert die Peaks.

        :param data: EKG-Daten
        :param peaks: Indizes der Peaks
        :return: Plotly Figure Objekt
        """
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=data, mode='lines', name='EKG Signal'))
        fig.add_trace(go.Scatter(x=peaks, y=data[peaks], mode='markers', name='Peaks'))
        return fig

    def analyze_and_plot_ekg(self, current_user_name, file_path):
        """
        Analysiert und plottet die EKG-Daten für den aktuellen Benutzer.

        :param current_user_name: Name des aktuellen Benutzers
        :param file_path: Pfad zur Datei mit den Personendaten
        :return: Plotly Figure Objekt, mittlere Herzfrequenz, maximale Herzfrequenz, ausgewählte Person
        """
        personen_data = self.load_person_data(file_path)
        selected_person = next(p for p in personen_data if f"{p['firstname']} {p['lastname']}" == current_user_name)

        ekg_test_dates = [test['date'] for test in selected_person['ekg_tests']]
        selected_ekg_test_date = ekg_test_dates[0]  # Wählen Sie den ersten EKG-Test
        selected_ekg_test = next(test for test in selected_person['ekg_tests'] if test['date'] == selected_ekg_test_date)

        ekg_data = self.load_ekg_data(selected_ekg_test['result_link'])
        ekg_signal = ekg_data[0]
        peaks = self.detect_peaks(ekg_signal)
        mean_hr, max_hr = self.calculate_heart_rate(peaks)

        fig = EKGAnalyzer.plot_ekg(ekg_signal, peaks)

        return fig, mean_hr, max_hr, selected_person
    
if __name__ == "__main__":
    file_path = "data/person_db.json"  # Replace with the desired file path
    current_user_name = "Julian Huber"  # Replace with the desired user name

    analyzer = EKGAnalyzer()
    fig, mean_hr, max_hr, selected_person = analyzer.analyze_and_plot_ekg(current_user_name, file_path)

    print(f"Mittlere Herzfrequenz: {mean_hr:.2f} bpm")
    print(f"Maximale Herzfrequenz: {max_hr:.2f} bpm")
    fig.show()  # Show the plot