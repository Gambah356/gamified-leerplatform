# app.py
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

import streamlit as st

# Titel en introductie
st.title("Loogman Leerplatform")
st.write("Welkom bij het Gamified Leerplatform! Log in om te beginnen.")

# Inloggedeelte
username = st.text_input("Gebruikersnaam")
password = st.text_input("Wachtwoord", type='password')

if st.button("Login"):
    # Authenticatie logica (vereenvoudigd voor deze demo)
    if username == "Jeroen" and password == "1234":
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

def show_lesson(lesson_title):
    st.title(lesson_title)
    if lesson_title == "Klantinteractie 101":
        st.header("Missie")
        st.write("**Wij maken het verschil, iedere wasbeurt weer!**")
        st.write("""
            In deze les leer je hoe je onze missie kunt uitdragen in elke interactie met de klant.
            Het is belangrijk om elke klant het gevoel te geven dat ze speciaal zijn en dat we er alles aan doen om hun ervaring uitzonderlijk te maken.
        """)

        # Meerkeuzevragen
        st.subheader("Quiz")

        # Lijst van vragen met opties en juiste antwoorden
        quiz_questions = [
            {
                "question": "Wat is het belangrijkste aspect van onze klantinteractie?",
                "options": ["A) Snelheid", "B) Vriendelijkheid", "C) Kosten", "D) Efficiëntie"],
                "answer": "B) Vriendelijkheid"
            },
            {
                "question": "Hoe kunnen we het verschil maken tijdens elke wasbeurt?",
                "options": ["A) Door extra diensten aan te bieden", "B) Door hogere prijzen te vragen", "C) Door persoonlijke aandacht te geven", "D) Door snelle service te leveren"],
                "answer": "C) Door persoonlijke aandacht te geven"
            },
            {
                "question": "Wat betekent onze missie voor jouw dagelijkse werk?",
                "options": ["A) Niets, het is slechts een slogan", "B) Ik moet altijd op tijd zijn", "C) Ik moet elke klant een unieke ervaring bieden", "D) Ik moet zoveel mogelijk auto's wassen"],
                "answer": "C) Ik moet elke klant een unieke ervaring bieden"
            }
        ]

        user_answers = []
        correct_count = 0

        # Loop door elke vraag en toon deze aan de gebruiker
        for idx, q in enumerate(quiz_questions):
            st.write(f"**Vraag {idx + 1}: {q['question']}**")
            user_choice = st.radio("", q['options'], key=f"question_{idx}")
            user_answers.append({"question": q['question'], "user_choice": user_choice, "correct_answer": q['answer']})
            st.write("---")

        if st.button("Verstuur Antwoorden"):
            for idx, ua in enumerate(user_answers):
                if ua['user_choice'] == ua['correct_answer']:
                    st.success(f"Vraag {idx + 1}: Correct!")
                    correct_count += 1
                else:
                    st.error(f"Vraag {idx + 1}: Onjuist. Het juiste antwoord is: {ua['correct_answer']}")
            st.write(f"Je hebt {correct_count} van de {len(quiz_questions)} vragen correct beantwoord.")

            # Hier kunt u code toevoegen om de resultaten op te slaan en punten toe te kennen

            # Terug naar Dashboard knop
            if st.button("Terug naar Dashboard"):
                st.session_state.page = "dashboard"
                st.experimental_rerun()
    else:
        st.write("Lesinhoud voor deze les is nog niet beschikbaar.")
        if st.button("Terug naar Dashboard"):
            st.session_state.page = "dashboard"
            st.experimental_rerun()
