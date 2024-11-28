# app.py

import streamlit as st

# Titel en introductie
st.title("Gamified Leerplatform")
st.write("Welkom bij het Gamified Leerplatform! Log in om te beginnen.")

# Inloggedeelte
username = st.text_input("Gebruikersnaam")
password = st.text_input("Wachtwoord", type='password')

if st.button("Login"):
    # Authenticatie logica (vereenvoudigd voor deze demo)
    if username == "gebruiker" and password == "wachtwoord":
        st.success(f"Welkom, {username}!")
        
        # Gamificatie-elementen
        st.header("Jouw Voortgang")
        col1, col2, col3 = st.columns(3)
        col1.metric("Punten", "150")
        col2.metric("Badges", "3")
        col3.metric("Ranglijstpositie", "5e")

        # Lessenoverzicht
        st.header("Beschikbare Lessen")
        lessons = [
            {"title": "Introductie tot Bedrijfsprocessen", "duration": 5, "content": "Inhoud van les 1..."},
            {"title": "Klantinteractie 101", "duration": 5, "content": "Inhoud van les 2..."},
            {"title": "Productkennis Basics", "duration": 5, "content": "Inhoud van les 3..."},
        ]

        for lesson in lessons:
            with st.expander(f"{lesson['title']} ({lesson['duration']} min)"):
                st.write(lesson["content"])
                if st.button(f"Start {lesson['title']}", key=lesson['title']):
                    st.write(f"Je hebt {lesson['title']} gestart!")
                    # Hier zou de lesinhoud worden weergegeven
    else:
        st.error("Onjuiste gebruikersnaam of wachtwoord.")
