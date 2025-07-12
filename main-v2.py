import pandas as pd
from datetime import datetime
from tabulate import tabulate
import matplotlib.pyplot as plt
import streamlit as st 



def load_csv(filepath): #here I load the csv file and parse the dates
    df = pd.read_csv(filepath)

    #Updated this if statement because the streamlit would give me an error with the date column. 
    if 'Date' in df.columns:
        df['parsed_date'] = pd.to_datetime(df['Date'], format='%b %d, %Y', errors='coerce').dt.date
        df.drop(columns=['Date'], inplace=True)
    else:
        df['parsed_date'] = pd.to_datetime(df['parsed_date'], errors='coerce').dt.date


    # Added this so if the flags arent in the csv they dont show up as NaN on the table
    if 'Flag' not in df.columns:
        df['Flag'] = ""
    else:
        df['Flag'] = df['Flag'].fillna("")

    print(df.head()) #here I check if it loaded correclty
    return df

    #Now I replace the old CLI input with the Streamlit interface (at the bottom of my code)

#Now I am goign to update this as well so I have the plotting adapted to streamlit. For now I will keep matplotlib but later I will explore with Seaborn 
def plot_category_progress(df): 
    #Below I am asking the user which category they want to plot
    categories = list(df['Category'].unique())
    category_list_str = ", ".join(f"{i+1} ({categories[i]})" for i in range(len(categories)))
    selected_category = st.selectbox("Pick a category to plot progress for:", categories) #here I have updated the input to use streamlit instead of CLI


    #Then I filter the df for that category only
    df_cat = df[df['Category'] == selected_category].copy()

    #FInally I convert it in dates as suggested on feedback, since dates might not be in order
    df_cat = df_cat.sort_values('parsed_date')

    #I added this to check if the df is empty, so if it is I show a message instead of plotting and giving an error
    if df_cat.empty:
        st.info("No data available for this category.")
        return

    st.write(df_cat[['parsed_date', 'Milestone']]) #Same here, I adapted it to streamlit instead of printing it in the CLI

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
    st.pyplot(plt.gcf()) #Replaced plt.show() with st.pyplot to have the plot in the Streamlit page


def plot_overall_distribution(df):
    #Since this is for all the categories, first I count how many entries there are for each category
    category_counts = df['Category'].value_counts()

    #then I plot a pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title("Overall Log Distribution by Category")
    plt.tight_layout()
    st.pyplot(plt.gcf()) #replaced this too with the st.pyplot so it appears in streamlit and not in the CLI window

#replaced older code with streamlit code 
df = load_csv("data/test_data.csv")
st.title("Step by Step: Child Progress Tracker")
st.subheader("Current Data")
st.dataframe(df)
st.subheader("Add New Log Entry") #Fist I add a subheader to prompt the user
#Then I first start by creating my dropdown for the categories the user can select
categories = df['Category'].unique().tolist()
category = st.selectbox("Select a Category", categories)
#and then the "warning" in case they add a new milestone that is lower than the previous one entered
existing = df[df['Category'] == category]
current_max = existing['Milestone'].max() if not existing.empty else -1
st.text(f"Previous milestone: {current_max}")
#And lastly the input for the milestone number
milestone = st.number_input("Enter milestone number", min_value=0, step=1)
#then just like in the CLI version I check if the milestone is lower than the current max
flag = ""
if milestone < current_max:
    flag = "regression"
    st.warning(f"This milestone is lower than the current max ({current_max})")
#I keep going with the note input
note = st.text_input("Add a note")
#and lastly I need a submit button here, and I also print the last entry added 
if st.button("Add Log Entry"):
    new_row = {
        'Category': category,
        'Milestone': int(milestone),
        'Note': note,
        'parsed_date': datetime.now().date(),
        'Flag': flag
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv("data/test_data.csv", index=False) #I have added this line so entries start getting saves and appear on the graph

    st.success("New log entry added!")
    st.dataframe(df.tail(1))
#Now I add another button with a dropdown to actually view the graphs for each category
with st.expander("View Category Graphs", expanded=False):
    plot_category_progress(df)
#Lastly I add the pie chart button
with st.expander("Display Pie Chart for Overall Progress", expanded=False):
    plot_overall_distribution(df)