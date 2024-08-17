import streamlit as st
import requests

BASE_URL = "https://flaskproductservice.azurewebsites.net/"  # Update this if your Flask app runs on a different host/port

def main():
    st.title("Flask Microservice UI with Streamlit")

    # Sidebar navigation
    menu = ["Home", "Login", "Products"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.text("Welcome to the Flask Microservice UI")

    elif choice == "Login":
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            login(username, password)

    elif choice == "Products":
        st.subheader("Products")
        if 'token' in st.session_state:
            get_products()
        else:
            st.text("Please login first")

def login(username, password):
    url = f"{BASE_URL}/auth"
    headers = {"Content-Type": "application/json"}
    data = {"username": username, "password": password}
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        st.success("Authentication successful")
        st.session_state.token = response.cookies.get('token')
    else:
        st.error("Login failed: Invalid username or password")

def get_products():
    url = f"{BASE_URL}/products"
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        products = response.json().get('data', [])
        for product in products:
            st.write(f"**{product['title']}**")
            st.write(f"Price: ${product['price']}")
            st.write(f"Description: {product['description']}")
            st.write("---")
    else:
        st.error("Failed to fetch products")

if __name__ == '__main__':
    main()
