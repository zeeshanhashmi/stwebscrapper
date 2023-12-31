import requests
import streamlit as st
from bs4 import BeautifulSoup
from PIL import Image
import random
import pandas as pd
from pandas import option_context


st.session_state['button'] = False if 'button' not in st.session_state else st.session_state['button']
st.session_state['tags'] = [] if 'tags' not in st.session_state else st.session_state['tags']
st.session_state['selectedTag'] = '' if 'selectedTag' not in st.session_state else st.session_state['selectedTag']
st.session_state['soup'] = [] if 'soup' not in st.session_state else st.session_state['soup']
site = ''

# FUNCTIONS 
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def fetchLottieJson(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def fetchTags(url):
    tags = []
    if len(url) > 0:
        tags.append('')
        acceptTags = ['div','a','img','p','meta']
        html = requests.get(url)
        soup = BeautifulSoup(html.content,'html.parser')
        st.session_state['soup'] = soup
        for tag in soup.find_all():
            if not tag.name in tags and tag.name in acceptTags:
                tags.append(tag.name)
    return tags

result = []
def parseHtmlForTag(option):
     soup = st.session_state['soup']
     if not option == '':
        try:      
            for tag in soup.find_all(option):
                if tag.name == 'a':
                    href = tag.get('href')
                    if href[0] == '/':
                        href = site+href[1:]
                    result.append(href)
                    #st.write(href)               
                elif tag.name == 'div' or tag.name == 'p':
                    result.append(tag.text)
                    #st.write(tag.text)  
                elif tag.name == 'img': 
                    src = tag.get('src')
                    if src[0] == '/':
                        src = site+src
                    result.append(tag.get('src'))   
                elif tag.name == 'meta': 
                    result.append(tag.get('content'))                      
                                
        except:
            ''
        pd.set_option('display.max_colwidth', 400) 
        with option_context('display.max_colwidth', 400):   
            resBlock.write(pd.DataFrame(result, columns=['Result']))    

def clearForm():
    textBlk.empty()
    site =textBlk.text_input('', '', placeholder='https://',key=random.randint(0,99999))
    st.session_state['button'] = False
    st.session_state['tags'] = []
    st.session_state['selectedTag']
    st.session_state['soup'] = []

# Make initial page layout
st.set_page_config(page_title="Website Scrapper", page_icon=":globe_with_meridians:",layout="wide")


load_css("styles/style.css")



with st.container():
    lcol, rcol = st.columns(2)
    with lcol:
        image = Image.open('images/logo.png')
        st.image(image,width=300)
        st.write("by Zeeshan Hashmi")
        st.write("In the input are below, enter url and then click on the Fetch Button")
        st.write("Once loaded select the tag you wish to fetch in the select box.")
    with rcol:
        placeholder = st.empty()

    #lc, rc = st.columns(2)
    with lcol:
        textBlk = st.empty()
        site = textBlk.text_input('', '', placeholder='https://')
        lc1, rc1 = st.columns([1,4])
        with lc1:
            button = st.button('Fetch Tags')  
        with rc1:
            clrButton = st.button('Clear Search') 
            option = ''
            if clrButton:
                site= option = ''
                clearForm()
        if button and st.session_state['button'] == False:
            st.session_state['button'] = True
            st.session_state['tags'] = [] 
            st.session_state['tags'] = fetchTags(site)
            placeholder.empty()
        if st.session_state['button'] == True:
            selBox = st.empty()
            opt = selBox.selectbox('Select Tag',(st.session_state['tags']),index=0)  
            st.session_state['selectedTag'] = opt
    with rcol:
        resBlock = st.empty()  
        if not st.session_state['selectedTag'] == '':
            parseHtmlForTag(st.session_state['selectedTag'])
           
        

      

 