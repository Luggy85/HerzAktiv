import plotly.graph_objects as go
import streamlit as st

def create_bmi_chart(bmi):
    # Definieren der Segmente und Farben
    ranges = [0, 18.5, 25, 30, 35, 40]
    colors = ['blue', 'green', 'yellow', 'orange', 'red']
    labels = ['Underweight', 'Normal', 'Overweight', 'Obese', 'Extremely Obese']
    
    # Berechnen des Winkels für den Zeiger
    angle = 140 - (bmi - ranges[0]) * 280 / (ranges[-1] - ranges[0])
    
    fig = go.Figure()

    # Hinzufügen der farbigen Segmente
    for i in range(len(ranges) - 1):
        fig.add_trace(go.Scatterpolar(
            r=[0, 1, 1, 0],
            theta=[140 - ranges[i] * 280 / ranges[-1], 140 - ranges[i] * 280 / ranges[-1],
                   140 - ranges[i + 1] * 280 / ranges[-1], 140 - ranges[i + 1] * 280 / ranges[-1]],
            fill='toself',
            fillcolor=colors[i],
            line=dict(color='rgba(0,0,0,0)'),
            opacity=0.5,
            name=labels[i]
        ))

    # Zeiger hinzufügen
    fig.add_trace(go.Scatterpolar(
        r=[0, 1],
        theta=[0, angle],
        mode='lines',
        line=dict(color='black', width=4),
        name='BMI'
    ))

    # Layout-Einstellungen
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 1]),
            angularaxis=dict(visible=False)
        ),
        showlegend=True,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig

def calculate_bmi(weight, height):
    """Berechnet den Body-Mass-Index (BMI).

    Args:
        weight (float): Gewicht in Kilogramm.
        height (float): Größe in Metern.

    Returns:
        float: Der berechnete BMI.
        str: Die BMI-Kategorie.
    """
    if height <= 0:
        raise ValueError("Die Höhe muss größer als 0 sein.")
    if weight <= 0:
        raise ValueError("Das Gewicht muss größer als 0 sein.")

    bmi = round(weight / (height ** 2), 2)

    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obesity"

    return bmi, category