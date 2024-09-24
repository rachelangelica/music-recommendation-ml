import streamlit as st
import pickle
import pandas as pd
import requests
import lxml
from bs4 import BeautifulSoup as bs
from bing_image_urls import bing_image_urls
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# def fetch_poster(music_title):
#     response = requests.get("https://saavn.me/search/songs?query={}&page=1&limit=2".format(music_title))
#     data = response.json()
#     return data['data']['results'][0]['image'][2]['link']

def recommend(musics):
    music_index = music[music['title'] == musics].index[0]
    distances = similarity[music_index]
    music_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]
    recommended_music = []
    # recommended_music_poster = []
    for i in music_list:
        music_title = music.iloc[i[0]].title 
        recommended_music.append(music.iloc[i[0]].title)
        # recommended_music_poster.append(fetch_poster(music_title))
    # return recommended_music, recommended_music_poster
    return recommended_music

music_dict = pickle.load(open('musicrec.pkl', 'rb'))
music = pd.DataFrame(music_dict)

similarity = pickle.load(open('similarities.pkl', 'rb'))

st.image('image.png',width=650)
st.title('Music Recommendation System')
selected_music_name = st.selectbox('Select a music you like', music['title'].values)
client_id = "1999931239204f5f9ecf7c4bee0a4b1f"
client_secret = "562b80a3273f4688b78f6a07b35edc77"

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def search_spotify(query, search_type='track'):
    results = sp.search(q=query, type=search_type, limit=10)
    return results[search_type + 's']['items']


if st.button('Recommend'):
    # names, posters = recommend(selected_music_name)
    no = []
    
    names = recommend(selected_music_name)
    for i in range(0, len(music.index)):
        if music['title'][i] == selected_music_name:
            fav_song_artist = i
    
    st.write("Artist : ", music['Artist'][fav_song_artist])
    # st.subheader(music['Artist'][fav_song_artist])
    image = bing_image_urls(music['Artist'][fav_song_artist], limit=1)[0]    
    st.image(image, width=200)
    result = search_spotify(music['title'][fav_song_artist])
    for item in result:
        artists = ", ".join([artist['name'] for artist in item['artists']]) 
        if music['Artist'][fav_song_artist] in artists.lower():
            track_url = item['external_urls']['spotify']
    st.write(f'Link to Spotify : {track_url}')
    
    for j in range(0, 5):
        for i in range(0,len(music.index)):
            if music['title'][i] == names[j]:
                no.append(i)
     
    
    st.write("Recommended Song : ")
    for i in range(0,5):
        st.write(i+1, "Song Title : ", names[i], " - Artist : " , music['Artist'][no[i]])

        image = bing_image_urls(music['Artist'][no[i]], limit=1)[0]
        st.image(image, width=200)
        result = search_spotify(music['title'][no[i]])
        j = 1
        for item in result:
            artists = ", ".join([artist['name'] for artist in item['artists']]) 
            if music['Artist'][no[i]] in artists.lower():
                track_url = item['external_urls']['spotify']
        st.write(f'Link to Spotify : {track_url}')
        
        
# py -m streamlit run main.py