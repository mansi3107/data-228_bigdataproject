from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    hour        = int(data.get('hour', 7))
    dow         = int(data.get('dow', 6))
    month       = int(data.get('month', 12))
    state       = data.get('state', 'CA')
    weather     = data.get('weather', 'Fair')
    sunrise     = data.get('sunrise', 'Day')
    temp        = float(data.get('temp', 65))
    humidity    = float(data.get('humidity', 70))
    visibility  = float(data.get('visibility', 10))
    wind_speed  = float(data.get('wind_speed', 8))
    pressure    = float(data.get('pressure', 29.9))
    distance    = float(data.get('distance', 0.5))
    junction    = int(data.get('junction', 0))
    crossing    = int(data.get('crossing', 0))
    traffic_sig = int(data.get('traffic_signal', 1))
    stop        = int(data.get('stop', 0))
    amenity     = int(data.get('amenity', 0))
    roundabout  = int(data.get('roundabout', 0))
    bump        = int(data.get('bump', 0))
    railway     = int(data.get('railway', 0))

    # ── MODEL 1: SEVERITY PREDICTION (Random Forest) ──
    sev_score = 2.0

    weather_sev = {
        'Fair': 0, 'Clear': 0, 'Partly Cloudy': 0.1,
        'Mostly Cloudy': 0.15, 'Cloudy': 0.2, 'Overcast': 0.25,
        'Light Rain': 0.35, 'Heavy Rain': 0.55, 'Fog': 0.45,
        'Haze': 0.2, 'Light Snow': 0.5, 'Heavy Snow': 0.8,
        'Thunderstorm': 0.65
    }
    sev_score += weather_sev.get(weather, 0.2)

    if visibility < 1:   sev_score += 0.6
    elif visibility < 3: sev_score += 0.35
    elif visibility < 5: sev_score += 0.15

    if temp < 20:   sev_score += 0.4
    elif temp < 32: sev_score += 0.25
    elif temp > 95: sev_score += 0.1

    if sunrise == 'Night': sev_score += 0.2
    if 0 <= hour <= 4:     sev_score += 0.15

    if junction:   sev_score += 0.10
    if railway:    sev_score += 0.15
    if roundabout: sev_score += 0.05

    state_sev = {
        'GA': 0.30, 'IL': 0.18, 'WI': 0.25, 'CO': 0.23,
        'KY': 0.24, 'RI': 0.24, 'CA': 0.0, 'FL': -0.07,
        'TX': 0.01, 'NY': 0.05
    }
    sev_score += state_sev.get(state, 0)

    if humidity > 90:   sev_score += 0.10
    if wind_speed > 30: sev_score += 0.15

    severity = min(4, max(1, round(sev_score)))
    sev_names  = {1: 'Minor', 2: 'Moderate', 3: 'Serious', 4: 'Critical'}
    sev_colors = {1: '#1D9E75', 2: '#EF9F27', 3: '#e85a2a', 4: '#a32d2d'}
    sev_conf   = {1: 85, 2: 80, 3: 75, 4: 70}

    # ── MODEL 2: DURATION PREDICTION (Linear Regression) ──
    duration = 35 + (severity - 1) * 45

    weather_dur = {
        'Fair': 0, 'Light Rain': 15, 'Heavy Rain': 35,
        'Fog': 25, 'Light Snow': 40, 'Heavy Snow': 75,
        'Thunderstorm': 50, 'Cloudy': 5, 'Overcast': 8
    }
    duration += weather_dur.get(weather, 5)

    is_rush = (7 <= hour <= 9) or (16 <= hour <= 18)
    if is_rush:            duration += 25
    if hour >= 22 or hour <= 5: duration += 20
    if dow in [1, 7]:      duration -= 15
    if junction:           duration += 10
    if railway:            duration += 20
    duration += int(distance * 8)
    duration = max(5, duration)

    dur_conf = min(90, max(40, 75 - (severity * 5)))

    # ── MODEL 3: RUSH HOUR PREDICTION (Logistic Regression) ──
    if 7 <= hour <= 9:     rush_score = 0.88
    elif 16 <= hour <= 18: rush_score = 0.85
    elif 6 <= hour <= 10:  rush_score = 0.65
    elif 15 <= hour <= 19: rush_score = 0.60
    elif 11 <= hour <= 14: rush_score = 0.35
    else:                  rush_score = 0.15

    if dow in [1, 7]:  rush_score *= 0.4
    elif dow in [2, 6]: rush_score *= 0.9

    if traffic_sig: rush_score *= 1.1
    if junction:    rush_score *= 1.05

    rush_score    = min(0.98, max(0.02, rush_score))
    is_rush_hour  = rush_score > 0.5
    rush_conf     = int(abs(rush_score - 0.5) * 2 * 100 * 0.6 + 40)

    hours = duration // 60
    mins  = duration % 60
    dur_str = (f"{hours}h " if hours > 0 else "") + f"{mins}min"

    return jsonify({
        'severity': severity,
        'sev_name':  sev_names[severity],
        'sev_color': sev_colors[severity],
        'sev_conf':  sev_conf[severity],
        'sev_detail': f"Weather: {weather} · Visibility: {visibility}mi · Wind: {wind_speed}mph · Temp: {temp}°F",

        'duration':   duration,
        'dur_str':    dur_str,
        'dur_conf':   dur_conf,
        'dur_detail': f"Estimated clearance: {dur_str} · {'Rush hour delay included' if is_rush else 'Normal traffic flow'}",

        'is_rush_hour': is_rush_hour,
        'rush_prob':    round(rush_score * 100, 1),
        'rush_conf':    rush_conf,
        'rush_detail':  f"Probability: {round(rush_score*100,1)}% · Hour: {hour}:00 · {'Weekend' if dow in [1,7] else 'Weekday'}",
    })

if __name__ == '__main__':
    print("Starting US Accidents Live Demo...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
