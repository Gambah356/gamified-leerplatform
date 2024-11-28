# app.py

import streamlit as st

# Stap 1: Initialiseer st.session_state
if 'page' not in st.session_state:
    st.session_state.page = 'login'  # Start met de login pagina

if 'points' not in st.session_state:
    st.session_state.points = 150  # Startpunten

if 'leaderboard_position' not in st.session_state:
    st.session_state.leaderboard_position = 5  # Startpositie op de ranglijst

if 'badges' not in st.session_state:
    st.session_state.badges = 3  # Startaantal badges

if 'completed_lessons' not in st.session_state:
    st.session_state.completed_lessons = {}  # Houdt bij welke lessen voltooid zijn

if 'show_confetti' not in st.session_state:
    st.session_state.show_confetti = False  # Vlag voor confetti-effect

# Stap 2: Definieer de lessen
lessons = [
    {"title": "Introductie tot Bedrijfsprocessen", "duration": 5, "content": "Leer over onze bedrijfsprocessen."},
    {"title": "Klantinteractie 101", "duration": 5, "content": "Verbeter je klantinteractie vaardigheden."},
    {"title": "Productkennis Basics", "duration": 5, "content": "Verdiep je in onze producten."},
]

# Functie om een groen vinkje weer te geven
def get_checkmark_icon():
    return "✅"

# Stap 3: Definieer de show_lesson functie met meerdere meerkeuzevragen
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
            user_choice = st.radio("", q['options'], key=f"question_{lesson_title}_{idx}")
            user_answers.append({"question": q['question'], "user_choice": user_choice, "correct_answer": q['answer']})
            st.write("---")

        # Controleer of de gebruiker de quiz al heeft ingediend
        if f'quiz_submitted_{lesson_title}' not in st.session_state:
            st.session_state[f'quiz_submitted_{lesson_title}'] = False

        if not st.session_state[f'quiz_submitted_{lesson_title}']:
            if st.button("Verstuur Antwoorden"):
                st.session_state[f'quiz_submitted_{lesson_title}'] = True  # Markeer quiz als ingediend
                for idx, ua in enumerate(user_answers):
                    if ua['user_choice'] == ua['correct_answer']:
                        st.success(f"Vraag {idx + 1}: Correct!")
                        correct_count += 1
                    else:
                        st.error(f"Vraag {idx + 1}: Onjuist. Het juiste antwoord is: {ua['correct_answer']}")
                st.write(f"Je hebt {correct_count} van de {len(quiz_questions)} vragen correct beantwoord.")

                # Voeg punten toe op basis van correcte antwoorden
                points_earned = correct_count * 10  # Bijvoorbeeld 10 punten per correct antwoord
                st.session_state.points += points_earned

                st.write(f"Je hebt {points_earned} punten verdiend!")
                st.write(f"Totaal aantal punten: {st.session_state.points}")

                # Update ranglijstpositie (vereenvoudigde logica)
                previous_position = st.session_state.leaderboard_position  # Bewaar vorige positie
                if correct_count >= 2 and st.session_state.leaderboard_position > 1:
                    st.session_state.leaderboard_position -= 1
                    st.write(f"Gefeliciteerd! Je ranglijstpositie is verbeterd naar {st.session_state.leaderboard_position}e plaats.")
                    # Stel de confetti-vlag in
                    st.session_state.show_confetti = True

                # Verleen badge als alle antwoorden correct zijn
                if correct_count == len(quiz_questions):
                    st.session_state.badges += 1
                    st.write("Je hebt een nieuwe badge verdiend!")

                # Markeer de les als voltooid en sla het aantal correcte antwoorden op
                st.session_state.completed_lessons[lesson_title] = correct_count

                # Knop om terug te keren naar het dashboard
                if st.button("Terug naar Dashboard"):
                    st.session_state.page = 'dashboard'
            else:
                if st.button("Terug naar Dashboard"):
                    st.session_state.page = 'dashboard'
        else:
            st.write("Je hebt deze quiz al voltooid.")
            if st.button("Terug naar Dashboard"):
                st.session_state.page = 'dashboard'

    else:
        st.write("Lesinhoud voor deze les is nog niet beschikbaar.")
        if st.button("Terug naar Dashboard"):
            st.session_state.page = 'dashboard'

# Stap 4: Hoofdfunctie van de app
def main():
    # Inlogpagina
    if st.session_state.page == 'login':
        st.title("Gamified Leerplatform")
        st.write("Welkom bij het Gamified Leerplatform! Log in om te beginnen.")

        # Inloggedeelte
        username = st.text_input("Gebruikersnaam")
        password = st.text_input("Wachtwoord", type='password')

        if st.button("Login"):
            # Eenvoudige authenticatie logica (voor demonstratie)
            if username == "gebruiker" and password == "wachtwoord":
                st.success(f"Welkom, {username}!")
                st.session_state.page = 'dashboard'
            else:
                st.error("Onjuiste gebruikersnaam of wachtwoord.")

    # Dashboardpagina
    elif st.session_state.page == 'dashboard':
        # Controleer of we confetti moeten tonen
        if st.session_state.show_confetti:
            st.success("Gefeliciteerd met je verbeterde ranglijstpositie!")
            st.session_state.show_confetti = False  # Reset de confetti-vlag

        st.header("Jouw Voortgang")
        col1, col2, col3 = st.columns(3)
        col1.metric("Punten", f"{st.session_state.points}")
        col2.metric("Badges", f"{st.session_state.badges}")
        col3.metric("Ranglijstpositie", f"{st.session_state.leaderboard_position}e")

        # Verdeel lessen in beschikbaar en voltooid
        available_lessons = [lesson for lesson in lessons if lesson['title'] not in st.session_state.completed_lessons]
        completed_lessons = [lesson for lesson in lessons if lesson['title'] in st.session_state.completed_lessons]

        # Beschikbare Lessen
        if available_lessons:
            st.header("Beschikbare Lessen")
            for lesson in available_lessons:
                lesson_title = lesson['title']
                with st.expander(f"{lesson_title} ({lesson['duration']} min)"):
                    st.write(lesson["content"])
                    if st.button(f"Start {lesson_title}", key=f"start_{lesson_title}"):
                        st.session_state.page = lesson_title
        else:
            st.header("Geen Beschikbare Lessen")
            st.write("Je hebt alle lessen voltooid. Goed gedaan!")

        # Voltooide Lessen
        if completed_lessons:
            st.header("Voltooide Lessen")
            for lesson in completed_lessons:
                lesson_title = lesson['title']
                correct_answers = st.session_state.completed_lessons[lesson_title]
                total_questions = 3  # Aantal vragen in de quiz (pas aan indien nodig)
                checkmark = get_checkmark_icon()
                with st.expander(f"{lesson_title} {checkmark}"):
                    st.write(f"Je hebt deze les voltooid met {correct_answers}/{total_questions} correct beantwoorde vragen.")
        else:
            st.header("Voltooide Lessen")
            st.write("Je hebt nog geen lessen voltooid.")

    # Lespagina's
    elif st.session_state.page in [lesson['title'] for lesson in lessons]:
        show_lesson(st.session_state.page)

    else:
        # Onbekende pagina, terug naar dashboard
        st.session_state.page = 'dashboard'

# Stap 5: Voer de app uit
if __name__ == "__main__":
    main()
