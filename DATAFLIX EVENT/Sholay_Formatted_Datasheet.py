import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64  # for local background image

# -------------------------------
# Function to set local background
# -------------------------------
def set_bg_local(image_file):
    import base64
    import streamlit as st
    with open(image_file, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{b64}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# -------------------------------
# Dashboard Setup
# -------------------------------
st.set_page_config(page_title="Sholay (1975) - Detailed Dashboard", layout="wide")

# Set Sholay-themed local background
set_bg_local(r"C:\Users\jadej\OneDrive\Desktop\sholay_bakcground.png")

st.title("🎥 Sholay (1975) - Detailed Dashboard")

# -------------------------------
# Movie Description
# -------------------------------
st.markdown("""
**Sholay (1975)** is one of the greatest and most influential films in Indian cinema.  
Directed by **Ramesh Sippy**, it was released on **15th August 1975** and is regarded as the 
first true *Curry Western* in Bollywood.  

The film tells the story of two ex-convicts, **Jai** (Amitabh Bachchan) and **Veeru** (Dharmendra), 
who are hired by retired police officer **Thakur Baldev Singh** (Sanjeev Kumar) to capture the ruthless bandit **Gabbar Singh** (Amjad Khan).  

Known for its **iconic dialogues, memorable characters, timeless music, and action sequences**,  
*Sholay* is widely celebrated as the **Film of the Millennium** by BBC India and continues to 
remain a cultural phenomenon.
""")

# -------------------------------
# Section 1: Sholay Posters / Images
# -------------------------------
st.header("🖼️ Sholay Posters & Stills")
col1, col2 = st.columns(2)

with col1:
    st.image(
        "https://upload.wikimedia.org/wikipedia/en/5/52/Sholay-poster.jpg",
        caption="Official Poster of Sholay",
        use_container_width=True
    )
    # Local cast image
    st.image(
        r"C:\Users\jadej\OneDrive\Desktop\sholay_cast",
        caption="Iconic Cast of Sholay",
        use_container_width=True
    )

# -------------------------------
# Section 2: Sholay Movie Information
# -------------------------------
basic_path = r"C:\Users\jadej\OneDrive\Desktop\Sholay_Formatted_Datasheet.xlsx"
cast_path = r"C:\Users\jadej\OneDrive\Desktop\cast_datasheet(1).xlsx"

try:
    basic_info = pd.read_excel(basic_path, sheet_name="Basic Info")
except Exception as e:
    basic_info = None
    st.error(f"❌ Could not load Basic Info: {e}")

try:
    cast = pd.read_excel(cast_path)
except Exception as e:
    cast = None
    st.error(f"❌ Could not load Cast sheet: {e}")

with st.expander("📌 Basic Information", expanded=False):
    if basic_info is not None:
        basic_info = basic_info.reset_index(drop=True)
        basic_info.index = basic_info.index + 1
        basic_info.index.name = "S.No"
        basic_info = basic_info.rename(columns={"Field": "Attribute", "Details": "Information"})
        st.table(basic_info)
    else:
        st.warning("⚠️ 'Basic Info' sheet not found!")

# -------------------------------
# Cast
# -------------------------------
st.header("🎭 Cast & Roles")
if cast is not None:
    st.dataframe(cast)
    if "Actor" in cast.columns and "Screen Time (mins)" in cast.columns:
        fig_cast = px.bar(
            cast.sort_values("Screen Time (mins)", ascending=False),
            x="Actor", y="Screen Time (mins)", color="Actor",
            title="Cast Screen Time Distribution", text="Screen Time (mins)"
        )
        fig_cast.update_traces(texttemplate='%{text:.1f}', textposition="outside")
        st.plotly_chart(fig_cast, use_container_width=True)

        fig_pie = px.pie(cast, names="Actor", values="Screen Time (mins)", title="Screen Time Share by Actor")
        st.plotly_chart(fig_pie, use_container_width=True)


# -------------------------------
# Movie Highlights
# -------------------------------
st.header("🌟 Movie Highlights")
highlights = [
    "Ran for over 5 years at Minerva Theatre, Mumbai.",
    "First Indian 'Curry Western'.",
    "Iconic dialogues: *Kitne aadmi the?*, *Yeh haath mujhe de de Thakur!*",
    "Filmed in Ramanagara (Karnataka), now known as 'Sholay Hills'.",
    "Songs like *Yeh Dosti* and *Mehbooba Mehbooba* are evergreen classics."
]
for h in highlights:
    st.markdown(f"- {h}")

# -------------------------------
# 1975 Hindi Films Overview
# -------------------------------
st.header("📊 1975 Hindi Films: Budget vs Box Office")
file_path = r"C:\Users\jadej\Downloads\1975_Hindi_Films_Budget_vs_BoxOffice.xlsx"

try:
    df = pd.read_excel(file_path)
except Exception as e:
    st.error(f"❌ Could not load 1975 films data: {e}")
    st.stop()

st.subheader("📑 1975 Films Data Table")
st.dataframe(df)

fig = go.Figure()
fig.add_trace(go.Bar(x=df["Film"], y=df["Budget (₹ crore)"], name="Budget (₹ crore)", marker_color="skyblue"))
fig.add_trace(go.Bar(x=df["Film"], y=df["Box Office (₹ crore)"], name="Box Office (₹ crore)", marker_color="orange"))
fig.update_layout(
    title="1975 Hindi Films: Budget vs Box Office",
    xaxis_title="Films", yaxis_title="Amount (₹ crore)", barmode="group", template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

top_film = df.loc[df["Box Office (₹ crore)"].idxmax(), "Film"]
st.subheader("💡 Insights")
st.write(f"- The **highest grossing film** of 1975 was **{top_film}**.")

# -------------------------------
# Awards
# -------------------------------
st.header("🏆 Awards & Recognition")
awards = [
    "Filmfare Award for Best Editing (M. S. Shinde).",
    "Nominated for Best Film, Best Director, Best Actor, Best Actress.",
    "Declared 'Film of the Millennium' by BBC India."
]
for a in awards:
    st.markdown(f"- {a}")

# -------------------------------
# Legacy
# -------------------------------
st.header("📖 Legacy")
legacy = [
    "Established Amitabh Bachchan as the 'angry young man'.",
    "Gabbar Singh became Bollywood's most iconic villain.",
    "Still re-released in cinemas after 40+ years.",
    "A benchmark in Indian cinema history."
]
for l in legacy:
    st.markdown(f"- {l}")

