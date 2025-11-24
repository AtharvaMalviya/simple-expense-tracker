import csv
import os
from datetime import datetime

filename = "expenses.csv"

def initialize_file():
    if not os.path.exists(filename):
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Category", "Description", "Amount"])
        except IOError as e:
            print("Error creating file:", e)

def add_expense():
    print("\n--- Add New Expense ---")
    
    date_input = input("Enter Date (YYYY-MM-DD) or press Enter for today: ")
    if date_input == "":
        date_input = datetime.today().strftime('%Y-%m-%d')
    
    category = input("Enter Category (e.g., Food, Travel): ")
    if category == "":
        category = "Uncategorized"
    
    description = input("Enter Description: ")
    if description == "":
        description = "Misc"
    
    while True:
        try:
            amount_str = input("Enter Amount: ")
            amount = float(amount_str)
            if amount < 0:
                print("Amount cannot be negative.")
            else:
                break 
        except ValueError:
            print("Invalid input. Please enter a number.")

    try:
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([date_input, category, description, amount])
        print("Success! Expense added.")
    except IOError as e:
        print("Error writing to file:", e)

def view_expenses():
    print("\n--- Your Expense History ---")
    
    if not os.path.exists(filename):
        print("No records found.")
        return

    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
            
            if len(data) <= 1:
                print("No expenses recorded yet.")
                return

            rows = data[1:]

            print(f"{'Date':<12} | {'Category':<15} | {'Amount':<10} | {'Description'}")
            print("-" * 60)
            
            for row in rows:
                if len(row) >= 4:
                    d = row[0]
                    c = row[1]
                    desc = row[2]
                    a = row[3]
                    print(f"{d:<12} | {c:<15} | {a:<10} | {desc}")
                    
    except IOError as e:
        print("Error reading file:", e)

def expense_summary():
    print("\n--- Expense Summary ---")
    if not os.path.exists(filename):
        print("No data to analyze.")
        return

    totals = {}
    total_sum = 0.0

    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)

            for row in reader:
                if len(row) < 4:
                    continue 
                
                cat = row[1]
                try:
                    amt = float(row[3])
                except ValueError:
                    continue 

                total_sum += amt
                
                if cat in totals:
                    totals[cat] += amt
                else:
                    totals[cat] = amt

        print(f"Total Spent: Rs {total_sum:.2f}")
        print("\nBreakdown by Category:")
        
        if len(totals) == 0:
            print("No valid data found.")
        else:
            for cat, val in totals.items():
                print(f" - {cat:<15}: Rs {val:.2f}")
                
    except IOError as e:
        print("Error analyzing file:", e)

def main():
    initialize_file()
    
    while True:
        print("\n=== PERSONAL EXPENSE TRACKER ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Summary")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ")
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            expense_summary()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()