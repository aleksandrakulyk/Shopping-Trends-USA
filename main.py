import streamlit as st
import plotly.express as px
import pandas as pd

#Add title, selectboxes and subheaders
st.title("USA Shopping Trends vs Gender")
place = st.selectbox("Place: ", ('Ohio', 'New Hampshire', 'South Dakota', 'Wisconsin', 'Rhode Island', 'Mississippi',
                     'Alabama', 'Nebraska', 'Washington', 'West Virginia', 'Oklahoma', 'Indiana', 'Texas', 'Missouri',
                     'Massachusetts', 'Florida', 'Tennessee', 'Utah', 'Alaska', 'Minnesota', 'Pennsylvania', 'Iowa', 'Illinois', 'Georgia', 'Idaho', 'New Mexico', 'Oregon', 'Louisiana', 'Nevada', 'Arizona', 'Connecticut', 'Hawaii', 'North Carolina', 'Maryland', 'California', 'New Jersey', 'Maine', 'Colorado', 'Virginia', 'Montana', 'Michigan', 'Arkansas', 'Delaware', 'Vermont', 'South Carolina', 'North Dakota', 'Kentucky', 'Wyoming', 'Kansas', 'New York'))

gender = st.selectbox("Choose the gender: ", ("Male", "Female"))
category = st.selectbox("Choose the category: ", ("Clothing", "Accessories", "Outerwear", "Footwear"))
analysis = st.selectbox("What would you like to know? ", ("What do they most like to buy?", "Average money spent",
                        "Seasonal shopping", "Payment method", "Size"))

#DataFrames for both genders
df = pd.read_csv("Shopping_trends.csv")
df = df.loc[df["Gender"] == f"{gender}"]
df = df.loc[df["Location"] == f"{place}"]
df_total = pd.read_csv("TotalShoppingBasedOnCategory.csv")
df_total = df_total.loc[df_total["Gender"] == f"{gender}"]
df_trends = pd.read_csv("ShoppingBasedOnLocationAndGender.csv")
df_trends = df_trends.loc[df_trends["Gender"] == f"{gender}"]
df_trends = df_trends.loc[df_trends["Location"] == f"{place}"]

#def IfNothing():
def IfNothing(items, bar):
    if items == 0:
        st.text("Nothing was bought!")
    else:
        st.plotly_chart(bar)

#Analysis
payments = []
items_bought = []
if analysis == "What do they most like to buy?":
    selected_category = df_trends.loc[df_trends["Category"] == f"{category}"].rename(columns={"Category": f"{category}"})
    figure = px.pie(selected_category, names='ItemPurchased', values='TotallyBought', labels={"ItemPurchased": "",
                                                                                 "TotallyBought": ""})
    st.plotly_chart(figure)
elif analysis == "Average money spent":
    average_money = df.loc[df["Category"] == f"{category}"].rename(columns={'Category': f'{category}'})
    output = average_money.groupby(["Item Purchased", "Purchase Amount (USD)"]).sum().reset_index().groupby(
        "Item Purchased").sum()
    fig = px.bar(output, y='Purchase Amount (USD)', text_auto='.2s',
                 labels={'Purchase Amount (USD)': 'Average money spent [USD]', 'Item Purchased': 'Item'})
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig)
elif analysis == 'Seasonal shopping':
    season = st.selectbox("Season: ", ("Summer", "Winter", "Fall", "Spring"))
    df = df.loc[df["Season"] == f"{season}"]
    seasonal_shopping = df.loc[df["Category"] == f"{category}"].rename(columns={'Category': f'{category}'})
    output = seasonal_shopping.groupby(["Item Purchased", "Season"]).sum().reset_index(["Item Purchased", "Season"])
    items_bought = len(output["Item Purchased"])
    seasonal_shopp = px.pie(output, names='Item Purchased').update_traces(textposition='inside')
    IfNothing(items_bought, seasonal_shopp)
elif analysis == "Payment method":
    payment_methods = list(set(df["Payment Method"]))
    for method in payment_methods:
        payments.append(len(df.loc[df["Payment Method"] == f"{method}"]))
    payment_methods_pie = px.pie(df, names=payment_methods, values=payments, labels={f'{payment_methods}': "Method"})
    st.plotly_chart(payment_methods_pie)
elif analysis == "Size":
    size= px.bar(df, x='Size', y='Category', color='Category', labels={"Size": "", 'Category': ""}).update_yaxes(visible=False)
    st.plotly_chart(size)

#The End


