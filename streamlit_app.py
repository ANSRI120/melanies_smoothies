# Import python packages
import streamlit as st
import requests
import requests
import pandas

from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose Fruits you want in StreamLit!
  """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The Name on Smoothie will be: ", name_on_order)

cnx = st.connection("snowflake")

session = cnx.session()
my_dataframe = session.table ('smoothies.public.fruit_options').select(col('FRUIT_NAME'), col('SEARCH_ON'))

pd_df = my_dataframe.to_pandas()
st.dataframe (pd_df)

ing_list = st.multiselect('Choose up to 5 Fruits: ',
                          my_dataframe, 
                          max_selections= 6)

if ing_list:
    ing_string = ''
    for fruit_chosen in ing_list:
        ing_string += i + ' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.subheader(fruit_chosen + "  Nitrution Information ")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon" + search_on)
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True) 
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values ('""" + ing_string + """' , '""" + name_on_order + """')"""

    time_to_insert = st.button('SUBMIT YOUR ORDER')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")

#new section to display smoohyfroot nutritional input


