import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure GenAI
api_key = os.getenv("GOOGLE_API_KEY")
if api_key and api_key != "your_google_api_key_here":
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    model = None

# --- Page Config ---
st.set_page_config(page_title="VibeFlow Stadium", page_icon="🏟️", layout="wide", initial_sidebar_state="collapsed")



# --- Custom CSS for Unique Sports Dashboard Styling ---
st.markdown("""
<style>
    /* Google Fonts: Outfit for sleek text, Share Tech Mono for the Scoreboard feel */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Share+Tech+Mono&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Outfit', sans-serif;
    }

    /* Hide Sidebar completely */
    [data-testid="collapsedControl"] { display: none; }
    
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    /* Unique Sports Touch: Scoreboard Metric Cards */
    .metric-card-optimal, .metric-card-warning, .metric-card-critical {
        background: linear-gradient(145deg, #111111 0%, #080808 100%);
        border-radius: 8px;
        padding: 15px 10px;
        text-align: center;
        border-top: 3px solid;
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    /* Subtle grid pattern inside cards to look like a stadium screen */
    .metric-card-optimal::before, .metric-card-warning::before, .metric-card-critical::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 10px 10px;
        pointer-events: none;
        opacity: 0.5;
    }

    .metric-card-optimal { border-top-color: #ff6f00; }
    .metric-card-warning { border-top-color: #faca2b; }
    .metric-card-critical { border-top-color: #ff4b4b; }

    /* Fix text wrapping: adjust font size and word-break */
    .metric-value {
        font-family: 'Share Tech Mono', monospace;
        font-size: 2.2rem;
        font-weight: 400;
        margin-top: 5px;
        white-space: nowrap;
        text-shadow: 0 0 10px rgba(255,255,255,0.1);
    }
    .value-optimal { color: #ff6f00; text-shadow: 0 0 15px rgba(255,111,0,0.5); }
    .value-warning { color: #faca2b; text-shadow: 0 0 15px rgba(250,202,43,0.5); }
    .value-critical { color: #ff4b4b; text-shadow: 0 0 15px rgba(255,75,75,0.5); }

    .metric-label {
        font-size: 0.8rem;
        color: #aaaaaa;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    /* Headers */
    h1 {
        font-weight: 800;
        font-style: italic;
        background: -webkit-linear-gradient(45deg, #ff6f00, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        text-transform: uppercase;
    }
    h2, h3, h4 {
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #f0f0f0;
    }

    .stChatFloatingInputContainer {
        padding-bottom: 20px;
    }
    
    .sports-panel {
        background: #0f0f0f;
        border-radius: 8px;
        padding: 20px;
        margin-top: 15px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
        border: 1px solid #1a1a1a;
    }

    .food-stand {
        background: #151515;
        padding: 15px 10px;
        border-radius: 5px;
        text-align: center;
        border-left: 4px solid #333;
        font-family: 'Share Tech Mono', monospace;
    }
    

</style>
""", unsafe_allow_html=True)

# --- Data Simulation ---
def generate_simulated_data():
    gates = ["North Gate", "South Gate", "East Gate", "West Gate"]
    gate_occupancy = {gate: random.randint(10, 95) for gate in gates}
    
    concessions = ["The Grill", "Sushi Bar", "Vegan Eats"]
    concession_waits = {stand: random.randint(2, 25) for stand in concessions}
    
    return gate_occupancy, concession_waits

# Initialize state
if "data" not in st.session_state:
    st.session_state.data = generate_simulated_data()



# Pulse Action
def pulse_data():
    st.session_state.data = generate_simulated_data()



# --- Top Header ---
col_head1, col_head2 = st.columns([5, 1])
with col_head1:
    st.title("VibeFlow // Stadium Command")
with col_head2:
    st.write("") # Spacing
    st.button("⚡ SYNC FEED", on_click=pulse_data, use_container_width=True)

st.markdown("<hr style='margin: 0.5em 0; border-color: #333;'>", unsafe_allow_html=True)

gate_data, food_data = st.session_state.data



# --- Main Layout (2 Columns) ---
main_left, main_right = st.columns([1.3, 1], gap="medium")

