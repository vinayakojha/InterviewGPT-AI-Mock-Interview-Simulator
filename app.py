import streamlit as st
import re

from utils.pdf_reader import extract_text

from ai_interviewer import (
    generate_questions,
    evaluate_answer
)

# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="InterviewGPT",
    page_icon="🎤",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------

st.title(
    "🚀 InterviewGPT – AI Powered Mock Interview Simulator"
)

st.caption(
    "AI Powered Personalized Interview Preparation Platform"
)

st.markdown(
    """
    Upload your resume, enter a job description, generate personalized interview questions,
    and get AI-powered feedback on your answers.
    """
)

st.markdown("---")

# -----------------------------
# Session State
# -----------------------------

if "questions_generated" not in st.session_state:
    st.session_state.questions_generated = False

if "questions" not in st.session_state:
    st.session_state.questions = ""

if "questions_list" not in st.session_state:
    st.session_state.questions_list = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "scores" not in st.session_state:
    st.session_state.scores = []

# -----------------------------
# Resume Upload
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if uploaded_file is not None:

    resume_text = extract_text(
        uploaded_file
    )

    jd = st.text_area(
        "Paste Job Description",
        height=150
    )

    # -----------------------------
    # Generate Questions
    # -----------------------------

    if st.button(
        "Generate Questions"
    ):

        if jd.strip() == "":

            st.warning(
                "Please enter Job Description."
            )

        else:

            with st.spinner(
                "Generating Questions..."
            ):

                questions = generate_questions(
                    resume_text,
                    jd
                )

                st.session_state.questions = questions

                question_list = []
                for line in questions.split("\n"):
                    line = line.strip()
                    if len(line) > 5 and line[0].isdigit():
                        question_list.append(line)

                st.session_state.questions_list = question_list
                st.session_state.questions_generated = True

    # -----------------------------
    # Show Questions
    # -----------------------------

    if st.session_state.questions_generated:

        tab1, tab2 = st.tabs(
            [
                "📋 Interview Questions",
                "🎯 Mock Interview"
            ]
        )

        with tab1:
            # Dashboard Metrics

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
    "Target Role",
    jd
)

            with col2:
                st.metric(
    "Questions",
    "20+"
)

            with col3:
                st.metric(
                    "Model",
                    "GPT-055"
                )

            st.progress(1.0)

            st.markdown("---")

            st.subheader(
                "📋 Interview Questions"
            )

            st.markdown(
                st.session_state.questions
            )

        with tab2:
            st.markdown("---")

            st.header("🎯 Mock Interview Mode")

            # -----------------------------
            # Mock Interview Mode
            # -----------------------------

            if len(st.session_state.questions_list) > 0:
                current_q = st.session_state.questions_list[st.session_state.current_question]
                progress = (st.session_state.current_question + 1) / len(st.session_state.questions_list)
                st.progress(progress)

                st.subheader(f"Question {st.session_state.current_question + 1}")

                st.info(current_q)

                answer = st.text_area(
                    "Your Answer",
                    height=200
                )

                if st.button("Evaluate Answer"):
                    if current_q.strip() == "" or answer.strip() == "":
                        st.warning(
                            "Please enter both Question and Answer."
                        )
                    else:
                        with st.spinner("Evaluating Answer..."):
                            feedback = evaluate_answer(
                                current_q,
                                answer
                            )
                            st.session_state.feedback = feedback
                            score_match = re.search(
                                r"Score[:\s]*(\d+)",
                                feedback
                            )

                            if score_match:
                                score = int(
                                    score_match.group(1)
                                )
                                st.metric(
                                    "Interview Score",
                                    f"{score}/10"
                                )
                                st.progress(
                                    score / 10
                                )

                if st.session_state.get("feedback"):
                    st.subheader(
                        "📊 Interview Feedback"
                    )

                    st.markdown(
                        st.session_state.feedback
                    )

                    if (
                        st.session_state.current_question
                        < len(st.session_state.questions_list) - 1
                    ):
                        if st.button("Next Question"):
                            st.session_state.current_question += 1
                            st.session_state.feedback = ""
                            st.rerun()

                    from pdf_generator import generate_pdf

                    pdf_file = generate_pdf(
                        st.session_state.feedback
                    )

                    with open(
                        pdf_file,
                        "rb"
                    ) as file:
                        st.download_button(
                            "📥 Download Report",
                            file,
                            file_name="Interview_Report.pdf",
                            mime="application/pdf"
                        )
            else:
                st.info("No questions generated yet. Please generate questions first.")

                if len(st.session_state.scores) > 0:

                    average_score = (
                        sum(st.session_state.scores)
                        /
                        len(st.session_state.scores)
                    )

                    st.metric(
                        "Average Interview Score",
                        f"{average_score:.1f}/10"
                    )