def check_blood_compatibility(donor, recipient):
    compatible_types = {
        "O-": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
        "O+": ["O+", "A+", "B+", "AB+"],
        "A-": ["A-", "A+", "AB-", "AB+"],
        "A+": ["A+", "AB+"],
        "B-": ["B-", "B+", "AB-", "AB+"],
        "B+": ["B+", "AB+"],
        "AB-": ["AB-", "AB+"],
        "AB+": ["AB+"]
    }
    return recipient in compatible_types.get(donor, [])

recipient = input("Enter a blood type of recipient: ").upper()
donor = input("Enter a blood type of donor: ").upper()
print(check_blood_compatibility(donor, recipient))




def determine_bmi_category(weight, height):
    bmi = weight / (height ** 2)
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

weight = float(input("Enter your weight(kilogramms): "))
height = float(input("Enter yout height(meters): "))
print(determine_bmi_category(weight, height))




def aggregate_state_of_water(temp):
    if temp <= 0:
        return "Solid (Ice)"
    elif 0 < temp < 100:
        return "Liquid"
    else:
        return "Gas (Steam)"

temp = float(input("Enter a temperature "))
print(aggregate_state_of_water(temp))




formula = input("Enter a formula: ").upper()
print(formula.startswith("H"))