import requests


url = "http://127.0.0.1:5000/api/predict"


data = {
    "Discount offered": 0.06,
    "Unit Price": 40.98,
    "Freight Expenses": 2.99,
    "QtyOrdered": 3,

    "Order Year": 2010,
    "Order Month": 1,
    "Order Quarter": 1,
    "Order Day": 2,
    "Order DayOfWeek": 5,

    "Order Priority": "High",
    "Freight Mode": "Regular Air",
    "Segment": "Consumer",
    "Product Type": "Meat/Poultry",
    "Product Sub-Category": "Meat/Poultry",
    "Product Container": "Small Box",
    "State": "California",
    "City": "Los Angeles",
    "Region": "West"
}


response = requests.post(
    url,
    json=data
)


print("Status Code:", response.status_code)
print("\nAPI Response:")
print(response.json())