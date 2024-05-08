import numpy as np
import pandas as pd
import plotly.graph_objs as go

activity_data = pd.read_csv('data/activity.csv')

mittelwert_leistung = round(activity_data['PowerOriginal'].mean(),3)
maximalwert_leistung = round(activity_data['PowerOriginal'].max(),3)

print(f"Mittelwert der Leistung: {mittelwert_leistung}")
print(f"Maximalwert der Leistung: {maximalwert_leistung}")


def plot_leistung_herzfrequenz(activity_data):
    # Plot erstellen
    activity_data['CumulativeTime'] = activity_data['Duration'].cumsum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=activity_data['CumulativeTime'], y=activity_data['PowerOriginal'], mode='lines', name='Leistung'))
    fig.add_trace(go.Scatter(x=activity_data['CumulativeTime'], y=activity_data['HeartRate'], mode='lines', name='Herzfrequenz', yaxis='y2'))

    # Layout anpassen
    fig.update_layout(
        title="Leistung und Herzfrequenz über die Zeit",
        xaxis_title="Zeit",
        yaxis_title="Leistung",
        yaxis2=dict(
            title="Herzfrequenz",
            overlaying='y',
            side='right'
        )
    )

    return fig

max_herzfrequenz = 200 #float(input("Bitte geben Sie die maximale Herzfrequenz ein: "))

# Herzfrequenzzonen definieren
zonen_grenzen = [
    0.6 * max_herzfrequenz,
    0.7 * max_herzfrequenz,
    0.8 * max_herzfrequenz,
    0.9 * max_herzfrequenz,
    max_herzfrequenz
]

# Zonen zuordnen
activity_data['Zone'] = pd.cut(activity_data['HeartRate'], bins=[0] + zonen_grenzen, labels=["Z1", "Z2", "Z3", "Z4", "Z5"], right=False)

# Zeit in jeder Zone berechnen
zeit_in_zonen = activity_data['Zone'].value_counts()
if __name__ == "__main__":
    plot_leistung_herzfrequenz(activity_data)
    print("Zeit in den Zonen:")
    print(zeit_in_zonen)
    print(zonen_grenzen)
    print(activity_data['Zone'])

