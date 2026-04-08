import streamlit as st
import pandas as pd
import re

st.title("📄 Comprehension CSV Auto Generator")

title = st.text_input("Passage Title")
difficulty = st.selectbox("Difficulty", ["Foundation","Elementary","Intermediate","Advanced"])

raw_input = st.text_area("Paste Passage + Questions", height=400)

def parse_input(text):
    passage = ""
    questions = []

    # Split passage and questions
    parts = text.split("Questions:")
    passage = parts[0].replace("Passage:", "").strip()

    if len(parts) > 1:
        q_block = parts[1]

        q_splits = re.split(r"\n\d+\.", q_block)

        for q in q_splits:
            if not q.strip():
                continue

            lines = q.strip().split("\n")

            q_text = lines[0]
            options = {"A":"", "B":"", "C":"", "D":""}
            correct = ""

            for line in lines[1:]:
                if line.startswith("A."):
                    options["A"] = line[2:].strip()
                elif line.startswith("B."):
                    options["B"] = line[2:].strip()
                elif line.startswith("C."):
                    options["C"] = line[2:].strip()
                elif line.startswith("D."):
                    options["D"] = line[2:].strip()
                elif "Answer:" in line:
                    correct = line.split(":")[1].strip()

            questions.append({
                "question_text": q_text,
                "option_a": options["A"],
                "option_b": options["B"],
                "option_c": options["C"],
                "option_d": options["D"],
                "correct_answer": correct
            })

    return passage, questions

if st.button("Generate CSV"):
    passage_text, questions = parse_input(raw_input)

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

    csv = df.to_csv(index=False, encoding="utf-8-sig")

    st.download_button(
        "Download CSV",
        data=csv,
        file_name=f"{title.replace(' ', '_')}.csv",
        mime="text/csv"
    )

    st.dataframe(df)
