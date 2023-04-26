import pandas as pd
import plotly.express as px
import streamlit as st
import calendar
import plotly.graph_objects as go
from datetime import datetime

st.title("College Budget")

# Load the data
df = pd.read_excel(
    io='College budget1.xlsx',
    sheet_name='Monthly Living Expenses',
    engine='openpyxl',
    skiprows=4,
    usecols='B:D',
    nrows=13,
)

year = st.sidebar.number_input("Enter a year:", value=2023, min_value=1, max_value=9999, step=1)
month = st.sidebar.selectbox("Select a month:", options=range(1,13))


# Display the calendar only on the sidebar
cal = calendar.month(year, month, 2, 3)
st.sidebar.write(f"Calendar for {year}-{month}")
st.sidebar.text(cal)


# Allow the user to enter text
notes = []

# Allow the user to enter text
text_input = st.text_input("Enter Notes to self:")

# Append the text input to the list every time the user enters new text
if text_input:
    notes.append(text_input)

# Display the entered text and the full list of notes
if notes:
    st.write(f"You entered: {notes[-1]}")
    st.write("All notes:")
    for note in notes:
        st.write(note)

# Display the entered text
if text_input:
    st.write(f"You entered: {text_input}")

st.title("Budget Tracker")

print("Check whichever is applicable:")

if st.checkbox("Do you have an allowance?"):
    allowance = st.slider("Enter your allowance:",0,40000)
    st.write(f"Your allowance is {allowance}")

else:
    allowance = 0.0

if st.checkbox("Do you have a salary?"):
    salary=st.slider("Enter your salary:", 0, 100000)
    st.write(f"Your salary is {salary} ")

else:
    salary=0.0

if (salary*12<300000):
    tax=0
elif(salary*12<600000):
    tax=(0.05*salary*12)/12
elif(salary*12<900000):
    tax=(0.1*salary*12 + 15000)/12
elif(salary*12<1200000):
    tax=(0.15*salary*12+45000)/12
elif(salary*12<1500000):
    tax=(0.2*salary*12+90000)/12
else:
    tax=(0.3*salary*12+150000)/12

# Add the calculated tax as an item in the updating table
df = df.append({'Item': 'Tax', 'Amount': tax}, ignore_index=True)



# Create the sidebar for selecting columns to display
if len(df.columns) > 0:
    cols_to_display_options = df.columns
    cols_to_display = st.sidebar.multiselect(
        "Columns:",
        options=["Item","Amount"],
        default=["Item", "Amount"]
    )
    if not set(cols_to_display).issubset(cols_to_display_options):
        st.sidebar.warning("At least one default column does not exist inin the dataframe.")
else:
    st.sidebar.warning("The dataframe doesn't have any columns to display.")
    



# Create the sidebar for selecting items to update
st.sidebar.header("Deselect items that are not applicable:")
items_to_update = st.sidebar.multiselect(
    "Items:",
    options= df["Item"].unique(),
    default=df["Item"].unique()
)


# Allow the user to enter new values for selected items and columns
for item in items_to_update:
    st.sidebar.write(f"Enter new values for {item}:")
    item_row = df.loc[df['Item'] == item]
    for col in cols_to_display:
        if col != "Item":
            old_value = float(item_row[col])
            new_value = st.sidebar.number_input(
                f"{col}:",
                key=f"{item}-{col}",  # add a unique key based on item and col
                value=old_value,
                step=0.01
            )
            if new_value != old_value:
                df.at[item_row.index[0], col] = new_value

# Display the updated table with the selected columns and items
df_filtered = df.loc[df["Item"].isin(items_to_update), cols_to_display]
st.dataframe(df_filtered)



total_amount = df_filtered['Amount'].sum()


# Calculate the remaining budget
if allowance > 0.0:
    remaining_budget = allowance + salary - total_amount
    st.write(f"Remaining budget: {remaining_budget}")
elif salary > 0.0:
    remaining_budget = salary + allowance - total_amount
    st.write(f"Remaining budget: {remaining_budget}")
    

    

            
# Create a bar chart to visualize the data
fig = px.bar(df_filtered, x="Item", y="Amount")
st.plotly_chart(fig)

fig1 = px.pie(df_filtered, values="Amount", names="Item")
st.plotly_chart(fig1)