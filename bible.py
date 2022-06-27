
import streamlit as st
import pandas as pd
import requests
import streamlit as st


st.set_page_config(layout="wide", page_icon=':scroll:', page_title='Biblica | Online Bible',
                   initial_sidebar_state="expanded")

hide_things = """
<style>
#MainMenu { visibility: hidden;}
footer { visibility:hidden;}
header { visibility:hidden;}
</style>
"""
st.markdown(hide_things, unsafe_allow_html=True)

st.markdown("""<meta charset="utf-8">""", unsafe_allow_html=True)
st.markdown("""<meta name="viewport" content="width=device-width, initial-scale=1">""",
            unsafe_allow_html=True)
st.markdown("""<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
 integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">""", unsafe_allow_html=True)
code = ""

code = """<link href="https://fonts.googleapis.com/css2?family=Amatic+SC&family=Arizonia&family=Calligraffitti&family=Caveat&family=Encode+Sans:wght@100;"""

code += """&family=Nixie+One&family=Open+Sans&family=KoHo:wght@200&family=Notable&family=Oooh+Baby&family=Open+Sans&"""
code += """Poiret+One&family=Bitter:wght@100&&family=Tajawal:wght@200&family=Work+Sans:wght@100&display=swap" rel="stylesheet">"""
st.markdown(code, unsafe_allow_html=True)
st.markdown("""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.3/font/bootstrap-icons.css">""", unsafe_allow_html=True)


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def header():
    return f"""
    <div class="card text-center border-0 bg-transparent" style="margin-top:-10vh">
      <div class="card-body">
      <span style="font:15px Thasadith;">A web app created by <a href ="https://www.linkedin.com/in/franklyn-achara-59b959162/" >Achara Franklyn</a> </span>
         <p class="card-text " style="font:60px Notable">Biblica</p>
          <p class="card-text my-3" style="font:15px Quicksand">
    Biblica is an online bible and a great source for daily  motivation and inspiration. It contains all passages from the bible in different translations.
    Take advantage of this powerful only resource to help you achieve your goals and live a fulfilling life as you read a word from God.</p>
     
      </div>
    </div>
  
    """


def bible_details(icon, book, message):
    return f"""
     <div class="card border-0" style="background-color: transparent;height:15vh;">
     <div class="d-flex justify-content-center align-items-center mx-2 rounded-circle p-2" style=" width:3rem; border:1px solid white;">
     <i class="bi bi-{icon}" style="font-size:20px"></i>
     </div>
      <div class="card-body">
        <p class="card-title" style="font:20px Bitter;">{book}</p>
        <p class="card-text" style="font:15px Tajawal";>{message}</p>
        
      </div>
    </div>
    """


def circles():
    return f"""
        <div class="card" style="width:70%;border-color: transparent;height:15vh;margin: 0px 35px;">
           <div class="card-body col rounded-circle bg-secondary">
           </div>
        </div>
       """


def card(message, verses, number, show='visibility', show2='hidden'):
    return f"""
         <div class="row row-cols-1 row-cols-md-3 g-4">
  <div class="col-md-5" style="border-color:transparent;border-right:1px solid white; border-radius:0;visibility: {show}">
    <div class="card h-100 bg-transparent  border-0">
        <div class="card-body">
        <p class="card-title" style="font:20px 'Nixie One';"><b><i>{verses}</i></b></p>
        <p class="text-right" style="font: 17px 'Open Sans';word-spacing:3px;">{message}</p>
      </div>
    </div>
  </div>
  
  <div class="col-md-2 d-flex justify-content-center align-items-center" style="height:25vh;">
    <div class="d-flex justify-content-center align-items-center" style="width:60%;height:50%; border:2px solid white; border-radius: 50%;">
        <div>
        <p class="text-center" style="font-size:10px">verse</p>
        <p style = "font:30px KoHo;">{int(number):02d}</p>
        </div>
    </div>    
  </div>
  <div class="col-md-5 " style="border-color:transparent;border-left:1px solid white; border-radius:0;visibility: {show2}">
    <div class="card h-100 bg-transparent  border-0">
        <div class="card-body">
        <p class="card-title" style="font:20px 'Nixie One';"><b><i>{verses}</i></b></p>
        <p class="text-right" style="font: 17px 'Open Sans'; word-spacing:7px;">{message}</p>
      </div>
    </div>
  </div>
</div>
<br/><br/>
       """