with main_left:
    st.markdown("### Live Matchday Operations")
    
    # Calculate metrics
    total_attendance_est = sum(gate_data.values()) * 150
    avg_wait = sum(food_data.values()) // len(food_data)
    max_gate = max(gate_data.values())
    
    if max_gate > 80:
        flow_status, flow_class = "CRITICAL", "critical"
    elif max_gate > 50:
        flow_status, flow_class = "MODERATE", "warning"
    else:
        flow_status, flow_class = "OPTIMAL", "optimal"

    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.markdown(f'<div class="metric-card-optimal"><div class="metric-label">Est. Attendance</div><div class="metric-value value-optimal">{total_attendance_est:,}</div></div>', unsafe_allow_html=True)
        
    with m2:
        wait_class = "optimal" if avg_wait < 10 else ("warning" if avg_wait < 20 else "critical")
        st.markdown(f'<div class="metric-card-{wait_class}"><div class="metric-label">Avg Concession Wait</div><div class="metric-value value-{wait_class}">{avg_wait}M</div></div>', unsafe_allow_html=True)
        
    with m3:
        st.markdown(f'<div class="metric-card-{flow_class}"><div class="metric-label">Gate Flow</div><div class="metric-value value-{flow_class}">{flow_status}</div></div>', unsafe_allow_html=True)

    # --- Live Density Map ---
    st.markdown("<div class='sports-panel'>", unsafe_allow_html=True)
    st.markdown("#### Sector Density")
    df_gates = pd.DataFrame(list(gate_data.items()), columns=["Gate", "Occupancy"])
    
    def get_color(occ):
        if occ < 50: return "#ff6f00"
        elif occ <= 80: return "#faca2b"
        else: return "#ff4b4b"
        
    df_gates["Color"] = df_gates["Occupancy"].apply(get_color)

    fig = go.Figure(data=[
        go.Bar(
            x=df_gates["Gate"],
            y=df_gates["Occupancy"],
            marker_color=df_gates["Color"],
            text=df_gates["Occupancy"].apply(lambda x: f"{x}%"),
            textposition="auto",
            textfont=dict(family="Share Tech Mono", size=14, color="white"),
            hovertemplate="<b>%{x}</b><br>Load: %{y}%<extra></extra>",
            marker_line_width=0
        )
    ])

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#f0f0f0",
        font_family="Outfit",
        showlegend=False,
        yaxis=dict(range=[0, 100], gridcolor="rgba(255,255,255,0.05)", title="", showticklabels=False),
        xaxis=dict(title="", showgrid=False, tickfont=dict(size=12, family="Outfit")),
        margin=dict(l=0, r=0, t=10, b=0),
        height=220
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Food Stand Status
    st.markdown("#### Concessions Status")
    food_cols = st.columns(3)
    for i, (stand, wait) in enumerate(food_data.items()):
        status_color = "#ff6f00" if wait < 10 else ("#faca2b" if wait < 20 else "#ff4b4b")
        with food_cols[i % 3]:
            st.markdown(f"<div class='food-stand' style='border-left-color: {status_color};'><div style='font-family: Outfit; font-size: 0.8rem; color: #888; text-transform: uppercase;'>{stand}</div><div style='font-size: 1.4rem; color: {status_color};'>{wait} MIN</div></div>", unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)

with main_right:
    # --- AI Fan Concierge ---
    st.markdown("### ⚡ Smart Routing AI")
    
    chat_container = st.container(border=True)
    
    with chat_container:
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Stadium Command AI initialized. Ask me for real-time routing or concession updates."}
            ]

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar="⚡" if msg["role"] == "assistant" else "👤"):
                st.markdown(msg["content"])

    if prompt := st.chat_input("E.g., Which gate has the shortest wait?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with chat_container:
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)
            
            with st.chat_message("assistant", avatar="⚡"):
                if model:
                    context = f"You are the VibeFlow Stadium Command AI, a high-tech, fast, and precise assistant for managing fan flow and stadium operations. REAL-TIME LIVE DATA: - Gate Sector Loads (%): {gate_data} (Lower is better for entry/exit) - Concession Wait Times (mins): {food_data} (Lower is better). Respond directly to the fan's query using this live data. Keep your answers short, dynamic, and action-oriented. Give them a 'Smart Route' recommendation if they ask for directions. Do not explain where you got the data."
                    try:
                        with st.spinner("Analyzing stadium telemetry..."):
                            response = model.generate_content([context, prompt])
                            st.markdown(response.text)
                            st.session_state.messages.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error(f"Telemetry error: {e}")
                else:
                    msg = "Please configure your `GOOGLE_API_KEY` in the `.env` file to access the AI network."
                    st.warning(msg)
                    st.session_state.messages.append({"role": "assistant", "content": msg})
    

