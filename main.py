import streamlit as st
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt

def calculate_total_p_a(df):
    # Calculate total 'P' and total 'A' for each ID (excluding the 'name' column)
    total_p = df.iloc[:, 1:].apply(lambda row: (row == "P").sum(), axis=1)
    total_a = df.iloc[:, 1:].apply(lambda row: (row == "A").sum(), axis=1)

    # Add new columns to the dataframe
    df["Total_P"] = total_p
    df["Total_A"] = total_a

    return df

def draw_bar_chart(df):
    x_axis = st.text_input("Enter X-axis column:", key="bar_x")
    y_axis = st.text_input("Enter Y-axis column:", key="bar_y")

    if st.button("Draw Bar Chart"):
        if x_axis and y_axis:
            fig, ax = plt.subplots()
            ax.bar(df[x_axis].astype(str), df[y_axis])
            st.pyplot(fig)

def draw_pie_chart(df):
    labels = st.text_input("Enter Labels column:", key="pie_labels")
    values = st.text_input("Enter Values column:", key="pie_values")

    if st.button("Draw Pie Chart"):
        if labels and values:
            # Handle NaN values
            df = df.dropna(subset=[labels, values])
            
            fig, ax = plt.subplots()
            ax.pie(df[values], labels=df[labels].astype(str), autopct="%1.1f%%")
            st.pyplot(fig)

def draw_line_plot(df):
    x_axis = st.text_input("Enter X-axis column:", key="line_x")
    y_axis = st.text_input("Enter Y-axis column:", key="line_y")

    if st.button("Draw Line Plot"):
        if x_axis and y_axis:
            fig, ax = plt.subplots()
            ax.plot(df[x_axis].astype(str), df[y_axis])
            st.pyplot(fig)

def draw_scatter_plot(df):
    x_axis = st.text_input("Enter X-axis column:", key="scatter_x")
    y_axis = st.text_input("Enter Y-axis column:", key="scatter_y")

    if st.button("Draw Scatter Plot"):
        if x_axis and y_axis:
            fig, ax = plt.subplots()
            ax.scatter(df[x_axis].astype(str), df[y_axis])
            st.pyplot(fig)

# Function to remove empty values
def remove_empty_values(data):
    cleaned_data = data.dropna()
    return cleaned_data

# Function to show duplicate values
def show_duplicate_values(data):
    duplicate_rows = data[data.duplicated()]
    return duplicate_rows

# Function to delete duplicate rows
def delete_duplicate_rows(data):
    cleaned_data = data.drop_duplicates()
    return cleaned_data


# Function to show numeric columns
def show_numeric_columns(data):
    numeric_columns = data.select_dtypes(include='number')
    return numeric_columns

# Function to correct wrong formats
def correct_wrong_formats(data):
    for column in data.columns:
        if data[column].dtype == 'object':
            # Check if the column contains numeric values
            if data[column].str.isnumeric().all():
                try:
                    data[column] = pd.to_numeric(data[column], errors='raise')
                except (ValueError, TypeError):
                    pass  # If conversion to numeric fails, leave the column as is
            else:
                # Check if the column contains date values
                try:
                    data[column] = pd.to_datetime(data[column], errors='raise')
                except ValueError:
                    pass  # If conversion to datetime fails, leave the column as is

    return data

# Function to fill null values in numeric columns with mean
def fill_null_with_mean(data):
    numeric_columns = data.select_dtypes(include='number')

    for column in numeric_columns.columns:
        if data[column].isnull().any():
            mean_value = data[column].mean()
            data[column].fillna(mean_value, inplace=True)

    return data

# Function to create or load user data
def create_or_load_user_data():
    try:
        user_data = pd.read_excel("user_data.xlsx")
    except FileNotFoundError:
        # Create an empty DataFrame if the file doesn't exist
        user_data = pd.DataFrame(columns=["Username", "Password"])
    return user_data

# Function to sign up a new user
def sign_up(username, password):
    user_data = create_or_load_user_data()
    
    # Check if the username already exists
    if username in user_data["Username"].values:
        st.error("Username already exists. Please choose another.")
        return False
    
    # Add the new user to the DataFrame
    new_user = pd.DataFrame({"Username": [username], "Password": [password]})
    user_data = pd.concat([user_data, new_user], ignore_index=True)
    
    # Save the updated user data to the Excel file
    user_data.to_excel("user_data.xlsx", index=False)
    
    st.success("Account created successfully. You can now log in.")
    return True

# Function to authenticate a user during login
def authenticate_user(username, password):
    user_data = create_or_load_user_data()
    
    # Check if the username and password match
    if (username in user_data["Username"].values) and (password == user_data.loc[user_data["Username"] == username, "Password"].values[0]):
        return True
    else:
        return False

# Streamlit UI for sign up
def sign_up_page():
    st.title("Sign Up")
    
    username = st.text_input("Username", key="signup-username")
    password = st.text_input("Password", type="password", key="signup-password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup-confirm-password")
    
    if st.button("Sign Up"):
        if password == confirm_password:
            sign_up_result = sign_up(username, password)
            if sign_up_result:
                st.sidebar.success("Account created successfully. You can now log in.")
        else:
            st.error("Passwords do not match. Please try again.")

# Streamlit UI for login
def login_page():
    st.title("Login")
    
    username = st.text_input("Username", key="login-username")
    password = st.text_input("Password", type="password", key="login-password")
    
    if st.button("Log In"):
        if authenticate_user(username, password):
            st.experimental_set_query_params(logged_in=True)
        else:
            st.error("Invalid username or password. Please try again.")

