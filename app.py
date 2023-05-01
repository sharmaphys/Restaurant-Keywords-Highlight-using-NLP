import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import folium
import branca



#title
st.title(":green[Nashville Restaurants at a Glance.]")

#markdown
st.markdown('### This web app provides key highlights for the restaurants using the reviews from yelp \
            provided by the customers.')

DATA_URL = (
    'nashville_restaurants_with_reviews.csv'
)

@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv('nashville_restaurants_with_reviews.csv')
    return data

df = load_data()

#search for the restaurant name
st.header('**:green[Search your restaurant below:]**')
#restaurant_name = st.


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

icon("search")
#selected = 'The Stillery' # just for default
selected = st.text_input("Restaurant Name?", "")
button_clicked = st.button("ok")

#
#if not selected:
#selected = 'The Stillery'
lat=df[df['name'].str.lower().str.contains(selected)]['latitude'].iloc[0]
long=df[df['name'].str.lower().str.contains(selected)]['longitude'].iloc[0]
rest_name = df[df['name'].str.lower().str.contains(selected)]['name'].iloc[0]
star_rating = df[df['name'].str.lower().str.contains(selected)]['stars_x'].iloc[0]
total_reviews = df[df['name'].str.lower().str.contains(selected)]['review_count'].iloc[0]
categories = df[df['name'].str.lower().str.contains(selected)]['categories'].iloc[0]


#define color according to the star rating
if star_rating <=2:
    color ='red'
elif star_rating >2 and star_rating <= 4.0:
    color = 'orange'
else:
    color='green'


# credit to https://www.kaggle.com/code/dabaker/fancy-folium

def fancy_html(rest_name, star_rating,total_reviews,categories,positive,negative):
    
    
    Name = rest_name                           
    Rating = star_rating
    Total_Reviews = total_reviews
    Categories = categories
    Positives = positive
    Negatives = negative

                                              
    
    left_col_colour = "#2A799C"
    right_col_colour = "#C5DCE7"
    
    html = """<!DOCTYPE html>
    <html>

<head>
<h4 style="margin-bottom:0"; width="300px">{}</h4>""".format(Name) + """

</head>
    <table style="height: 126px; width: 300px;">
<tbody>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Star Rating</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Rating) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Total Reviews</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Total_Reviews) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Restaurant Category</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Categories) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Positive Factors</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Positives) + """
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Negative Factors</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Negatives) + """
</tr>
</tbody>
</table>
</html>
"""
    return html


# for map 
from streamlit_folium import st_folium


html = fancy_html(rest_name, star_rating, total_reviews,categories,positive=['clean','live music'], negative=['crowded','longer wait times'])
iframe = branca.element.IFrame(html=html,width=300,height=280)
popup = folium.Popup(iframe,parse_html=True)
# center on Liberty Bell, add marker
m = folium.Map(location=[lat, long], zoom_start=16)
folium.Marker(
    [lat, long], popup=popup,icon=folium.Icon(color=color, icon='info-sign'), tooltip=rest_name
).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)