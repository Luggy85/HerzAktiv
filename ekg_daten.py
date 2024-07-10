import plotly.graph_objs as go
from scipy.signal import find_peaks
import numpy as np
import json
import streamlit as st

class EKGAnalyzer:
    def __init__(self, fs=500, noise_threshold=0.001):  # Annahme: 2 ms zwischen den Messungen entspricht 500 Hz
        self.fs = fs
        self.noise_threshold = noise_threshold

    @staticmethod
    def load_person_data(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            with open(file_path, 'r') as file:
                content = file.read()
            print("Inhalt der JSON-Datei:")
            print(content)
            raise e
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            raise e

    @staticmethod
    def load_ekg_data(file_path):
        time = []
        data = []
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    values = line.split()
                    if len(values) == 2:
                        data.append(float(values[0]))  # Spannung
                        time.append(float(values[1]))  # Zeit
                except ValueError as e:
                    print(f"Zeile konnte nicht konvertiert werden: {line}")
                    raise e
        # Debug-Ausgaben um sicherzustellen, dass die Daten korrekt geladen wurden
        print(f"Geladene Daten: {data[:10]}")
        print(f"Geladene Zeitstempel: {time[:10]}")
        return time, data

    def detect_peaks(self, data, height=None, distance=None, threshold=None):
        if height is None:
            height = np.mean(data) + self.noise_threshold * np.std(data)
        if distance is None:
            distance = self.fs // 2

        peaks, properties = find_peaks(data, height=height, distance=distance)
        return peaks, properties

    def calculate_heart_rate(self, time, peaks):
        # Die Zeitwerte werden angenommen, dass sie bereits in Sekunden sind
        peak_times = np.array(time)[peaks]
        rr_intervals = np.diff(peak_times)
        print(f"Peak Times (in Sekunden): {peak_times}")
        print(f"RR-Intervalle (in Sekunden): {rr_intervals}")
        
        if len(rr_intervals) == 0:
            return None, None

        hr = 60 / rr_intervals  # Berechnung der Herzrate als Anzahl der Schläge pro Minute
        return np.mean(hr), np.max(hr)

    @staticmethod
    def plot_ekg(time, data, peaks=None):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time, y=data, mode='lines', name='EKG Signal'))
        if peaks is not None:
            fig.add_trace(go.Scatter(x=np.array(time)[peaks], y=np.array(data)[peaks], mode='markers', name='Peaks', marker=dict(color='red')))
        return fig

    def analyze_and_plot_ekg(self, person_name, file_path):
        time, data = self.load_ekg_data(file_path)
        time = [t / 1000 for t in time]  # Umrechnung in Sekunden

        peaks, properties = self.detect_peaks(data)

        # Slider zur Auswahl des Zeitintervalls
        time_min, time_max = st.slider("Zeitraum auswählen", min_value=min(time), max_value=max(time), value=(min(time), max(time)))
        filtered_indices = [i for i, t in enumerate(time) if time_min <= t <= time_max]
        filtered_time = [time[i] for i in filtered_indices]
        filtered_data = [data[i] for i in filtered_indices]

        # Korrektur der Peak-Indizes für das gefilterte Array
        filtered_peaks = [i for i, idx in enumerate(filtered_indices) if idx in peaks and i < len(filtered_time)]

        # Berechnung der Herzfrequenz für die gefilterten Peaks
        if filtered_peaks:
            mean_hr, max_hr = self.calculate_heart_rate(filtered_time, filtered_peaks)
        else:
            mean_hr, max_hr = None, None
            st.write("Keine gültigen Peaks im ausgewählten Zeitintervall gefunden.")

        fig = self.plot_ekg(filtered_time, filtered_data, filtered_peaks)
        return fig, mean_hr, max_hr