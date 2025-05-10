# Import python packages
import streamlit as st
import requests
import requests

#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose Fruits you want in StreamLit!
  """
)

### Adding a select box 

#option = st.selectbox(
#    "Which fruit would you like have smoothie made of?",
#    ("Banana", "Apple", "Mango", "Strawberry", "Guava", "Peach", "Orange", 
#        "Grapes", "Dragonfruit"),
#)

#st.write("You have selected:", option)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The Name on Smoothie will be: ", name_on_order)

cnx = st.connection("snowflake")
## add list of fruits from table
#session = get_active_session()
session = cnx.session()
my_dataframe = session.table ('smoothies.public.fruit_options').select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe (data = my_dataframe, use_container_width = True)
#st.stop

##convert snowpark dataframe to pandas
pd_df = my_dataframe.to_pandas()
st.dataframe (pd_df)
#st.stop()
##multiselect
ing_list = st.multiselect('Choose up to 5 Fruits: ', my_dataframe, max_selections= 5)

if ing_list:
    ##st.write(ing_list)
    ##st.text(ing_list) ----> Below for loop we are using, so no need of these
##converting list to string->create a variable->make sure PY thinks it contains a string
    ing_string = ''
    for i in ing_list:
        ing_string += i + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == i, 'SEARCH_ON'].iloc[0]
       #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader('fruit_chosen' + "  Nitrution Information ")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon" + search_on)
       #st.text(smoothiefroot_response.json())
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True) 
        #st.subheader('fruit_chosen' + "  Nitrution Information ")
    #st.write(ing_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values ('""" + ing_string + """' , '""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('SUBMIT YOUR ORDER')

    #if time_to_insert:
        #session.sql(my_insert_stmt).collect()
        #st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")

#new section to display smoohyfroot nutritional input