@st.cache
def dataframe():
    df = pd.read_pickle("bible_data.pkl")
    return df


df = dataframe()

versions = {
    'Bible in Basic English': 'bbe',
    'King James Version': 'kjv',
    'World English Bible': 'web',
    'World English Bible, British Edition': 'webbe',
    'João Ferreira de Almeida': 'almeida',
    'Protestant Romanian Corrected Cornilescu Version': 'rccv'
}


def spacermain(order, number):
    for i in range(number):
        order.markdown(
            '<br/>', unsafe_allow_html=True)


def passage(book, chapter, start, end, translation):
    lister = []
    if start > end:
        st.error("The start verse cannot be greater than end verse")
        st.stop()

    elif start == end:
        url = f'https://bible-api.com/{book}%20{chapter}:{start}?translation={translation}'
        # url= f'https://bible-api.com/john 3:16?translation=kjv'
    else:
        url = f'https://bible-api.com/{book}+{chapter}:{start}-{end}?translation={translation}'

    try:
        response = requests.get(url).json()

        lister.append(str(response['verses'][0]['book_name']) +
                      " " + str(response['verses'][0]['chapter']) + " : ")
        lister.append([li['text'] for li in response['verses']])
        lister.append([li['verse'] for li in response['verses']])
    except KeyError:
        st.error(
            "Please check: Are you sure the chapter and verse exists in the Bible? ")
        st.stop()

    return lister
    # st.write(response['verses'][0]['book_name'])


v1, v2, v3 = st.columns([2, 5, 2])

with v2:
    st.markdown(header(), unsafe_allow_html=True)


y1, x1, x2, x3, xt, x4, y5 = st.columns([2, 3, 2, 2, 2, 3, 2])

with st.container():
    with x1:
        '---'
        books = st.selectbox(
            'How would you like to be contacted?',
            df['book'].unique(), df['book'].tolist().index('John'))
        '---'
    with x2:
        '---'
        chapter = st.number_input(
            'Select the Chapter', min_value=1, value=3, step=1)
        '---'
    with x3:
        '---'
        verse = st.number_input(
            'Select the Start verse', min_value=1, value=16, step=1)
        '---'
        st.markdown("""<p style="font: 20px 'Open Sans'; margin-top:2vh;white-space:nowrap;">Facts about <span style="font-weight:bold;"> """ +
                    books + """<span>""", unsafe_allow_html=True)
    with xt:
        '---'
        verse_to = st.number_input(
            'Select the End verse', min_value=1, value=17, step=1)
        '---'
    with x4:
        '---'
        translation = st.selectbox(
            'Select the translation?',
            [key for key in versions], [key for key in versions].index('King James Version'))
        '---'


spacermain(st, 2)
z1, z2, z3, z4, z5, z6 = st.columns([2, 2, 2, 2, 4, 2])
spacermain(st, 1)
st.markdown("""---""")
df_filtered = df[df['book'] == books]

written = ' The book of <b>' + str(df_filtered.iloc[0]['book']) + \
    "</b><em> witten by</em> " + str(df_filtered.iloc[0]['Author'])
with z2:

    st.markdown(bible_details(
        'book', 'Book', written), unsafe_allow_html=True)

with z3:

    st.markdown(bible_details('gem', 'Genre',
                df_filtered.iloc[0]['Genre']), unsafe_allow_html=True)

with z4:
    st.markdown(bible_details('calendar-check', 'Period Written',
                df_filtered.iloc[0]['Year']), unsafe_allow_html=True)

with z5:
    st.markdown(bible_details('file-earmark-word', 'About',
                df_filtered.iloc[0]['message']), unsafe_allow_html=True)

spacermain(st, 3)
output = passage(books, int(chapter), int(verse),
                 int(verse_to), versions[translation])
col1, col2, col3 = st.columns([2, 12, 2])
with col2:

    for (i, j) in zip(output[1], output[2]):
        if j % 2 == 0:
            st.markdown(card(
                i, output[0] + ' ' + str(j), str(j), show='visible', show2='hidden'), unsafe_allow_html=True)

        else:
            st.markdown(card(
                i, output[0] + ' ' + str(j), str(j), show='hidden', show2='visible'), unsafe_allow_html=True)
