import streamlit as sl
import pandas as pd
import requests as rq
import snowflake.connector as sfc
from urllib.error import URLError

sl.title('My Parents New Healthy Diner')

sl.header('Breakfast Menu')
sl.text('🥣 Omega 3 & Blueberry Oatmeal')
sl.text('🥗 Kale, Spinach & Rocket Smoothie')
sl.text('🐔 Hard-Boiled Free-Range Egg')
sl.text('🥑🍞 Avocado Toast')

sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# let's put a pick list here so they can pick the fruit they want to include
fruits_selected = sl.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
sl.dataframe(fruits_to_show)

# get_fruityvice_data f(x)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

# fruityvise
sl.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = sl.text_input('What fruit would you like information about?')
  if not fruit_choice:
    sl.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    sl.dataframe(back_from_function)

except URLError as e:
  sl.error()
  
sl.write('The user entered ', fruit_choice)

sl.stop()

# establish connection to snowflake
my_cnx = sfc.connect(**sl.secrets["snowflake"])
my_cur = my_cnx.cursor()

# get fruit_load_list and output
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
sl.text("The fruit load list contains:")
my_data_row = my_cur.fetchone()

# allow user to add a fruit to list
add_my_fruit = sl.text_input('What fruit would you like to add?','')
sl.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
