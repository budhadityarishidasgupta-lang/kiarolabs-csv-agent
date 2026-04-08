import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="CSV Generator", layout="wide")

st.title("📄 Comprehension CSV Generator")

st.markdown("Generate upload-ready CSV for ComprehensionSprint")

# -------------------------
# INPUTS
# -------------------------

title = st.text_input("Passage Title")

difficulty = st.selectbox(
    "Difficulty",
    ["Foundation", "Elementary", "Intermediate", "Advanced"]
)

passage_text = st.text_area("Passage Text", height=300)

num_questions = st.number_input("Number of Questions", min_value=1, max_value=20, value=5)

questions = []

for i in range(num_questions):
    st.markdown(f"### Question {i+1}")

    q_text = st.text_input(f"Question {i+1}", key=f"q{i}")

    col1, col2 = st.columns(2)

    with col1:
        opt_a = st.text_input("Option A", key=f"a{i}")
        opt_b = st.text_input("Option B", key=f"b{i}")

    with col2:
        opt_c = st.text_input("Option C", key=f"c{i}")
        opt_d = st.text_input("Option D", key=f"d{i}")

    correct = st.selectbox(
        "Correct Answer",
        ["A", "B", "C", "D"],
        key=f"correct{i}"
    )

    questions.append({
        "question_text": q_text,
        "option_a": opt_a,
        "option_b": opt_b,
        "option_c": opt_c,
        "option_d": opt_d,
        "correct_answer": correct
    })

# -------------------------
# GENERATE CSV
# -------------------------

if st.button("Generate CSV"):

    rows = []

    for i, q in enumerate(questions):

        rows.append({
            "new_passage": 1 if i == 0 else 0,
            "title": title,
            "passage_text": passage_text if i == 0 else "",
            "difficulty": difficulty if i == 0 else "",
            "question_text": q["question_text"],
            "option_a": q["option_a"],
            "option_b": q["option_b"],
            "option_c": q["option_c"],
            "option_d": q["option_d"],
            "correct_answer": q["correct_answer"],
            "question_type": "mcq",
            "sort_order": i + 1
        })

    df = pd.DataFrame(rows)

    # FIX: UTF-8-SIG for Excel compatibility
    csv = df.to_csv(index=False, encoding="utf-8-sig")

    st.success("CSV generated successfully!")

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{title.replace(' ', '_')}.csv",
        mime="text/csv"
    )

    st.dataframe(df)
