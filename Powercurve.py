import pandas as pd
import plotly.graph_objects as go
import math
import numpy as np

df = pd.read_csv('data/activity.csv', encoding='utf-8',sep = ",", header=0, skiprows=[1])
power_data = df['PowerOriginal'][10:300]
def maxtime_spend_in_power(power_series, power):
    
    
    last_index = 0
    series_list = [0]

    max_power = power_data.max()
    power_data_cut = power_data[power_data>max_power-power]

    for index, value in power_data_cut.items():
        if last_index and last_index == index - 1:
            series_list[-1] += 1
        else:
            series_list.append(1)
        last_index = index

    return max(series_list)

def sort_max_time(resolution):
    # resolution = 1
    data = []
    for p in range(0, power_data.max(), resolution):
        data.append([power_data.max()-p, maxtime_spend_in_power(power_data, p)])
        #print(f"Max time spend in {power_data.max()-p}W: {maxtime_spend_in_power(power_data, p)}")

    df = pd.DataFrame(data, columns=['Leistung', 'Maximale Zeit'])
    return df


def plot_powercurve():
    fig = go.Figure()
    df = sort_max_time(1)
    fig.add_trace(go.Scatter(
        y=df["Leistung"],
        x=df["Maximale Zeit"],
        mode='lines+markers',
        name='Power Curve'
    ))
    fig.update_layout(
        title='Power Curve',
        xaxis_title='Maximale Zeit (s)',
        yaxis_title='Leistung (W)',
        template='plotly_dark'
    )
    return fig

if __name__ == "__main__":
    print(sort_max_time(1))
    print(plot_powercurve())