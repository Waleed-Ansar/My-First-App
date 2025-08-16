import streamlit as st
import pandas as pd
import os

FILE_NAME = "stock.csv"

def load_stock():
    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)
    else:
        return pd.DataFrame(columns=["Item", "Quantity", "Price"])

def save_stock(stock_df):
    stock_df.to_csv(FILE_NAME, index=False)

if "stock" not in st.session_state:
    st.session_state.stock = load_stock()

if "cart" not in st.session_state:
    st.session_state.cart = []   # empty cart after creating bill for new purchase

st.title("🛒 Super Store Management System")

# Costumer Section
st.header("🛍️ Add Items to Cart")

if not st.session_state.stock.empty:
    selected_item = st.selectbox("Select Item:", st.session_state.stock["Item"].unique())
    item_data = st.session_state.stock.loc[st.session_state.stock["Item"] == selected_item].iloc[0]
    qty = st.number_input(f"Quantity:", min_value=1, max_value=100, step=1)

    if st.button("Add to Cart"):
        total_price = qty * item_data["Price"]
        st.session_state.cart.append([selected_item, qty, item_data["Price"], total_price])
        st.success(f"Added {qty} Kg {selected_item} to cart.")
else:
    st.warning("No stock available! Add items to stock first.")

# Cart Display & Bill Section
if st.session_state.cart:
    st.subheader("🛒 Cart")
    cart_df = pd.DataFrame(st.session_state.cart, columns=["Item", "Quantity", "Price", "Total"])
    st.table(cart_df)
    total_bill = cart_df["Total"].sum()

    if st.button("✅ Create Bill"):
        st.success(f"Bill Created! Total = {total_bill}")

        # save_stock(st.session_state.stock)
        st.session_state.cart = []

st.sidebar.title("📊 Stock Management")

if st.sidebar.button("Show Stock Inquiry"):
    st.sidebar.write(st.session_state.stock)

# Adding Stock Section
if st.sidebar.button("Add Item to Stock"):
    st.session_state.show_add_stock = True
else:
    if "show_add_stock" not in st.session_state:
        st.session_state.show_add_stock = False
if st.session_state.show_add_stock:
    st.header("Add Items to Stock")
    with st.form("add_item_form"):
        item = st.text_input("Item Name:")
        price = st.number_input("Price per Unit:", min_value=0.0, step=50.0)
        add_btn = st.form_submit_button("Add Item")

    if add_btn:
        new_item = {"Item": item,  "Price": price}
        st.session_state.stock = pd.concat([st.session_state.stock, pd.DataFrame([new_item])], ignore_index=True)
        save_stock(st.session_state.stock)
        st.success(f"Added {item} at {price} each!")
        st.session_state.show_add_stock = False


# streamlit run streamlit_store_management.py