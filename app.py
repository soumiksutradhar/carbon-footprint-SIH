from flask import Flask, render_template, request

app = Flask(__name__)

# --- emission factors (kg CO2 per unit) ---
CAR_FACTOR = 0.21   # per km
BUS_FACTOR = 0.10   # per km
DIET_FACTORS = {
    "vegetarian": 1.7,
    "mixed": 2.5,
    "heavy_meat": 3.5
}

# --- state-specific electricity emission factors (kg CO2 per kWh) ---
STATE_ELECTRICITY_FACTORS = {
    "Andhra Pradesh": 0.82,
    "Arunachal Pradesh": 0.38,
    "Assam": 0.79,
    "Bihar": 0.90,
    "Chhattisgarh": 0.85,
    "Goa": 0.75,
    "Gujarat": 0.70,
    "Haryana": 0.80,
    "Himachal Pradesh": 0.40,
    "Jharkhand": 0.85,
    "Karnataka": 0.70,
    "Kerala": 0.60,
    "Madhya Pradesh": 0.85,
    "Maharashtra": 0.75,
    "Manipur": 0.50,
    "Meghalaya": 0.40,
    "Mizoram": 0.35,
    "Nagaland": 0.45,
    "Odisha": 0.85,
    "Punjab": 0.78,
    "Rajasthan": 0.70,
    "Sikkim": 0.35,
    "Tamil Nadu": 0.65,
    "Telangana": 0.82,
    "Tripura": 0.55,
    "Uttar Pradesh": 0.85,
    "Uttarakhand": 0.50,
    "West Bengal": 0.75,
    "Andaman and Nicobar Islands": 0.40,
    "Chandigarh": 0.70,
    "Dadra and Nagar Haveli and Daman and Diu": 0.70,
    "Delhi": 0.70,
    "Jammu and Kashmir": 0.45,
    "Ladakh": 0.40,
    "Lakshadweep": 0.35,
    "Puducherry": 0.70
}


AVERAGE_FOOTPRINT = 6.0  # average daily footprint in kg CO2 for comparison

def safe_float(value, default=0.0):	# Convert form input to float, return default if empty or invalid
    try:
    	return float(value)
    except(TypeError, ValueError):
        return default


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        car_km = safe_float(request.form.get("car_km", 0))
        bus_km = safe_float(request.form.get("bus_km", 0))
        electricity = safe_float(request.form.get("electricity", 0))
        diet = request.form.get("diet", "mixed")
        state = request.form.get("state")
        if not state or state not in STATE_ELECTRICITY_FACTORS:
        	error_msg = "Please select a valid state!"
        	return render_template("index.html",error=error_msg,car_km=request.form.get("car_km", ""),bus_km=request.form.get("bus_km", ""),electricity=request.form.get("electricity", ""),diet=request.form.get("diet", "mixed"))
        	
        elec_factor = STATE_ELECTRICITY_FACTORS[state]
        electricity_emissions = electricity * elec_factor
        transport_emissions = (car_km * CAR_FACTOR) + (bus_km * BUS_FACTOR)
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
