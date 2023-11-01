import streamlit as sl

sl.title('My Parents New Healthy Diner')

sl.header('Breakfast Menu')
sl.text('🥣 Omega 3 & Blueberry Oatmeal')
sl.text('🥗 Kale, Spinach & Rocket Smoothie')
sl.text('🐔 Hard-Boiled Free-Range Egg')
sl.text('🥑🍞 Avocado Toast')

sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas as pd
my_fruit_list as mFruitL = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
mFruitL = mFruitL.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include
sl.multiselect("Pick some fruits:", list(mFruitL.index))

# Display the table on the page
sl.dataframe(mFruitL)
