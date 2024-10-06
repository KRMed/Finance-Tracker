import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from data import get_category, get_amount, get_date, get_description

class CSV:
    csv_file = 'Finance_data.csv'
    Columns = ['Date', 'Amount', 'Category', 'Description']
    Date_Format = '%m-%d-%Y'

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.csv_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.Columns)
            df.to_csv(cls.csv_file, index=False)

#comment
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            'Date':date,
            'Amount':amount,
            'Category':category,
            'Description':description
        }
        with open(cls.csv_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.Columns)
            writer.writerow(new_entry)
        print('Entry Added')

    @classmethod
    def get_transactions(cls, start_date, end_date, sort_by=None, sort_order='Ascend'):
        df = pd.read_csv(cls.csv_file)
        df['Date'] = pd.to_datetime(df['Date'], format=CSV.Date_Format)
        start_date = datetime.strptime(start_date, CSV.Date_Format)
        end_date = datetime.strptime(end_date, CSV.Date_Format)

        mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print('No transactions found')
        else:
            if sort_by:
                if sort_order == 'Descend':
                    filtered_df = filtered_df.sort_values(by=sort_by, ascending=False)
                else:
                    filtered_df = filtered_df.sort_values(by=sort_by, ascending=True)

            print(f'Transactions from {start_date.strftime(CSV.Date_Format)} to {end_date.strftime(CSV.Date_Format)}')

            print(
                filtered_df.to_string(
                    index=False, formatters={'Date': lambda x: x.strftime(CSV.Date_Format)}
                )
            )

            total_income = filtered_df[filtered_df['Category']=='Income']['Amount'].sum()
            total_expense = filtered_df[filtered_df['Category']=='Expense']['Amount'].sum()
            total_day = end_date-start_date
            if total_day.days <= 0:
                weeks = 1
            else:
                weeks = (total_day.days / 7)
            weekly_expense = (total_expense/weeks)

            print()
            print('Summary: ')
            print(f'Total income: ${total_income:.2f}')
            print(f'Total expense: ${total_expense:.2f}')
            print(f'Net Savings: ${total_income-total_expense:.2f}')
            print(f'Average Weekly Expense: ${weekly_expense:.2f}')
        return filtered_df

    @classmethod
    def get_descriptions(cls, start_date, end_date):
        df = pd.read_csv(cls.csv_file)
        df['Date'] = pd.to_datetime(df['Date'], format=CSV.Date_Format)
        start_date = datetime.strptime(start_date, CSV.Date_Format)
        end_date = datetime.strptime(end_date, CSV.Date_Format)

        mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print('No transactions found')
            return

        expense_df = filtered_df[filtered_df['Category'] == 'Expense']
        description_summary = expense_df.groupby('Description')['Amount'].sum().reset_index()
        sort_description = description_summary.sort_values(by='Amount', ascending=False)

        print(f'Expenses from {start_date.strftime(CSV.Date_Format)} to {end_date.strftime(CSV.Date_Format)}')
        print(
            sort_description.to_string(index=False, formatters={'Amount': '${:,.2f}'.format}
        ))

        return filtered_df


def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (mm-dd-yyyy) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    df.set_index('Date', inplace=True)

    income_df = df[df['Category']=='Income'].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df['Category']=='Expense'].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(8, 4))
    plt.bar(income_df.index, income_df["Amount"], label="Income", color="g")
    plt.bar(expense_df.index, expense_df["Amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_descriptions(df):
    df.set_index('Date', inplace=True)

    categories = [
        'Food', 'Groceries','Housing','Shopping','Online','Travel','Gas','Entertainment','Other'
    ]
    colors = ['g', 'brown', '#40E0D0', 'blue', 'red', 'yellow', 'purple', 'orange', 'gray', 'black']  # Different colors for each category
    amounts = []

    for category in categories:
        category_df = df[df['Description'] == category].resample("D").sum().reindex(df.index, fill_value=0)
        amounts.append(category_df['Amount'].sum())

    plt.figure(figsize=(10, 5))
    wedges, texts, perc = plt.pie(amounts, labels=categories, colors=colors, autopct='%1.1f%%',labeldistance=1.2, pctdistance=1.1, startangle=140)
    plt.setp(texts, fontsize=8)
    plt.setp(perc, fontsize=7)
    plt.text(-2.7, 1.3, "Expense by Description", fontsize=14, fontweight='bold', ha='left')
    plt.tight_layout()
    plt.show()

def main():
    df = pd.DataFrame()
    while True:
        print()
        print('1. Add a new transaction')
        print('2. View transactions and summary')
        print('3. View description percentage and summary')
        print('4. Exit')
        option = input('Enter your choice (1-4):')
        print()

        if option == '1':
            add()

        elif option == '2':
            start_date = get_date('Enter the start date (mm-dd-yyyy): ')
            end_date = get_date('Enter the end date (mm-dd-yyyy): ')
            sort_choice = input('Do you wish to change sorting order, y for yes, n for no? ')
            if sort_choice == 'y':
                sort_by = input('Sort by Date, Amount, or press enter for no sorting: ').strip()
                sort_order = input('Sort by Ascend, Descend, or press enter for no sorting: ').strip()
                sort_order = sort_order if sort_order in ['Ascend', 'Descend'] else 'Ascend'
                df = CSV.get_transactions(start_date, end_date, sort_by if sort_by in ['Date', 'Amount'] else None, sort_order)
            if sort_choice == 'n':
                df = CSV.get_transactions(start_date, end_date)
            if input('Do you want to see a plot, y for yes, n for no? ').lower()=="y":
                plot_transactions(df)
        elif option == '3':
            start_date = get_date('Enter the start date (mm-dd-yyyy): ')
            end_date = get_date('Enter the end date (mm-dd-yyyy): ')
            df = CSV.get_descriptions(start_date, end_date)
            if input('Do you want to see a plot, y for yes, n for no? ').lower() == "y":
                plot_descriptions(df)

        elif option == '4':
            print('Thank you, have a good day!')
            break
        else:
            print('Invalid option, please select an option 1-3.')

if __name__ == "__main__":
    main()



