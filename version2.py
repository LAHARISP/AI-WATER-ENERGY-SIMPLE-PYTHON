
# ==============================================================
# AI WATER AND ENERGY WASTE INVESTIGATOR
# Version 2: Improved Rule-Based Resource Monitoring
# ==============================================================
from datetime import datetime
# --------------------------------------------------------------
# 1. RESOURCE CONFIGURATION
# --------------------------------------------------------------
RESOURCES = {
    "water": {
        "name": "Water",
        "unit": "litres/day",
        "threshold": 20,
        "critical_threshold": 75
    },

    "electricity": {
        "name": "Electricity",
        "unit": "kWh/day",
        "threshold": 20,
        "critical_threshold": 75
    }
}

# --------------------------------------------------------------
# 2. SAMPLE HISTORICAL DATA
# --------------------------------------------------------------

RESOURCE_DATA = {
    "water": {
        "usage": [1200, 1250, 1180, 1220, 1270, 1240, 2100],
        "occupancy": [80, 82, 79, 81, 83, 80, 81],
        "operating_hours": None
    },

    "electricity": {
        "usage": [200, 210, 205, 215, 208, 212, 340],
        "occupancy": [80, 82, 79, 81, 83, 80, 81],
        "operating_hours": [10, 10, 11, 10, 10, 11, 18]
    }
}
# --------------------------------------------------------------
# 3. INPUT VALIDATION
# --------------------------------------------------------------
def get_positive_number(message):
    while True:
        try:
            value = float(input(message))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue

            return value

        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def get_menu_choice():
    while True:
        print("\nChoose an option:")
        print("1. Analyse water consumption")
        print("2. Analyse electricity consumption")
        print("3. Analyse both resources")
        print("4. Enter a new reading")
        print("5. View historical readings")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice in ["1", "2", "3", "4", "5", "6"]:
            return choice

        print("Invalid choice. Please select 1 to 6.")

# --------------------------------------------------------------
# 4. CALCULATE HISTORICAL BASELINE
# --------------------------------------------------------------

def calculate_baseline(readings):
    if len(readings) < 2:
        raise ValueError(
            "At least two readings are required."
        )

    # The last reading is treated as the latest observation.
    historical_readings = readings[:-1]

    average = sum(historical_readings) / len(historical_readings)

    return average
# --------------------------------------------------------------
# 5. CALCULATE PERCENTAGE CHANGE
# --------------------------------------------------------------

def calculate_percentage_change(expected, actual):
    if expected <= 0:
        return 0.0

    change = ((actual - expected) / expected) * 100

    return change
# --------------------------------------------------------------
# 6. ANALYSE CONSUMPTION TREND
# --------------------------------------------------------------
def analyse_trend(readings):

    if len(readings) < 3:
        return "Insufficient data"

    previous_readings = readings[:-1]

    previous_average = (
        sum(previous_readings) / len(previous_readings)
    )

    latest_reading = readings[-1]

    change = calculate_percentage_change(
        previous_average,
        latest_reading
    )

    if change > 5:
        return "Increasing"

    elif change < -5:
        return "Decreasing"

    else:
        return "Stable"
# --------------------------------------------------------------
# 7. DETECT ANOMALIES
# --------------------------------------------------------------
def detect_anomaly(expected, actual, threshold):

    percentage_change = calculate_percentage_change(
        expected,
        actual
    )
    anomaly_detected = percentage_change > threshold

    return percentage_change, anomaly_detected
# --------------------------------------------------------------
# 8. CLASSIFY SEVERITY
# --------------------------------------------------------------
def classify_severity(percentage_change, threshold, critical_threshold):

    if percentage_change <= threshold:
        return "NORMAL"

    elif percentage_change < 40:
        return "MODERATE"

    elif percentage_change < critical_threshold:
        return "HIGH"

    else:
        return "CRITICAL"
# --------------------------------------------------------------
# 9. INVESTIGATE POSSIBLE CAUSES
# --------------------------------------------------------------

def investigate_cause(
    resource,
    percentage_change,
    occupancy_change,
    operating_hours_change
):

    possible_causes = []
    recommendations = []

    # Investigate occupancy changes.
    if occupancy_change is not None and occupancy_change > 10:

        possible_causes.append(
            "Occupancy increased significantly."
        )

        recommendations.append(
            "Check whether additional residents or visitors "
            "explain the increased consumption."
        )

    # Investigate equipment operating hours.
    if (
        operating_hours_change is not None
        and operating_hours_change > 15
    ):

        possible_causes.append(
            "Equipment operating hours increased."
        )

        recommendations.append(
            "Review equipment schedules and operating hours."
        )

    # Water-specific investigation.
    if resource == "water":

        if percentage_change > 40:

            possible_causes.append(
                "Possible water leakage or unusually high usage."
            )

            recommendations.append(
                "Inspect plumbing, taps, toilets, and water meters."
            )

        else:

            possible_causes.append(
                "Increased water use or a change in normal activities."
            )

            recommendations.append(
                "Compare water consumption across different days."
            )

    # Electricity-specific investigation.
    elif resource == "electricity":

        if percentage_change > 40:

            possible_causes.append(
                "Unusually high appliance usage or a possible "
                "equipment issue."
            )

            recommendations.append(
                "Inspect high-consumption appliances and verify "
                "their operating schedules."
            )

        else:

            possible_causes.append(
                "Increased electricity demand."
            )

            recommendations.append(
                "Review appliance usage and operating hours."
            )

    # If there is no strong increase, avoid unnecessary alerts.
    if percentage_change <= 20:

        possible_causes = [
            "No significant increase detected."
        ]

        recommendations = [
            "Continue monitoring resource consumption."
        ]

    return possible_causes, recommendations


