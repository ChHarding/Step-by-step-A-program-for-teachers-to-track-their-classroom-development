import pandas as pd
from datetime import datetime


def load_csv(filepath): #here I load the csv file and parse the dates
    df = pd.read_csv(filepath)
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%b. %d, %Y', errors='coerce')

    print(df.head()) #here I check if it loaded correclty
    return df


def add_log_cli(df):
    # Now I am working on the adding a log from an input
    # I do that by first making an empty list to store the categories
    categories = []
    #then I loop through each of the df's categories
    for cat in df['Category']:
        if cat not in categories: #if its not already in my list then I add it
            categories.append(cat)

#this below is for the user to select from usinga number that corresponds to the category
    category_list_str = ", ".join(f"{i+1} ({categories[i]})" for i in range(len(categories))) #updated this to show the category names when selecting
    choice = input(f"Select from the following categories: {category_list_str}\nEnter category number: ")
    category = categories[int(choice) - 1]

#same for the milestone number
    milestone = input("Enter milestone number: ")
    note = input("Enter a note: ")

#then here I use date time to het the current date
    from datetime import datetime
    date_now = datetime.now().strftime('%b. %d, %Y')

#finally I create a dictionary that will become a new row in the dataframe
    new_row = {
        'Date': date_now,
        'Category': category,
        'Milestone': int(milestone),
        'Note': note,
        'parsed_date': pd.to_datetime(date_now, format='%b. %d, %Y')
    }

#then I append it to the actual df
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True) #it didnt work with append so I am trying with concat instead
    print("New log added:")
    print(df.tail(1)) #to see if it got added


    return df

if __name__ == "__main__":
    df = load_csv("data/test_data.csv")
    df = add_log_cli(df)
    from tabulate import tabulate
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
