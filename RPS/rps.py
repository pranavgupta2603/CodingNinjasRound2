#from __future__ import division
from math import sqrt
import random as rand
import streamlit as st
import pandas as pd

st.markdown("""
<style>
#MainMenu{visibility: hidden;} 
td.css-57lzw8:nth-of-type(4){}
footer, label.css-zyb2jl, img.css-1jhkrss, button.css-bl767a {visibility: hidden;}
.copy-button{color:red;}
button.css-19deh3e, button.css-6163i7, button.css-14n4bfl{visibility: hidden; cursor: none;}

</style>

""", unsafe_allow_html=True)
def create_combos():
    a = ["0", "1", "2"]
    d = {}
    for i in a:
        for j in a:
            for k in a:
                for l in a:
                    d[i+j+k+l] = 4
    return d

def checkGame(a, b):
    if a == '0' and b == '1' or a == '1' and b == '2' or a == '2' and b == '0':
        return "Loss"
    elif a == b:
        return "Tie"
    else:
        return "Win"
if "combos" not in st.session_state or "rps" not in st.session_state:
    st.session_state["combos"] = create_combos()
    st.session_state["rps"]  = {'0' : 'rock', '1' : 'paper', '2' : 'scissor'}


wins, ties, losses = 0,0,0
if "wins" not in st.session_state:
    st.session_state["wins"] = 0
    st.session_state["ties"] = 0
    st.session_state["losses"] = 0
    df = pd.DataFrame({"You": [], "Computer": [], "Result": []})
    st.session_state["df"] = df

if "lastthree" not in st.session_state:
    st.session_state["lastthree"] = ''

st.sidebar.title("ROCK PAPER SCISSORS")
st.sidebar.subheader("Click any of the Rock/Paper/Scissor buttons to start playing")
st.sidebar.write("")
r, p, s = st.sidebar.columns(3)
st.sidebar.markdown("""<hr>""", unsafe_allow_html=True)
player, vs, comp = st.columns([1.25, 1, 1])

rock = r.button("Rock")
paper = p.button("Paper")
sci = s.button("Scissor")
#Loops until user presses q
def main(x):
    
    if(len(st.session_state.lastthree) < 3):
        y = str(rand.randint(0,2))
        st.session_state.lastthree = st.session_state.lastthree + x
        if y == '0':
            comp.image("rock.png", width=200)
        elif y == '1':
            
            comp.image("paper.png", width=200)
        else:
            comp.image("scissors.png", width=200)
    else:
        #print(st.session_state.combos)
        st.session_state.lastthree = st.session_state.lastthree[1:3] + x
        r_count = st.session_state.combos[st.session_state.lastthree + '0']
        p_count = st.session_state.combos[st.session_state.lastthree + '1']
        s_count = st.session_state.combos[st.session_state.lastthree + '2']

        tot_count = r_count + p_count + s_count

        q_dist = [ r_count/tot_count, p_count/tot_count, 1- (r_count/tot_count) - (p_count/tot_count) ]
        #print(q_dist)
        result = [ max(q_dist[2]-q_dist[1],0), max(q_dist[0]-q_dist[2],0), max(q_dist[1]-q_dist[0],0) ]
        #print(result)
        resultnorm = sqrt(result[0]*result[0] + result[1]*result[1] + result[2]*result[2])
        result = [result[0]/resultnorm, result[1]/resultnorm, 1 - result[0]/resultnorm - result[1]/resultnorm]

        y = rand.uniform(0,1)
        #print(y)
        if y <= result[0]:
            y = '0'
            comp.image("rock.png", width=200)
        elif y <= result[0] + result[1]:
            y = '1'
            comp.image("paper.png", width=200)
        else:
            y = '2'
            comp.image("scissors.png", width=200)

        #update dictionary
        st.session_state.combos[st.session_state.lastthree+x] += 1

    
    player.write('You played: ' + st.session_state.rps[x].upper())
    comp.write("Computer played: " + st.session_state.rps[y].upper())
    data = pd.DataFrame({"You": [st.session_state.rps[x].upper()], "Computer": [st.session_state.rps[y].upper()], "Result": [checkGame(x, y)]})
    st.session_state["df"] = st.session_state["df"].append(data, ignore_index=True)
    st.sidebar.dataframe(st.session_state.df)
    if checkGame(x,y) == "Loss":
        st.session_state.losses += 1
    elif checkGame(x,y) == "Tie":
        st.session_state.ties   += 1
    elif checkGame(x,y) == "Win":
        st.session_state.wins   += 1

    st.sidebar.write('Wins:', str(st.session_state.wins) + ' Losses: ' + str(st.session_state.losses) + ' Ties: ' + str(st.session_state.ties))
if rock:
    x = '0'
    vs.write("")
    vs.write("")
    vs.write("")
    vs.title("SHOOT")
    main(x)
    player.image("rock.png", width=200)
elif paper:
    x = '1'
    vs.write("")
    vs.write("")
    vs.write("")
    vs.title("SHOOT")
    main(x)
    player.image("paper.png", width=200)
elif sci:
    x = '2'
    vs.write("")
    vs.write("")
    vs.write("")
    vs.title("SHOOT")
    main(x)
    player.image("scissors.png", width=200)
else:
    pass
