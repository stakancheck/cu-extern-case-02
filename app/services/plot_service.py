import plotly.graph_objs as go
import plotly.io as pio
import base64
from flask_babel import gettext as _


def create_weather_plot_wind(dates, wind_speeds):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dates, y=wind_speeds, mode='lines+markers', name='Wind Speed (m/s)'))

    fig.update_layout(xaxis_title=_('Date'), yaxis_title=_('Value, (m/s)'), title='')

    img_bytes = pio.to_image(fig, format='png')
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    return img_base64

def create_weather_plot_temp(dates, temperatures):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dates, y=temperatures, mode='lines+markers', name='Temperature (°C)', line=dict(color='red')))

    fig.update_layout(xaxis_title=_('Date'), yaxis_title=_('Value, (°C)'), title='')

    img_bytes = pio.to_image(fig, format='png')
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    return img_base64