import pandas as pd
from datetime import datetime
from tabulate import tabulate
import matplotlib.pyplot as plt




def load_csv(filepath): #here I load the csv file and parse the dates
    df = pd.read_csv(filepath)

    #Updated after feedback B to drop the date column 
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%b %d, %Y', errors='coerce').dt.date
    df.drop(columns=['Date'], inplace=True)

    # Added this so if the flags arent in the csv they dont show up as NaN on the table
    if 'Flag' not in df.columns:
        df['Flag'] = ""
    else:
        df['Flag'] = df['Flag'].fillna("")

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

    #Here I added a warning if the milestone is not higher than the current max in that category --For now its simple CLI but I will try to find a way to make it more "warning" in the version 2
    existing = df[df['Category'] == category]
    if not existing.empty:
        current_max = existing['Milestone'].max()
    if int(milestone) <= current_max:
        print(f"Warning: Milestone {milestone} is not higher than the current max ({current_max}) in '{category}'")

    #And here I make sure the flag column gets populated with the "regression" flags
    flag = "" 
    if not existing.empty and int(milestone) < current_max:
        flag = "regression"

    note = input("Enter a note: ")

    #then here I use date time to het the current date
    date_now = datetime.now().date()

    #finally I create a dictionary that will become a new row in the dataframe ---ALSO UPDATED AFTER FEEDBACK
    new_row = {
    'Category': category,
    'Milestone': int(milestone),
    'Note': note,
    'parsed_date': date_now,
    'Flag': flag #I also wanted to add a flag column so when user inpuuts a lower milestone it flags it on the table
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
    df_cat = df_cat.sort_values('parsed_date')

    print(df_cat[['parsed_date', 'Milestone']])  #Double checking before plotting

    #Now I create the actual plot
    plt.figure(figsize=(10, 5))
    plt.plot(df_cat['parsed_date'], df_cat['Milestone'], marker='o', linestyle='-', color='b')

    #Now I take care of the current category graph, I added a title and labels for the axis
    plt.title(f"Progress in '{selected_category}' Category")
    plt.xlabel("Date")
    plt.ylabel("Milestone")

    #As suggested on the feedback video, I added some simple math in this case is an overall average for each category 
    average = df_cat['Milestone'].mean()
    plt.axhline(average, color='gray', linestyle='--', linewidth=1) #and I tried to make it decently designed with a dashed line and a subtle color
    plt.text(df_cat['parsed_date'].iloc[-1], average, f' Avg: {average:.1f}', color='gray', fontsize=9, va='bottom') #also I used iloc -1 to have the label always at the end of the chart 


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

