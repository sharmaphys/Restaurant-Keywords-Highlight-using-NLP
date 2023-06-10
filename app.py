import pandas as pd
pd.options.display.float_format = '{:.2f}'.format
import numpy as np
import streamlit as st
from streamlit_folium import st_folium
import altair as alt
import folium
import branca
from geopy.geocoders import Nominatim


#title
st.title(":green[  Aspect Based Keyword Highlights of Nashville Restaurants.]")

#markdown
st.markdown(
"""
The information of restaurants in yelp online directory provides 
            the star ratings and reviews provided by customers. However, to obtain 
            the overall perspectives on the attributes of the restaurants like service, 
            atomsphere etc. is necessary to read through the reviews. This project aims to provides the 
            positive and negative attributes of the restaurant in couple of keyword highlights 
            in addition to the compound rating factoring into the sentiment of reviews.'
""")

st.markdown(
"""
Quick Info:
- Hover mouse around the cutlery icon provides the name of the restaurant
- Color of icon: green: super rating > 5, orange: greater than 3 and less than 5, red: less than 3
- Click on the icon will pop up a display table with more info regarding the restaurant
"""
)


@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv('final_result.csv')
    return data


# read the data
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
selected = st.text_input("Restaurant Name?", "")
button_clicked = st.button("ok")

def get_latitude_longitude(address):
    geolocator = Nominatim(user_agent="my-app")  # Initialize geocoder
    location = geolocator.geocode(address)  # Geocode the address

    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None

# Example usage
address = "Nashville"
coordinates = get_latitude_longitude(address)
if coordinates:
    latitude, longitude = coordinates

Nashville_coord = list(coordinates)

def get_attributes(selected,dataframe):
    """
    given the name of restaurant, returns its attributes (like name, rating etc)
    """
    attrib = dict()
    attrib['lat']=df[df['name'].str.lower().str.contains(selected)]['latitude'].iloc[0]
    attrib['long']=df[df['name'].str.lower().str.contains(selected)]['longitude'].iloc[0]
    attrib['rest_name'] = df[df['name'].str.lower().str.contains(selected)]['name'].iloc[0]
    attrib['star_rating'] = df[df['name'].str.lower().str.contains(selected)]['super_rating'].iloc[0]
    attrib['total_reviews'] = df[df['name'].str.lower().str.contains(selected)]['review_count'].iloc[0]
    attrib['categories'] = df[df['name'].str.lower().str.contains(selected)]['categories'].iloc[0]
    attrib['positive'] = df[df['name'].str.lower().str.contains(selected)]['positive_aspect'].iloc[0]
    attrib['negative'] = df[df['name'].str.lower().str.contains(selected)]['negative_aspect'].iloc[0]
    return attrib



#define color according to the star rating
def get_color(star_rating):
    if star_rating <=3:
        color ='red'
    elif star_rating >3 and star_rating < 5.0:
        color = 'orange'
    else:
        color='green'
    return color


# credit to https://www.kaggle.com/code/dabaker/fancy-folium
def fancy_html(attribute_dict):    
    Name = attribute_dict['rest_name']
    Rating = attribute_dict['star_rating']
    Total_Reviews = attribute_dict['total_reviews']
    Categories = attribute_dict['categories']
    Positives = attribute_dict['positive']
    Negatives = attribute_dict['negative']

                                            
    
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
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Categories</span></td>
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


#map = folium.Map(location=[36.1627, -86.7816], zoom_start=14)

def draw_map(restaurant_info,m=None):  
    html = fancy_html(restaurant_info)
    iframe = branca.element.IFrame(html=html,width=300,height=280)
    popup = folium.Popup(iframe,parse_html=True)
    # center on icon, add marker
    
    folium.Marker(
        [restaurant_info['lat'], restaurant_info['long']],
          popup=popup,
          icon=folium.Icon(color=get_color(restaurant_info['star_rating']),
                           icon='cutlery'),
                           tooltip=restaurant_info['rest_name']
        ).add_to(m)
    # call to render Folium map in Streamlit
    
    return None

if selected:
    names = df['name'].str.lower()
    name_list = names.values.tolist()

    if any(selected in name for name in name_list):
        restaurant_info = get_attributes(selected, df)
        location = [restaurant_info['lat'], restaurant_info['long']]
        map = folium.Map(location, zoom_start=14)
        draw_map(restaurant_info,map)
        st_data = st_folium(map, width=725)
    else:
        # use the map with nashville at the center
        #map = folium.Map(location=[36.1627, -86.7816], zoom_start=14)
        map = folium.Map(location=Nashville_coord, zoom_start=14)
        st.text('RESTAURANT NOT FOUND.......')
        st_data = st_folium(map, width=725)



st.markdown(
"""
This app uses natural language processing with VADER's sentiment analysis and aspect \
            based sentiment analysis with PyABSA.
"""
)

