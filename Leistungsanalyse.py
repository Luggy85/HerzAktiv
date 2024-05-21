import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Daten laden
activity_data = pd.read_csv('data/activity.csv')

mittelwert_leistung = round(activity_data['PowerOriginal'].mean(), 3)
maximalwert_leistung = round(activity_data['PowerOriginal'].max(), 3)

def plot_leistung_herzfrequenz(activity_data, max_heartrate):
    # Plot erstellen
    zonen_grenzen = heart_zones(max_heartrate)
    activity_data['CumulativeTime'] = activity_data['Duration'].cumsum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=activity_data['CumulativeTime'], y=activity_data['PowerOriginal'], mode='lines', name='Leistung'))
    fig.add_trace(go.Scatter(x=activity_data['CumulativeTime'], y=activity_data['HeartRate'], mode='lines', name='Herzfrequenz', yaxis='y2'))
    fig.add_hrect(y0=0, y1=zonen_grenzen[0], fillcolor='green', opacity=0.7, layer='below', line_width=0)
    fig.add_hrect(y0=zonen_grenzen[0], y1=zonen_grenzen[1], fillcolor='yellow', opacity=0.7, layer='below', line_width=0)
    fig.add_hrect(y0=zonen_grenzen[1], y1=zonen_grenzen[2], fillcolor='orange', opacity=0.7, layer='below', line_width=0)
    fig.add_hrect(y0=zonen_grenzen[2], y1=zonen_grenzen[3], fillcolor='red', opacity=0.7, layer='below', line_width=0)
    fig.add_hrect(y0=zonen_grenzen[3], y1=400, fillcolor='purple', opacity=0.7, layer='below', line_width=0)

    # Layout anpassen
    fig.update_layout(
        title="Leistung und Herzfrequenz über die Zeit",
        xaxis_title="Zeit (s)",
        yaxis=dict(
            title="Leistung (Watt)",
            side='left'
        ),
        yaxis2=dict(
            title='Herzfrequenz (bpm)',
            side='right',
            overlaying='y',
            matches='y',
            range=[activity_data['HeartRate'].min(), activity_data['HeartRate'].max()]
        ),
        legend=dict(
            orientation="v",
            x=1,
            y=1,
            xanchor="right",
            yanchor="top"
        )
    )

    return fig

def heart_zones(max_heartrate):
    # Herzfrequenzzonen definieren
    zonen_grenzen = [
        0.6 * max_heartrate,
        0.7 * max_heartrate,
        0.8 * max_heartrate,
        0.9 * max_heartrate,
        max_heartrate
    ]
    return zonen_grenzen

def analyze_heart_zones(max_heartrate):
    # Get heart rate zones boundaries
    zonen_grenzen = heart_zones(max_heartrate)
    activity_data = pd.read_csv('data/activity.csv')

    # Assign zones
    activity_data['Zone'] = pd.cut(activity_data['HeartRate'], bins=[0] + zonen_grenzen, labels=["Z1", "Z2", "Z3", "Z4", "Z5"], right=False)

    # Calculate time in each zone
    zeit_in_zonen = activity_data['Zone'].value_counts()

    return zeit_in_zonen

if __name__ == "__main__":
    plot_leistung_herzfrequenz(activity_data).show()
    print("Zeit in den Zonen:")
    #print(zeit_in_zonen)
    max_heartrate = 200
    heart_zones(max_heartrate)
    zeit_in_zonen = analyze_heart_zones(activity_data, max_heartrate)
    #print(activity_data['Zone'])
    
