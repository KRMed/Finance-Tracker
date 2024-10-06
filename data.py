from datetime import datetime


dform = '%m-%d-%Y'
Categories = {"I": "Income", "E": "Expense"}

def get_date(prompt, allow_default=False):
    date=input(prompt)
    if allow_default and not date:
        return datetime.today().strftime(dform)
    try:
        valid_date = datetime.strptime(date,dform)
        return valid_date.strftime(dform)
    except ValueError:
        print("Please enter in mm-dd-yyyy format")
        return get_date(prompt, allow_default)

def get_amount():
    try:
        amount = float(input('Enter amount: '))
        if amount <= 0:
            raise ValueError('Amount must be a positive non-zero value.')
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter the category ('I' for income or 'E' for expense): ").upper()
    if category in Categories:
        return Categories[category]
    else:
        print("Invalid category. Please enter 'I' for income or 'E' for expense")
        return get_category()

def get_description():
    desc = input('List of choices:\n- Food\n- Groceries\n- Housing\n- Shopping\n- Travel\n- Salary\n- Gas\n- Entertainment\n- Online\n- Other\nEnter a description: ')
    valid_desc = ['Food', 'Groceries', 'Housing', 'Shopping', 'Travel', 'Salary', 'Gas', 'Entertainment', 'Online', 'Other']

    if desc in valid_desc:
        return desc
    else:
        print('Please enter a valid description.')
        return get_description()