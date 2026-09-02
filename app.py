import math
import pandas as pd
import streamlit as st
from scipy.constants import Planck, c, electron_mass, electron_volt, pico

st.set_page_config(
    page_title="Compton Scattering Calculator", page_icon="🧪", layout="wide"
)


def compton_scattering(wavelength_pm, scatter_angle_deg):
    if wavelength_pm <= 0:
        wavelength_pm = 0.001
    scatter_angle_rad = math.radians(scatter_angle_deg)
    compton_shift_m = (Planck / (electron_mass * c)) * (
        1 - math.cos(scatter_angle_rad)
    )
    compton_shift_pm = compton_shift_m / pico
    scattered_wavelength_pm = wavelength_pm + compton_shift_pm
    energy_loss_fraction = compton_shift_pm / scattered_wavelength_pm
    return scattered_wavelength_pm, compton_shift_pm, energy_loss_fraction


st.title(":green[🧪 Compton Scattering Calculator]")
st.write(
    "This calculator computes the scattered wavelength and energy loss fraction of X-ray photons after Compton scattering based on the incident wavelength and scatter angle."
)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader(":blue[Inputs]")
    x_ray_wl = st.slider(
        "Incident X-ray Wavelength (pm)",
        min_value=1.0,
        max_value=100.0,
        value=22.0,
        step=1.0,
    )
    scatter_angle = st.slider(
        "Scatter Angle (degrees)", min_value=0, max_value=180, value=90, step=5
    )

with col2:
    st.subheader(":red[Calculation Results]")
    incident_energy_kev = (
        Planck * (c / (x_ray_wl * pico)) / electron_volt / 1000
    )
    sc_wl, shift_pm, loss_frac = compton_scattering(x_ray_wl, scatter_angle)

    m1, m2 = st.columns(2)
    m1.metric(label="Incident Energy", value=f"{incident_energy_kev:.2f} keV")
    m2.metric(label="Compton Shift (Δλ)", value=f"{shift_pm:.2f} pm")

    m3, m4 = st.columns(2)
    m3.metric(label="Scattered Wavelength", value=f"{sc_wl:.2f} pm")
    m4.metric(label="Energy Loss", value=f"{loss_frac * 100:.2f} %")

st.subheader("📊 Dynamic Angular Sweep Analysis")
st.write(
    "The chart below tracks how the photon's **Energy Loss (%)** scales continuously from forward scattering (0°) to absolute backscattering (180°) given your current incident wavelength."
)

angles = list(range(0, 181, 1))
chart_data = []

for ang in angles:
    _, _, loop_loss_frac = compton_scattering(x_ray_wl, ang)
    chart_data.append(
        {"Scattering Angle (°)": ang, "Energy Loss (%)": loop_loss_frac * 100}
    )

df = pd.DataFrame(chart_data)
df.set_index("Scattering Angle (°)", inplace=True)
st.line_chart(df, y="Energy Loss (%)", color="#FF4B4B")
