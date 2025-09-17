from flask import Flask, render_template, request

app = Flask(__name__)

# --- emission factors (kg CO2 per unit) ---
CAR_FACTOR = 0.21   # per km
BUS_FACTOR = 0.10   # per km
ELECTRICITY_FACTOR = 0.82  # per kWh
DIET_FACTORS = {
    "vegetarian": 1.7,
    "mixed": 2.5,
    "heavy_meat": 3.5
}

AVERAGE_FOOTPRINT = 6.0  # average daily footprint in kg CO2 for comparison

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        car_km = float(request.form.get("car_km", 0))
        bus_km = float(request.form.get("bus_km", 0))
        electricity = float(request.form.get("electricity", 0))
        diet = request.form.get("diet", "mixed")

        transport_emissions = (car_km * CAR_FACTOR) + (bus_km * BUS_FACTOR)
        electricity_emissions = electricity * ELECTRICITY_FACTOR
        food_emissions = DIET_FACTORS.get(diet, 2.5)

        total = round(transport_emissions + electricity_emissions + food_emissions, 2)

        suggestions = []
        if car_km > 0:
            suggestions.append("🚗 Try carpooling or use public transport more often.")
        if electricity > 3:
            suggestions.append("💡 Reduce usage: switch off appliances and use LED bulbs.")
        if diet == "heavy_meat":
            suggestions.append("🥗 Try adding 1-2 vegetarian meals per week.")
        if total > AVERAGE_FOOTPRINT:
            suggestions.append("🌱 Your footprint is higher than average, small changes can make big impact!")

        badge = "🌟 Eco Star" if total <= AVERAGE_FOOTPRINT else "🌍 Can Improve"

        return render_template("result.html",
                               total=total,
                               transport=transport_emissions,
                               electricity=electricity_emissions,
                               food=food_emissions,
                               suggestions=suggestions,
                               badge=badge,
                               average=AVERAGE_FOOTPRINT)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

