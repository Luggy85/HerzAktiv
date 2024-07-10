import plotly.graph_objects as go
import numpy as np

def create_bmi_chart(bmi, category):
    # Definieren der Segmente und Farben
    ranges = [3.4, 4.7, 6.2, 3.6, 2.6]  # Die Größen der Segmente
    colors = ['blue', 'green', 'yellow', 'orange', 'red']
    labels = ['Underweight', 'Normal weight', 'Overweight', 'Obesity', 'Extremely Obese']

    # Winkel für jede BMI-Zone definieren
    zones = {
        'Underweight': (0, 36),
        'Normal weight': (36, 72),
        'Overweight': (72, 108),
        'Obesity': (108, 144),
        'Extremely Obese': (144, 180)
    }

    # Funktion zur Berechnung des Winkels basierend auf der Kategorie
    def category_to_angle(category, bmi):
        angle_start, angle_end = zones[category]
        if category == 'Underweight':
            return np.interp(bmi, [0, 18.5], [angle_start, angle_end])
        elif category == 'Normal weight':
            return np.interp(bmi, [18.5, 25], [angle_start, angle_end])
        elif category == 'Overweight':
            return np.interp(bmi, [25, 30], [angle_start, angle_end])
        elif category == 'Obesity':
            return np.interp(bmi, [30, 35], [angle_start, angle_end])
        elif category == 'Extremely Obese':
            return np.interp(bmi, [35, 40], [angle_start, angle_end])
        return 180

    angle = category_to_angle(category, bmi)

    # Die Segmente als Halbkreis zeichnen
    fig = go.Figure()

    # Halber Donut
    fig.add_trace(go.Pie(
        values=[20.5] + ranges,
        labels=[' '] + labels,
        marker=dict(colors=['rgba(0,0,0,0)'] + colors),
        hole=0.4,
        direction='clockwise',
        rotation=90,  # Rotation auf 90 Grad setzen, um Halbkreis korrekt anzuzeigen
        showlegend=True,
        textinfo='label',
        hoverinfo='label',
        sort=False
    ))

    # Zeiger hinzufügen
    angle_rad = np.radians(175 - angle)  # Anpassung der Winkel für den Zeiger
    x = 0.5 + 0.4 * np.cos(angle_rad)
    y = 0.5 + 0.4 * np.sin(angle_rad)

    fig.add_shape(type="line",
                  x0=0.5, y0=0.5,
                  x1=x, y1=y,
                  line=dict(color="black", width=4))

    fig.add_shape(type="circle",
                  x0=0.48, y0=0.48,
                  x1=0.52, y1=0.52,
                  line=dict(color="black", width=2),
                  fillcolor="black")

    # Layout-Einstellungen
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        showlegend=True,
        legend=dict(
            x=0, y=1,
            traceorder='normal',
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
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
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
    elif 25 <= bmi < 30:
        category = "Overweight"
    elif 30 <= bmi < 35:
        category = "Obesity"
    else:
        category = "Extremely Obese"

    return bmi, category