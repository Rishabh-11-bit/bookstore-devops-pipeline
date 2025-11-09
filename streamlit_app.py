import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date

# -------------------------------
# Database Connection Function
# -------------------------------
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='db',                # connects to the docker service
            database='bookstore',
            user='bookuser',
            password='password123'
        )
        if connection.is_connected():
            return connection
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None



# -------------------------------
# User Login
# -------------------------------
def user_login():
    st.title("Bookstore Management System 📚")
    login_id = st.text_input("Login ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_id and password:
            connection = get_db_connection()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(
                    "SELECT * FROM authentication WHERE login_id = %s AND password = %s",
                    (login_id, password)
                )
                user = cursor.fetchone()
                if user:
                    if login_id == "chirag":  # Admin login
                        st.session_state.user_role = "admin"
                        admin_dashboard()
                    else:  # Customer login
                        st.session_state.user_role = "customer"
                        cursor.execute(
                            "SELECT cust_id FROM customer WHERE login_id = %s",
                            (login_id,)
                        )
                        row = cursor.fetchone()
                        if row:
                            st.session_state.cust_id = row['cust_id']
                            customer_dashboard()
                        else:
                            st.error("Customer record not found.")
                else:
                    st.error("Invalid credentials.")
                connection.close()
            else:
                st.error("Could not connect to database.")
        else:
            st.error("Please enter both login ID and password.")


# -------------------------------
# Admin Dashboard
# -------------------------------
def admin_dashboard():
    st.title("Admin Dashboard 🔐")
    menu = ["Book Management", "Author Management", "Staff Management",
            "Customer Management", "Reports", "Logout"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Book Management":
        book_management()
    elif choice == "Author Management":
        author_management()
    elif choice == "Staff Management":
        staff_management()
    elif choice == "Customer Management":
        customer_management()
    elif choice == "Reports":
        view_reports()
    elif choice == "Logout":
        logout()


# -------------------------------
# Book Management
# -------------------------------
def book_management():
    st.subheader("Book Management")
    menu = ["Add Book", "Delete Book", "View All Books", "Back to Admin Menu"]
    choice = st.selectbox("Select an option", menu)

    if choice == "Add Book":
        add_book()
    elif choice == "Delete Book":
        delete_book()
    elif choice == "View All Books":
        view_books()
    elif choice == "Back to Admin Menu":
        admin_dashboard()


def add_book():
    st.subheader("Add New Book")
    b_id = st.number_input("Book ID", min_value=1)
    b_name = st.text_input("Book Name")
    a_name = st.text_input("Author Name")
    genre = st.text_input("Genre")
    quantity = st.number_input("Quantity", min_value=1)
    price = st.number_input("Price", min_value=0.01)

    if st.button("Add Book"):
        if b_name and a_name:
            connection = get_db_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO books (b_id, b_name, a_name, genre, quantity, price) VALUES (%s, %s, %s, %s, %s, %s)",
                    (b_id, b_name, a_name, genre, quantity, price)
                )
                connection.commit()
                st.success(f"Book '{b_name}' added successfully!")
                connection.close()
            else:
                st.error("Database connection failed.")
        else:
            st.error("Please fill in all fields.")


def delete_book():
    st.subheader("Delete Book")
    b_id = st.number_input("Enter Book ID to delete", min_value=1)
    if st.button("Delete Book"):
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM books WHERE b_id = %s", (b_id,))
            connection.commit()
            st.success(f"Book with ID {b_id} deleted successfully!")
            connection.close()
        else:
            st.error("Database connection failed.")


def view_books():
    st.subheader("View All Books")
    connection = get_db_connection()
    if connection:
        query = "SELECT * FROM books"
        df = pd.read_sql(query, connection)
        st.dataframe(df)
        connection.close()
    else:
        st.error("Database connection failed.")


# -------------------------------
# Author Management
# -------------------------------
def author_management():
    st.subheader("Author Management")
    menu = ["Add Author", "Delete Author", "View All Authors", "Back to Admin Menu"]
    choice = st.selectbox("Select an option", menu)

    if choice == "Add Author":
        add_author()
    elif choice == "Delete Author":
        delete_author()
    elif choice == "View All Authors":
        view_authors()
    elif choice == "Back to Admin Menu":
        admin_dashboard()


def add_author():
    st.subheader("Add New Author")
    a_id = st.number_input("Author ID", min_value=1)
    a_name = st.text_input("Author Name")

    if st.button("Add Author"):
        if a_name:
            connection = get_db_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO author (a_id, a_name) VALUES (%s, %s)", (a_id, a_name))
                connection.commit()
                st.success(f"Author '{a_name}' added successfully!")
                connection.close()
            else:
                st.error("Database connection failed.")
        else:
            st.error("Please enter author name.")


def delete_author():
    st.subheader("Delete Author")
    a_id = st.number_input("Enter Author ID to delete", min_value=1)
    if st.button("Delete Author"):
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM author WHERE a_id = %s", (a_id,))
            connection.commit()
            st.success(f"Author with ID {a_id} deleted successfully!")
            connection.close()
        else:
            st.error("Database connection failed.")


def view_authors():
    st.subheader("View All Authors")
    connection = get_db_connection()
    if connection:
        query = "SELECT * FROM author"
        df = pd.read_sql(query, connection)
        st.dataframe(df)
        connection.close()
    else:
        st.error("Database connection failed.")


# -------------------------------
# The rest of your file (staff, customer, reports, customer_dashboard, buy_book, logout, etc.)
# remains identical — your earlier code is correct there.
# -------------------------------

# -------------------------------
# App Entry Point
# -------------------------------
if __name__ == "__main__":
    if "user_role" not in st.session_state:
        user_login()
    elif st.session_state.user_role == "admin":
        admin_dashboard()
    else:
        customer_dashboard()