# Streamlit UI for the welcome page
def welcome_page():
    st.title("Welcome to EMS App")
    st.markdown("You have successfully logged in.")
    
    # Buttons for different Streamlit apps (replace with your app URLs)
    if st.button("Data information", key="app1-button"):
        st.subheader("Data information Section")
        
        st.title("CSV File Analysis App")

    # Upload CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], key="1")

    if uploaded_file is not None:
        # Load CSV data into a Pandas DataFrame
        df = pd.read_csv(uploaded_file)

        # Display the uploaded DataFrame
        st.subheader("Uploaded Data")
        st.write(df)

        # Buttons
        if st.button("Show Information"):
            st.subheader("File Information")

            # Use StringIO to capture info() output
            info_buffer = StringIO()
            df.info(buf=info_buffer)
            info_text = info_buffer.getvalue()
            st.text(info_text)

        if st.button("Show Descriptive Statistics"):
            st.subheader("Descriptive Statistics")
            st.write(df.describe())

        if st.button("Capitalize First Letter of Columns"):
            st.subheader("Columns with Capitalized First Letter")
            df.columns = [col.capitalize() for col in df.columns]
            st.write(df)

        if st.button("Lowercase Column Names"):
            st.subheader("Columns with Lowercase Names")
            df.columns = [col.lower() for col in df.columns]
            st.write(df)

        # Search form
        with st.form("search_form"):
            st.subheader("Search Data")
            column_to_search = st.selectbox("Select Column", df.columns)
            search_value = st.text_input("Enter Search Value:")
            submit_button = st.form_submit_button("Search")

        # Handle form submission
        if submit_button:
            result_df = df[df[column_to_search].astype(str).str.contains(search_value, case=False)]
            st.write(result_df)
    if st.button("Data Cleaning", key="app2-button"):
        
        st.subheader("Data cleaning Section")
        st.title("Data Cleaning App")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], key="2")

    if uploaded_file is not None:
        original_data = pd.read_csv(uploaded_file)

        st.subheader("Original Data")
        st.write(original_data)

        if st.button("Remove Empty Values"):
            cleaned_data = remove_empty_values(original_data)
            st.subheader("Modified Data (Removed Empty Values)")
            st.write(cleaned_data)

        if st.button("Show Duplicate Values"):
            duplicate_rows = show_duplicate_values(original_data)
            st.subheader("Duplicate Rows")
            st.write(duplicate_rows)

        if st.button("Delete Duplicate Rows"):
            cleaned_data = delete_duplicate_rows(original_data)
            st.subheader("Modified Data (Removed Duplicate Rows)")
            st.write(cleaned_data)

        if st.button("Correct Wrong Formats"):
            cleaned_data = correct_wrong_formats(original_data)
            st.subheader("Modified Data (Corrected Formats)")
            st.write(cleaned_data)

        if st.button("Show Numeric Columns"):
            numeric_columns = show_numeric_columns(original_data)
            st.subheader("Numeric Columns Only")
            st.write(numeric_columns)

        if st.button("Replace Null with Mean"):
            original_data = fill_null_with_mean(original_data)
            st.subheader("Modified Data (Replaced Null with Mean)")
            st.write(original_data)
        
        
    if st.button("Data Visualization", key="app3-button"):
        st.subheader("Data Visualization Section")
        st.title("Visualization Model Streamlit App")

    # Upload CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="3")

    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

        # Display the DataFrame
        st.dataframe(df)

        # Buttons for different chart types
        chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart", "Line Plot", "Scatter Plot"])

        if chart_type == "Bar Chart":
            draw_bar_chart(df)
        elif chart_type == "Pie Chart":
            draw_pie_chart(df)
        elif chart_type == "Line Plot":
            draw_line_plot(df)
        elif chart_type == "Scatter Plot":
            draw_scatter_plot(df)
    if st.button("Attendence sheet analysis", key="app4-button"):
        st.subheader("Attendence sheet analyser")
        st.title("Attendance Management App")

    # File upload
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], key="4")

    if uploaded_file is not None:
        # Read CSV file
        df = pd.read_csv(uploaded_file)

        # Display data
        st.subheader("Attendance Data")
        st.write(df)

        # Count present and absent for each day (sum across rows)
        present_counts = (df.iloc[:, 1:] == "P").sum(axis=0)
        absent_counts = (df.iloc[:, 1:] == "A").sum(axis=0)

         # Show specific attendance by ID
        staff_id = st.text_input("Enter Staff ID:")
        if st.button("Show Attendance"):
            if staff_id:
                specific_attendance = df[df["ID"] == int(staff_id)]
                st.subheader(f"Attendance for Staff ID: {staff_id}")
                st.write(specific_attendance)
            else:
                st.warning("Please enter a valid Staff ID.")

        # Calculate total 'P' and total 'A' for each ID
        if st.button("Calculate Total Present and Absent for Each ID"):
            df_with_totals = calculate_total_p_a(df)
            st.subheader("Attendance Totals for Each ID")
            st.write(df_with_totals[["name", "Total_P", "Total_A"]])

        st.subheader("Attendance Counts")
        st.write("Present counts for each day:")
        st.write(present_counts)
        st.write("Absent counts for each day:")
        st.write(absent_counts)

        # Calculate percentage for each day
        total_records = len(df)
        attendance_percentages = (present_counts / total_records) * 100

        st.subheader("Attendance Percentages for Each Day")
        st.write(attendance_percentages)
        
            

# Choose between sign up, login, and welcome pages
logged_in = st.experimental_get_query_params().get("logged_in", [False])[0]

if not logged_in:
    sign_up_page()
    login_page()
else:
    welcome_page()
