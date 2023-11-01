import streamlit as sl

sl.title('My Parents New Healthy Diner')

sl.header('Breakfast Menu')
sl.text('🥣 Omega 3 & Blueberry Oatmeal')
sl.text('🥗 Kale, Spinach & Rocket Smoothie')
sl.text('🐔 Hard-Boiled Free-Range Egg')
sl.text('🥑🍞 Avocado Toast')

sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas as pd
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# let's put a pick list here so they can pick the fruit they want to include
fruits_selected = sl.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
sl.dataframe(fruits_to_show)

# new section to display fruitivise api response
sl.header("Fruityvice Fruit Advice!")
fruit_choice = sl.text_input('What fruit would you like information about?','Kiwi')
sl.write('The user entered ', fruit_choice)

import requests as rq
fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# normalize json
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# output as df
sl.dataframe(fruityvice_normalized)

import snowflake.connector as sfc

my_cnx = sfc.connect(**sl.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchone()
sl.text("The fruit load list contains:")
sl.text(my_data_row)

# allow user to add a fruit to list
add_my_fruit = sl.text_input('What fruit would you like to add?','')
sl.write('Thanks for adding ', add_my_fruit)
