
# ============================================================
# AI WATER AND ENERGY WASTE INVESTIGATOR
# Version 1: Basic Python
# ============================================================

# 1. HISTORICAL CONSUMPTION DATA

water_usage = [1200, 1250, 1180, 1220, 1270, 1240, 2100]
electricity_usage = [200, 210, 205, 215, 208, 212, 340]

# Water usage is measured in litres per day.
# Electricity usage is measured in kWh per day.


# 2. FUNCTION TO CALCULATE EXPECTED CONSUMPTION

def calculate_expected_usage(usage_history):

    
    historical_readings = usage_history[:-1]
    total_usage = sum(historical_readings)
    number_of_days = len(historical_readings)
    expected_usage = total_usage / number_of_days
    return expected_usage


# 3. FUNCTION TO DETECT UNUSUAL CONSUMPTION

def detect_anomaly(expected_usage, actual_usage):

    if expected_usage == 0:
        return 0, False

    percentage_change = (
        (actual_usage - expected_usage) / expected_usage
    ) * 100

    threshold = 20

    if percentage_change > threshold:
        anomaly_detected = True
    else:
        anomaly_detected = False

    return percentage_change, anomaly_detected


# 4. FUNCTION TO INVESTIGATE POSSIBLE CAUSES

def investigate_cause(resource, percentage_change):

    if percentage_change <= 20:

        return {
            "severity": "Normal",
            "possible_causes": ["No significant increase detected"],
            "recommendation": "Continue monitoring consumption."
        }

    elif percentage_change <= 50:

        if resource == "Water":

            causes = [
                "Increased water usage",
                "Change in occupancy",
                "Possible minor leakage"
            ]

            recommendation = (
                "Check occupancy, inspect taps, and compare "
                "consumption with previous days."
            )

        else:

            causes = [
                "Increased appliance usage",
                "Change in occupancy",
                "Longer equipment operating hours"
            ]

            recommendation = (
                "Check appliance usage and compare operating "
                "hours with previous days."
            )

        severity = "Moderate"

    else:

        if resource == "Water":

            causes = [
                "Possible water leakage",
                "Unusually high water consumption",
                "Faulty water-consuming equipment"
            ]

            recommendation = (
                "Inspect plumbing, check for leaks, and verify "
                "the water meter reading."
            )

        else:

            causes = [
                "Equipment operating longer than usual",
                "Possible equipment malfunction",
                "Unusually high appliance usage"
            ]

            recommendation = (
                "Inspect high-consumption equipment, check "
                "operating schedules, and verify meter readings."
            )

        severity = "High"

    return {
        "severity": severity,
        "possible_causes": causes,
        "recommendation": recommendation
    }


# 5. FUNCTION TO ANALYSE A RESOURCE

def analyse_resource(resource, usage_history, unit):

    print("\n" + "=" * 55)
    print(f"{resource.upper()} CONSUMPTION INVESTIGATION")
    print("=" * 55)

    # Check whether sufficient readings are available
    if len(usage_history) < 2:

        print("Not enough data to analyse consumption.")
        return

    # Get historical expected consumption
    expected_usage = calculate_expected_usage(usage_history)

    # Latest reading represents actual consumption
    actual_usage = usage_history[-1]

    # Calculate percentage change and detect anomaly
    percentage_change, anomaly_detected = detect_anomaly(
        expected_usage,
        actual_usage
    )

    print(f"Historical readings: {usage_history[:-1]}")
    print(f"Expected consumption: {expected_usage:.2f} {unit}")
    print(f"Actual consumption:   {actual_usage:.2f} {unit}")

    print(f"Change in consumption: {percentage_change:.2f}%")

    # Investigate the reading
    investigation = investigate_cause(
        resource,
        percentage_change
    )

    print(f"\nStatus: {investigation['severity']}")

    if anomaly_detected:

        print("\nALERT: Unusual consumption detected!")

        print("\nPossible causes:")

        for cause in investigation["possible_causes"]:
            print(f"- {cause}")

        print("\nRecommended action:")
        print(investigation["recommendation"])

    else:

        print("\nConsumption is within the configured threshold.")

        print("\nRecommended action:")
        print(investigation["recommendation"])

    print("=" * 55)


# 6. MAIN PROGRAM

def main():

    print("\n")
    print("*" * 55)
    print(" AI WATER AND ENERGY WASTE INVESTIGATOR")
    print("*" * 55)

    # Analyse water consumption
    analyse_resource(
        "Water",
        water_usage,
        "litres/day"
    )

    # Analyse electricity consumption
    analyse_resource(
        "Electricity",
        electricity_usage,
        "kWh/day"
    )

    print("\nInvestigation completed.")
    print("Continue monitoring resource consumption regularly.")


# 7. EXECUTE THE PROGRAM

if __name__ == "__main__":
    main()