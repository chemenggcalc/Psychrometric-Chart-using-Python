import numpy as np
import matplotlib.pyplot as plt
from psychrolib import (
    GetHumRatioFromRelHum, GetSatHumRatio, GetMoistAirEnthalpy, GetTDewPointFromHumRatio,
    GetTWetBulbFromHumRatio, GetMoistAirVolume, SI, SetUnitSystem
)

# Set to SI Units (Celsius, kg/kg, Pa)
SetUnitSystem(SI)

# Define Temperature and Humidity Ratio Ranges
temperature_range = np.linspace(0, 50, 100)  # Dry-bulb temperature range (°C)
humidity_ratio_range = np.linspace(0, 0.01, 30)  # Humidity ratio range (kg/kg dry air)
pressure = 101325  # Atmospheric pressure (Pa)

# Initialize the plot
plt.figure(figsize=(20, 15))

# Plot saturation line (Saturation curve)
sat_hum_ratios = [GetSatHumRatio(t, pressure) for t in temperature_range]
saturation_line, = plt.plot(temperature_range, sat_hum_ratios, color="blue", linewidth=4, label="Saturation Line")

# Plot constant relative humidity lines (10%, 20%, ..., 100%)
relative_humidities = np.linspace(0.1, 1, 10)
for rh in relative_humidities:
    hum_ratios = [GetHumRatioFromRelHum(t, rh, pressure) for t in temperature_range]
    plt.plot(temperature_range, hum_ratios, linestyle="--", color="#32CD32", linewidth=2)
rh_line, = plt.plot([], [], linestyle="--", color="#32CD32", linewidth=2, label="Relative Humidity Lines")

# Plot constant enthalpy lines (10, 20, 30, ..., 100 kJ/kg)
enthalpy_lines = range(10, 250, 15)  # Enthalpy values (kJ/kg)
for h in enthalpy_lines:
    hum_ratios = []
    for t in temperature_range:
        hum_ratio = (h - 1.006 * t) / (2501 + 1.86 * t)
        hum_ratios.append(hum_ratio if hum_ratio > 0 else np.nan)
    plt.plot(temperature_range, hum_ratios, linestyle="-.", color="#FF4500", linewidth=2)
enthalpy_line, = plt.plot([], [], linestyle="-.", color="#FF4500", linewidth=2, label="Enthalpy Lines")

# Plot constant wet-bulb temperature lines (5, 10, 15, ..., 35°C)
wet_bulb_temps = range(5, 36, 5)  # Wet-bulb temperatures (°C)
for twb in wet_bulb_temps:
    hum_ratios = []
    for t in temperature_range:
        try:
            hum_ratio = GetHumRatioFromRelHum(t, twb / 100.0, pressure)
            hum_ratios.append(hum_ratio)
        except:
            hum_ratios.append(np.nan)
    plt.plot(temperature_range, hum_ratios, linestyle=":", color="#9400D3", linewidth=2)
wb_line, = plt.plot([], [], linestyle=":", color="#9400D3", linewidth=2, label="Wet-Bulb Lines")

# Plot constant specific volume lines (0.75, 1.0, 1.25, ..., 1.5 m³/kg)
specific_volumes = np.linspace(0.75, 25, 20)  # Specific volumes (m³/kg)
for vol in specific_volumes:
    hum_ratios = [vol / (t + 273.15) for t in temperature_range]  # Approximation for visualization
    plt.plot(temperature_range, hum_ratios, linestyle="-", color="#FFA500", linewidth=2)
specific_vol_line, = plt.plot([], [], linestyle="-", color="#FFA500", linewidth=2, label="Specific Volume Lines")

# Add dry-bulb and humidity ratio grid lines (orthogonal)
for t in temperature_range:
    plt.axvline(t, color="gray", linestyle="--", linewidth=1, alpha=0.5)
for hr in np.linspace(humidity_ratio_range[0], humidity_ratio_range[1], 10):
    plt.axhline(hr, color="gray", linestyle=":", linewidth=1, alpha=0.5)

# Add the title inside the plot
plt.text(15, 0.075, "Psychrometric Chart", fontsize=50, ha="center", color="black", weight="bold")

# Labels and Axes
plt.xlabel("Dry-Bulb Temperature (°C)", fontsize=20, weight="bold")
plt.ylabel("Humidity Ratio (kg water / kg dry air)", fontsize=20, weight="bold")

# Add a custom legend
plt.legend(
    loc="center left", fontsize=18, frameon=True, shadow=True, fancybox=True
)

# Grid customization
plt.grid(True, which='both', linestyle="--", linewidth=1.5, alpha=0.7)

# Show the plot
plt.show()