# --------------------------------------------------------------
# 10. GENERATE RESOURCE INVESTIGATION REPORT
# --------------------------------------------------------------

def analyse_resource(resource):

    config = RESOURCES[resource]
    data = RESOURCE_DATA[resource]

    readings = data["usage"]

    if len(readings) < 2:

        print("Not enough readings to analyse this resource.")
        return

    # Calculate baseline and actual consumption.
    expected = calculate_baseline(readings)

    actual = readings[-1]

    # Detect unusual consumption.
    change, anomaly = detect_anomaly(
        expected,
        actual,
        config["threshold"]
    )

    # Classify severity.
    severity = classify_severity(
        change,
        config["threshold"],
        config["critical_threshold"]
    )

    # Analyse historical trend.
    trend = analyse_trend(readings)

    # Investigate occupancy changes, if available.
    occupancy = data["occupancy"]

    occupancy_change = None

    if len(occupancy) >= 2:

        previous_occupancy = occupancy[-2]
        current_occupancy = occupancy[-1]

        if previous_occupancy > 0:

            occupancy_change = calculate_percentage_change(
                previous_occupancy,
                current_occupancy
            )

    # Investigate equipment operating hours, if available.
    hours = data["operating_hours"]

    operating_hours_change = None

    if hours is not None and len(hours) >= 2:

        previous_hours = hours[-2]
        current_hours = hours[-1]

        if previous_hours > 0:

            operating_hours_change = calculate_percentage_change(
                previous_hours,
                current_hours
            )

    # Generate investigation results.
    causes, recommendations = investigate_cause(
        resource,
        change,
        occupancy_change,
        operating_hours_change
    )

    # Display the report.
    print("\n" + "=" * 65)
    print(f"{config['name'].upper()} INVESTIGATION REPORT")
    print("=" * 65)

    print(
        f"Report generated: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    print(f"\nHistorical readings: {readings[:-1]}")

    print(
        f"Expected consumption: "
        f"{expected:.2f} {config['unit']}"
    )

    print(
        f"Actual consumption:   "
        f"{actual:.2f} {config['unit']}"
    )

    print(
        f"Consumption change:   "
        f"{change:+.2f}%"
    )

    print(f"Consumption trend: {trend}")

    print(f"Severity: {severity}")

    if anomaly:

        print("\nALERT: UNUSUAL CONSUMPTION DETECTED!")

    else:

        print("\nNo significant consumption anomaly detected.")

    print("\nPossible explanations:")

    for cause in causes:
        print(f"- {cause}")

    print("\nRecommended actions:")

    for recommendation in recommendations:
        print(f"- {recommendation}")

    print("\nInvestigation limitations:")
    print(
        "Possible causes are rule-based suggestions, not "
        "confirmed equipment faults or leaks."
    )

    print("=" * 65)

# --------------------------------------------------------------
# 11. ADD A NEW READING
# --------------------------------------------------------------
def add_new_reading():

    print("\nAdd a new consumption reading")

    print("1. Water")
    print("2. Electricity")

    choice = input("Choose resource: ").strip()

    if choice == "1":
        resource = "water"

    elif choice == "2":
        resource = "electricity"

    else:
        print("Invalid resource selection.")
        return

    usage = get_positive_number(
        f"Enter consumption in {RESOURCES[resource]['unit']}: "
    )

    RESOURCE_DATA[resource]["usage"].append(usage)

    # Ask for occupancy so the contextual data remains aligned.
    occupancy = get_positive_number(
        "Enter current occupancy: "
    )

    RESOURCE_DATA[resource]["occupancy"].append(
        int(occupancy)
    )

    # Keep equipment operating hours aligned when available.
    if resource == "electricity":

        hours = get_positive_number(
            "Enter equipment operating hours: "
        )

        RESOURCE_DATA[resource]["operating_hours"].append(
            hours
        )

    print("\nNew reading added successfully.")

    print(
        "Note: This reading is stored in memory and will not "
        "persist after the program exits."
    )
# --------------------------------------------------------------
# 12. VIEW HISTORICAL READINGS
# --------------------------------------------------------------
def view_history():

    print("\n" + "=" * 55)
    print("HISTORICAL RESOURCE READINGS")
    print("=" * 55)

    for resource, data in RESOURCE_DATA.items():
        print(f"\nResource: {RESOURCES[resource]['name']}")
        for day, usage in enumerate(data["usage"], start=1):
            print(
                f"Day {day}: {usage} "
                f"{RESOURCES[resource]['unit']}"
            )
    print("=" * 55)


# --------------------------------------------------------------
# 13. MAIN APPLICATION
# --------------------------------------------------------------
def main():
    print("\n")
    print("*" * 65)
    print(" AI WATER AND ENERGY WASTE INVESTIGATOR")
    print(" Version 2: Rule-Based Monitoring System")
    print("*" * 65)
    while True:
        choice = get_menu_choice()
        if choice == "1":
            analyse_resource("water")
        elif choice == "2":
            analyse_resource("electricity")
        elif choice == "3":
            analyse_resource("water")
            analyse_resource("electricity")
        elif choice == "4":
            add_new_reading()
        elif choice == "5":
            view_history()
        elif choice == "6":
            print("\nThank you for using the investigator.")
            print("Application closed.")
            break

# -------------------------------------------------------------
# 14. PROGRAM ENTRY POINT
# --------------------------------------------------------------
if __name__ == "__main__":
    main()

