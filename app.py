# app.py

import streamlit as st

# Step 1: Initialize st.session_state
if 'page' not in st.session_state:
    st.session_state.page = 'login'  # Start with the login page

if 'points' not in st.session_state:
    st.session_state.points = 150  # Starting points

if 'leaderboard_position' not in st.session_state:
    st.session_state.leaderboard_position = 5  # Starting leaderboard position

if 'badges' not in st.session_state:
    st.session_state.badges = 3  # Starting number of badges

# Step 2: Define lessons
lessons = [
    {"title": "Introductie tot Bedrijfsprocessen", "duration": 5, "content": "Leer over onze bedrijfsprocessen."},
    {"title": "Klantinteractie 101", "duration": 5, "content": "Verbeter je klantinteractie vaardigheden."},
    {"title": "Productkennis Basics", "duration": 5, "content": "Verdiep je in onze producten."},
]

# Step 3: Define the show_lesson function with multiple choice questions
def show_lesson(lesson_title):
    st.title(lesson_title)
    if lesson_title == "Klantinteractie 101":
        st.header("Missie")
        st.write("**Wij maken het verschil, iedere wasbeurt weer!**")
        st.write("""
            In deze les leer je hoe je onze missie kunt uitdragen in elke interactie met de klant.
            Het is belangrijk om elke klant het gevoel te geven dat ze speciaal zijn en dat we er alles aan doen om hun ervaring uitzonderlijk te maken.
        """)

        # Multiple-choice questions
        st.subheader("Quiz")

        # List of questions with options and correct answers
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

        # Loop through each question and display it to the user
        for idx, q in enumerate(quiz_questions):
            st.write(f"**Vraag {idx + 1}: {q['question']}**")
            user_choice = st.radio("", q['options'], key=f"question_{idx}")
            user_answers.append({"question": q['question'], "user_choice": user_choice, "correct_answer": q['answer']})
            st.write("---")

        # Check if the user has already completed the quiz
        if 'quiz_submitted' not in st.session_state:
            st.session_state.quiz_submitted = False

        if not st.session_state.quiz_submitted:
            if st.button("Verstuur Antwoorden"):
                st.session_state.quiz_submitted = True  # Mark quiz as submitted
                for idx, ua in enumerate(user_answers):
                    if ua['user_choice'] == ua['correct_answer']:
                        st.success(f"Vraag {idx + 1}: Correct!")
                        correct_count += 1
                    else:
                        st.error(f"Vraag {idx + 1}: Onjuist. Het juiste antwoord is: {ua['correct_answer']}")
                st.write(f"Je hebt {correct_count} van de {len(quiz_questions)} vragen correct beantwoord.")

                # Add points based on correct answers
                points_earned = correct_count * 10  # For example, 10 points per correct answer
                st.session_state.points += points_earned

                st.write(f"Je hebt {points_earned} punten verdiend!")
                st.write(f"Totaal aantal punten: {st.session_state.points}")

                # Update leaderboard position (simplified logic)
                if correct_count >= 2 and st.session_state.leaderboard_position > 1:
                    st.session_state.leaderboard_position -= 1
                    st.write(f"Gefeliciteerd! Je ranglijstpositie is verbeterd naar {st.session_state.leaderboard_position}e plaats.")

                # Award badge if all answers are correct
                if correct_count == len(quiz_questions):
                    st.session_state.badges += 1
                    st.write("Je hebt een nieuwe badge verdiend!")

                # Button to return to dashboard
                if st.button("Terug naar Dashboard"):
                    # Reset quiz state
                    st.session_state.quiz_submitted = False
                    st.session_state.page = 'dashboard'
            else:
                if st.button("Terug naar Dashboard"):
                    st.session_state.page = 'dashboard'
        else:
            st.write("Je hebt deze quiz al voltooid.")
            if st.button("Terug naar Dashboard"):
                # Reset quiz state
                st.session_state.quiz_submitted = False
                st.session_state.page = 'dashboard'

    else:
        st.write("Lesinhoud voor deze les is nog niet beschikbaar.")
        if st.button("Terug naar Dashboard"):
            st.session_state.page = 'dashboard'

# Step 4: Main function of the app
def main():
    # Login page
    if st.session_state.page == 'login':
        st.title("Gamified Leerplatform")
        st.write("Welkom bij het Gamified Leerplatform! Log in om te beginnen.")

        # Login section
        username = st.text_input("Gebruikersnaam")
        password = st.text_input("Wachtwoord", type='password')

        if st.button("Login"):
            # Simple authentication logic (for demonstration)
            if username == "gebruiker" and password == "wachtwoord":
                st.success(f"Welkom, {username}!")
                st.session_state.page = 'dashboard'
            else:
                st.error("Onjuiste gebruikersnaam of wachtwoord.")

    # Dashboard page
    elif st.session_state.page == 'dashboard':
        st.header("Jouw Voortgang")
        col1, col2, col3 = st.columns(3)
        col1.metric("Punten", f"{st.session_state.points}")
        col2.metric("Badges", f"{st.session_state.badges}")
        col3.metric("Ranglijstpositie", f"{st.session_state.leaderboard_position}e")

        # Lessons overview
        st.header("Beschikbare Lessen")
        for lesson in lessons:
            with st.expander(f"{lesson['title']} ({lesson['duration']} min)"):
                st.write(lesson["content"])
                if st.button(f"Start {lesson['title']}", key=f"start_{lesson['title']}"):
                    st.session_state.page = lesson['title']

    # Lesson pages
    elif st.session_state.page in [lesson['title'] for lesson in lessons]:
        show_lesson(st.session_state.page)

    else:
        # Unknown page, return to dashboard
        st.session_state.page = 'dashboard'

# Step 5: Run the app
if __name__ == "__main__":
    main()
