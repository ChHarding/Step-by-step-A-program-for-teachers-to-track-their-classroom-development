import pandas as pd
from datetime import datetime
from tabulate import tabulate
import matplotlib.pyplot as plt




def load_csv(filepath): #here I load the csv file and parse the dates
    df = pd.read_csv(filepath)
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%b %d, %Y', errors='coerce')
    print(df.head()) #here I check if it loaded correclty
    return df


def add_log_cli(df):
    # Now I am working on the adding a log from an input
    # I do that by first making an empty list to store the categories
    categories = []
    #then I loop through each of the df's categories---UPDATED AFTER FEEDBACK
    categories = list(df['Category'].unique())

    #this below is for the user to select from usinga number that corresponds to the category
    category_list_str = ", ".join(f"{i+1} ({categories[i]})" for i in range(len(categories))) #updated this to show the category names when selecting
    choice = input(f"Select from the following categories: {category_list_str}\nEnter category number: ")
    category = categories[int(choice) - 1]

    #same for the milestone number
    milestone = input("Enter milestone number: ")
    note = input("Enter a note: ")

    #then here I use date time to het the current date
    date_now = datetime.now().strftime('%b %d, %Y')

    #finally I create a dictionary that will become a new row in the dataframe ---ALSO UPDATED AFTER FEEDBACK
    new_row = {
    'Date': date_now,
    'Category': category,
    'Milestone': int(milestone),
    'Note': note,
    'parsed_date': datetime.now() #I brough this back because I was having issues with parsing the Date now
}

    #then I append it to the actual df
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True) #it didnt work with append so I am trying with concat instead
    print("New log added:")
    print(df.tail(1)) #to see if it got added


    return df

def plot_category_progress(df):
    #Below I am asking the user which category they want to plot
    categories = list(df['Category'].unique())
    category_list_str = ", ".join(f"{i+1} ({categories[i]})" for i in range(len(categories)))
    choice = input(f"Pick a category to plot progress for:\n{category_list_str}\nEnter number: ")
    selected_category = categories[int(choice) - 1]

    #Then I filter the df for that category only
    df_cat = df[df['Category'] == selected_category].copy()

    #FInally I convert it in dates as suggested on feedback, since dates might not be in order
    df_cat['parsed_date'] = pd.to_datetime(df_cat['Date'], format='%b %d, %Y', errors='coerce')
    df_cat = df_cat.sort_values('parsed_date')

    print(df_cat[['parsed_date', 'Milestone']])  #Double checking before plotting

    #Now I create the actual plot
    plt.figure(figsize=(10, 5))
    plt.plot(df_cat['parsed_date'], df_cat['Milestone'], marker='o', linestyle='-', color='b')

    #lastly I show it, not sure why I didn't do it before my last commit
    plt.tight_layout()
    plt.show()

def plot_overall_distribution(df):
    #Since this is for all the categories, first I count how many entries there are for each category
    category_counts = df['Category'].value_counts()

    #then I plot a pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title("Overall Log Distribution by Category")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    df = load_csv("data/test_data.csv")
    df = add_log_cli(df)
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
    plot_category_progress(df)
    plot_overall_distribution(df)

