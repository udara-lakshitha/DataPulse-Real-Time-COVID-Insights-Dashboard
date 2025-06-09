from flask import Blueprint, render_template, request, jsonify
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

main_blueprint = Blueprint("main", __name__)

# Load the dataset bat once in startup
DATA_PATH = "data/owid-covid-data.csv"
df = pd.read_csv(DATA_PATH, parse_dates=["date"])

# Prepare country list and sort
countries = sorted(df["location"].dropna().unique())

# Filter data by country and period
# This is a helper function
def filter_data(country, period):
    country_data = df[df["location"] == country].copy()
    today = datetime.today()

    if period == "3M":
        start_date = today - timedelta(days = 90)
    if period == "6M":
        start_date = today - timedelta(days = 180)
    if period == "1Y":
        start_date = datetime(today.year, 1, 1)
    if period == "2Y":
        start_date = today - timedelta(days = 730)
    if period == "5Y":
        start_date = today - timedelta(days = 1825)
    else:
        start_date = country_data["date"].min()

    filtered = country_data[country_data["date"] >= start_date]
    return filtered

# Plot and save to the static folder
def plot_data(filtered, country, period):
    plt.figure(figsize = (10, 5))

    plt.plot(filtered["date"], filtered["total_cases"], label = "Total cases", color = "red")
    plt.plot(filtered["date"], filtered["new_cases"], label = "New cases", color = "orange")
    plt.plot(filtered["date"], filtered["total_vaccinations"], label = "Total vaccinations", color = "green")

    plt.title(f"COVID-19 Data for {country} {period}")
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.grid(True)

    filename = f"static/plots/{country}_{period}.png".replace(" ", "")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return "/" + filename

@main_blueprint.route("/")
def index():
    # Default country: Sri Lanka, period: 1Y
    user_country = "Sri Lanka"
    default_period = "1Y"

    filtered = filter_data(user_country, default_period)

    if filtered.empty:
        stats = {
            'date': 'N/A',
            'total_cases': 'N/A',
            'new_cases': 'N/A',
            'total_vaccinations': 'N/A',
            'people_vaccinated_per_hundred': 'N/A'
        }
        plot_url = ""
    else:
        latest = filtered.iloc[-1]
        stats = {
            'date': latest['date'].strftime('%Y-%m-%d'),
            'total_cases': int(latest['total_cases']) if pd.notna(latest['total_cases']) else 0,
            'new_cases': int(latest['new_cases']) if pd.notna(latest['new_cases']) else 0,
            'total_vaccinations': int(latest['total_vaccinations']) if pd.notna(latest['total_vaccinations']) else 0,
            'people_vaccinated_per_hundred': round(latest['people_vaccinated_per_hundred'], 2) if pd.notna(latest['people_vaccinated_per_hundred']) else 0,
        }
        plot_url = plot_data(filtered, user_country, default_period)

    return render_template(
        'index.html',
        countries=countries,
        selected_country=user_country,
        stats=stats,
        plot_url=plot_url
    )

@main_blueprint.route("/update_data", methods = ["POST"])
def update_data():
    data = request.json
    country = data.get('country', 'Sri Lanka')
    period = data.get('period', '1Y')
    
    filtered = filter_data(country, period)
    
    if filtered.empty:
        stats = {
            'date': 'N/A',
            'total_cases': 'N/A',
            'new_cases': 'N/A',
            'total_vaccinations': 'N/A',
            'people_vaccinated_per_hundred': 'N/A'
        }
        plot_url = ''
    else:
        latest = filtered.iloc[-1]
        stats = {
            'date': latest['date'].strftime('%Y-%m-%d'),
            'total_cases': int(latest['total_cases']) if pd.notna(latest['total_cases']) else 0,
            'new_cases': int(latest['new_cases']) if pd.notna(latest['new_cases']) else 0,
            'total_vaccinations': int(latest['total_vaccinations']) if pd.notna(latest['total_vaccinations']) else 0,
            'people_vaccinated_per_hundred': round(latest['people_vaccinated_per_hundred'], 2) if pd.notna(latest['people_vaccinated_per_hundred']) else 0,
        }
        plot_url = plot_data(filtered, country, period)
    
    return jsonify({'stats': stats, 'plot_url': plot_url})