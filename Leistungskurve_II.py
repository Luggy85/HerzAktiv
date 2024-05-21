import pandas as pd
import plotly.graph_objs as go
import numpy as np
from scipy.signal import find_peaks

activity_data = pd.read_csv('data/activity.csv')

Leistungswerte = activity_data['PowerOriginal']
Zeitdauer = activity_data['CumulativeTime'] = activity_data['Duration'].cumsum()
Zeitpunkt = activity_data['Duration']

def leistungskurve(Leistungswerte, Zeitdauer):
    # Leistungskurve berechnen
    Leistungskurve = np.array(Leistungswerte)
    Zeitdauer = np.array(Zeitdauer)
    return Leistungskurve, Zeitdauer

def find_peaks_in_leistungskurve(Leistungskurve, threshold):
    # Peaks in Leistungskurve finden
    peaks, _ = find_peaks(Leistungskurve, threshold)
    
    print(peaks)
    return peaks






if __name__ == '__main__':
    threshold = int(input("Enter the threshold: "))
    find_peaks_in_leistungskurve(Leistungswerte, threshold)