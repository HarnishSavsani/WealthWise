import json
import os
import datetime
import time

DATA_FILE = "finance_data.json"
INCOME_SOURCES = ["Salary", "Rental", "Investment", "Freelance", "Other"]
EXPENSE_CATEGORIES = ["Food", "Travel", "Housing", "Entertainment", "Utilities", "Other"]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {"income": [], "expenses": []}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def validate_date(date_str):
    if not date_str:
        return datetime.date.today().isoformat()
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except ValueError:
        print("Invalid date format! Use YYYY-MM-DD")
        return None

def add_income(data):
    amount = float(input("Enter income amount: "))
    print("\nIncome Sources:")
    for i, source in enumerate(INCOME_SOURCES, 1):
        print(f"{i}. {source}")
    source = INCOME_SOURCES[int(input("Choose an option: ")) - 1]
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
    date = validate_date(date)
    if not date:
        return
    description = input("Enter description: ")
    data["income"].append({"amount": amount, "source": source, "date": date, "description": description})
    save_data(data)
    print("Income added!")
    time.sleep(1)

def add_expense(data):
    amount = float(input("Enter expense amount: "))
    print("\nExpense Categories:")
    for i, category in enumerate(EXPENSE_CATEGORIES, 1):
        print(f"{i}. {category}")
    category = EXPENSE_CATEGORIES[int(input("Choose an option: ")) - 1]
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
    date = validate_date(date)
    if not date:
        return
    description = input("Enter description: ")
    data["expenses"].append({"amount": amount, "category": category, "date": date, "description": description})
    save_data(data)
    print("Expense added!")
    time.sleep(1)

def show_summary(data):
    total_income = sum(item["amount"] for item in data["income"])
    total_expense = sum(item["amount"] for item in data["expenses"])
    balance = total_income - total_expense
    print(f"\nFinancial Summary:")
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expense: ${total_expense:.2f}")
    print(f"Balance: ${balance:.2f}")
    if total_expense > 0:
        print("\nExpense Weightage by Category:")
        category_totals = {}
        for expense in data["expenses"]:
            category = expense["category"]
            category_totals[category] = category_totals.get(category, 0) + expense["amount"]
        for i, (category, amount) in enumerate(category_totals.items(), 1):
            weightage = (amount / total_expense) * 100
            print(f"{i}. {category}: ${amount:.2f} ({weightage:.2f}%)")
    input("\nPress Enter to continue...")

def edit_transaction(data):
    choice = input("1. Edit Income\n2. Edit Expense\nChoose option (1-2): ")
    if choice == "1":
        transactions = data["income"]
        type_str = "Income"
        fields = ["source", "amount", "date", "description"]
        options = INCOME_SOURCES
    elif choice == "2":
        transactions = data["expenses"]
        type_str = "Expense"
        fields = ["category", "amount", "date", "description"]
        options = EXPENSE_CATEGORIES
    else:
        print("Invalid choice!")
        time.sleep(1)
        return
    if not transactions:
        print(f"No {type_str.lower()} transactions available!")
        time.sleep(1)
        return
    print(f"\n{type_str} Transactions:")
    for i, item in enumerate(transactions, 1):
        print(f"{i}. {item[fields[0]]}: ${item['amount']:.2f}, {item['date']}, {item['description']}")
    index = int(input(f"Enter {type_str.lower()} number to edit: ")) - 1
    if 0 <= index < len(transactions):
        new_data = {}
        new_data["amount"] = float(input("Enter new amount: "))
        print(f"\n{type_str} {fields[0].capitalize()}s:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        new_data[fields[0]] = options[int(input("Choose an option: ")) - 1]
        date = input("Enter new date (YYYY-MM-DD) or press Enter for today: ")
        new_data["date"] = validate_date(date)
        if not new_data["date"]:
            return
        new_data["description"] = input("Enter new description: ")
        transactions[index] = new_data
        save_data(data)
        print(f"{type_str} updated!")
        time.sleep(1)
    else:
        print("Invalid index!")
        time.sleep(1)

def delete_transaction(data):
    choice = input("1. Delete Income\n2. Delete Expense\nChoose option (1-2): ")
    if choice == "1":
        transactions = data["income"]
        type_str = "Income"
        fields = ["source", "amount", "date", "description"]
    elif choice == "2":
        transactions = data["expenses"]
        type_str = "Expense"
        fields = ["category", "amount", "date", "description"]
    else:
        print("Invalid choice!")
        time.sleep(1)
        return
    if not transactions:
        print(f"No {type_str.lower()} transactions available!")
        time.sleep(1)
        return
    print(f"\n{type_str} Transactions:")
    for i, item in enumerate(transactions, 1):
        print(f"{i}. {item[fields[0]]}: ${item['amount']:.2f}, {item['date']}, {item['description']}")
    index = int(input(f"Enter {type_str.lower()} number to delete: ")) - 1
    if 0 <= index < len(transactions):
        transactions.pop(index)
        save_data(data)
        print(f"{type_str} deleted!")
        time.sleep(1)
    else:
        print("Invalid index!")
        time.sleep(1)

def main():
    data = load_data()
    while True:
        print("\n1. Add Income\n2. Add Expense\n3. Show Summary\n4. Edit Transaction\n5. Delete Transaction\n6. Exit")
        choice = input("Choose an option (1-6): ")
        if choice == "1":
            add_income(data)
        elif choice == "2":
            add_expense(data)
        elif choice == "3":
            show_summary(data)
        elif choice == "4":
            edit_transaction(data)
        elif choice == "5":
            delete_transaction(data)
        elif choice == "6":
            print("Goodbye!")
            time.sleep(1)
            break
        else:
            print("Invalid choice!")
            time.sleep(1)

if __name__ == "__main__":
    main()