# app.py

import streamlit as st

# Stap 1: Initialiseer st.session_state
def initialize_state():
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

initialize_state()

# Stap 2: Definieer de lessen
lessons = [
    {"title": "Introductie tot Bedrijfsprocessen", "duration": 5, "content": "Leer over onze bedrijfsprocessen."},
    {"title": "Klantinteractie 101", "duration": 5, "content": "Verbeter je klantinteractie vaardigheden."},
    {"title": "Productkennis Basics", "duration": 5, "content": "Verdiep je in onze producten."},
]

# Functie om een groen vinkje weer te geven
def get_checkmark_icon():
    return "✅"

# Callback-functies
def go_to_page(page_name):
    st.session_state.page = page_name

def handle_login():
    username = st.session_state.username
    password = st.session_state.password
    if username == "gebruiker" and password == "wachtwoord":
        st.success(f"Welkom, {username}!")
        st.session_state.page = 'dashboard'
    else:
        st.error("Onjuiste gebruikersnaam of wachtwoord.")

def start_lesson(lesson_title):
    st.session_state.page = lesson_title

def submit_quiz(lesson_title, quiz_questions):
    correct_count = 0
    total_questions = len(quiz_questions)
    user_answers = []

    for idx, q in enumerate(quiz_questions):
        user_choice = st.session_state.get(f"question_{lesson_title}_{idx}")
        user_answers.append({"question": q['question'], "user_choice": user_choice, "correct_answer": q['answer']})

    for idx, ua in enumerate(user_answers):
        if ua['user_choice'] == ua['correct_answer']:
            st.success(f"Vraag {idx + 1}: Correct!")
            correct_count += 1
        else:
            st.error(f"Vraag {idx + 1}: Onjuist. Het juiste antwoord is: {ua['correct_answer']}")

    st.write(f"Je hebt {correct_count} van de {total_questions} vragen correct beantwoord.")

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
    if correct_count == total_questions:
        st.session_state.badges += 1
        st.write("Je hebt een nieuwe badge verdiend!")

    # Markeer de les als voltooid en sla het aantal correcte antwoorden op
    st.session_state.completed_lessons[lesson_title] = correct_count

    # Wis quizgerelateerde gegevens uit st.session_state
    for idx in range(len(quiz_questions)):
        key = f"question_{lesson_title}_{idx}"
        if key in st.session_state:
            del st.session_state[key]

    # Ga terug naar het dashboard
    st.session_state.page = 'dashboard'

def show_lesson(lesson_title):
    st.title(lesson_title)

    # Controleer of de les voltooid is
    if lesson_title in st.session_state.completed_lessons:
        st.write("Je hebt deze les al voltooid.")
        st.button("Terug naar Dashboard", on_click=go_to_page, args=('dashboard',))
    else:
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

            # Loop door elke vraag en toon deze aan de gebruiker
            for idx, q in enumerate(quiz_questions):
                st.write(f"**Vraag {idx + 1}: {q['question']}**")
                st.radio("", q['options'], key=f"question_{lesson_title}_{idx}")
                st.write("---")

            st.button("Verstuur Antwoorden", on_click=submit_quiz, args=(lesson_title, quiz_questions))
            st.button("Terug naar Dashboard", on_click=go_to_page, args=('dashboard',))
        else:
            st.write("Lesinhoud voor deze les is nog niet beschikbaar.")
            st.button("Terug naar Dashboard", on_click=go_to_page, args=('dashboard',))

# Stap 4: Hoofdfunctie van de app
def main():
    if st.session_state.page == 'login':
        st.title("Gamified Leerplatform")
        st.write("Welkom bij het Gamified Leerplatform! Log in om te beginnen.")

        # Inloggedeelte
        st.text_input("Gebruikersnaam", key='username')
        st.text_input("Wachtwoord", type='password', key='password')

        st.button("Login", on_click=handle_login)

    elif st.session_state.page == 'dashboard':
        # Controleer of we confetti moeten tonen
        if st.session_state.show_confetti:
            st.balloons()
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
                    st.button(f"Start {lesson_title}", key=f"start_{lesson_title}", on_click=start_lesson, args=(lesson_title,))
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

    elif st.session_state.page in [lesson['title'] for lesson in lessons]:
        show_lesson(st.session_state.page)

    else:
        # Onbekende pagina, terug naar dashboard
        st.session_state.page = 'dashboard'

# Stap 5: Voer de app uit
if __name__ == "__main__":
    main()
