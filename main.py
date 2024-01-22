import streamlit as st
import pickle
import requests
from PIL import Image
from streamlit_option_menu import option_menu

selected = option_menu(
    menu_title=None,  # required
    options=["Movie", "Books", "Song"],  # required
    icons=["film", "book", "file-earmark-music"],  # optional
    menu_icon="cast",  # optional
    default_index=0,  # optional
    orientation="horizontal",
)


if selected == "Movie":
    def fetch_poster(movie_id):
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
            movie_id)
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path


    def recommend(movie):
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        recommended_movie_title = []
        for i in distances[1:6]:
            recommended_movie_names.append(movies.iloc[i[0]].title)
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_title.append(movies.iloc[i[0]].overview)
            recommended_movie_posters.append(fetch_poster(movie_id))
        return recommended_movie_names, recommended_movie_posters, recommended_movie_title


    movies = pickle.load(open('movie_list.pkl', 'rb'))
    movie_list = movies['title'].values
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    image2 = Image.open('mrt.jpg')

    # Here The Website Begin
    # st.set_page_config(page_title="Movie Recommender System")
    st.title("")
    st.image(image2)
    selected_movie = st.selectbox(" ", movie_list)
    click = st.button('Show Recommendation')
    if click:
        recommended_movie_names, recommended_movie_posters, recommended_movie_title = recommend(selected_movie)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])
        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])
        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])
        with st.expander(recommended_movie_names[0]):
            st.markdown(recommended_movie_title[0])
        with st.expander(recommended_movie_names[1]):
            st.markdown(recommended_movie_title[1])
        with st.expander(recommended_movie_names[2]):
            st.markdown(recommended_movie_title[2])
        with st.expander(recommended_movie_names[3]):
            st.markdown(recommended_movie_title[3])
        with st.expander(recommended_movie_names[4]):
            st.markdown(recommended_movie_title[4])
        columns = st.columns((2, 1, 2))
        button_pressed = columns[1].button('Search Again', click)
if selected == "Books":
    def recommend(movie):
        index = books[books['Book-Title'] == movie].index[0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)
        return data


    pt = pickle.load(open('pt.pkl', 'rb'))
    books = pickle.load(open('books.pkl', 'rb'))
    book_list = pickle.load(open('book_title.pkl', 'rb'))
    similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
    image1 = Image.open('brt.jpg')

    # Here The Website Begin
    # st.set_page_config(page_title="Movie Recommender System")
    st.title("")
    st.image(image1)
    selected_books = st.selectbox(" ", book_list)
    click = st.button('Show Recommendation')
    if click:
        final_book = recommend(selected_books)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.image(final_book[0][2])
            st.text(final_book[0][0])
            st.text(final_book[0][1])

        with col2:
            st.image(final_book[1][2])
            st.text(final_book[1][0])
            st.text(final_book[1][1])

        with col3:
            st.image(final_book[2][2])
            st.text(final_book[2][0])
            st.text(final_book[2][1])
        with col4:
            st.image(final_book[3][2])
            st.text(final_book[3][0])
            st.text(final_book[3][1])

        columns = st.columns((2, 1, 2))
        button_pressed = columns[1].button('Search Again', click)
if selected == "Song":
    image3 = Image.open('srt.jpg')
    st.image(image3)
    st.title(f"You Have Selected {selected} Which is Under Construction")

customized_button = st.markdown("""
    <style >
    .stDownloadButton, div.stButton {text-align:center}
    div.stButton > button:first-child {
        background-color: #FF4242;
        color:#ffffff;
    }
    div.stButton > button:hover {
        background-color: #BC4646;
        color:#ffffff;
        }
    </style>""", unsafe_allow_html=True)
