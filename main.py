import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
import logging
import os
from typing import Tuple, Dict, Optional, Any

from dotenv import load_dotenv
from google import genai
from google.genai import types

import config

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables securely
load_dotenv()


def init_genai_client() -> Optional[Any]:
    """
    Initializes the Google GenAI client using the new google-genai SDK.

    Configures the client with the API key from environment variables.
    Returns None if the key is missing or invalid to allow graceful degradation.

    Returns:
        google.genai.Client: Configured client, or None if API key is invalid.
    """
    api_key: str = os.getenv("GOOGLE_API_KEY", "")
    if not api_key or api_key == "your_google_api_key_here":
        logger.warning("GOOGLE_API_KEY not configured. AI features will be disabled.")
        return None

    client = genai.Client(api_key=api_key)
    logger.info("Google GenAI client initialized successfully.")
    return client


def generate_simulated_data() -> Tuple[Dict[str, int], Dict[str, int]]:
    """
    Generates simulated real-time IoT telemetry for stadium operations.

    Simulates data for stadium gate crowd density and concession stand
    wait times, mimicking a live sensor feed.

    Returns:
        Tuple[Dict[str, int], Dict[str, int]]: A tuple of (gate_occupancy, concession_waits)
            where values are integers representing percentage and minutes respectively.
    """
    gate_occupancy: Dict[str, int] = {
        gate: random.randint(config.GATE_OCCUPANCY_MIN, config.GATE_OCCUPANCY_MAX)
        for gate in config.GATE_NAMES
    }
    concession_waits: Dict[str, int] = {
        stand: random.randint(config.CONCESSION_WAIT_MIN, config.CONCESSION_WAIT_MAX)
        for stand in config.CONCESSION_NAMES
    }
    return gate_occupancy, concession_waits


def sanitize_prompt(prompt: str) -> bool:
    """
    Validates user input against known prompt injection attack patterns.

    Performs a case-insensitive check against a configurable blacklist of
    injection patterns to protect the system prompt integrity.

    Args:
        prompt (str): The raw user input string to validate.

    Returns:
        bool: True if the input is safe, False if a potential injection is detected.
    """
    prompt_lower: str = prompt.lower().strip()
    for pattern in config.PROMPT_INJECTION_BLACKLIST:
        if pattern in prompt_lower:
            logger.warning("Prompt injection attempt detected: '%s'", prompt[:50])
            return False
    return True


def get_flow_status(max_gate_occupancy: int) -> Tuple[str, str]:
    """
    Determines overall gate flow status based on peak occupancy.

    Args:
        max_gate_occupancy (int): The highest occupancy percentage among all gates.

    Returns:
        Tuple[str, str]: A tuple of (status_label, css_class).
    """
    if max_gate_occupancy > config.GATE_CRITICAL_THRESHOLD:
        return "CRITICAL", "critical"
    elif max_gate_occupancy > config.GATE_WARNING_THRESHOLD:
        return "MODERATE", "warning"
    return "OPTIMAL", "optimal"


def get_bar_color(occupancy: int) -> str:
    """
    Returns the appropriate hex color for a gate bar based on occupancy.

    Args:
        occupancy (int): Gate occupancy percentage (0-100).

    Returns:
        str: Hex color string.
    """
    if occupancy < config.GATE_WARNING_THRESHOLD:
        return config.COLOR_OPTIMAL
    elif occupancy <= config.GATE_CRITICAL_THRESHOLD:
        return config.COLOR_WARNING
    return config.COLOR_CRITICAL


def get_concession_color(wait_time: int) -> str:
    """
    Returns the appropriate hex color for a concession stand based on wait time.

    Args:
        wait_time (int): Wait time in minutes.

    Returns:
        str: Hex color string.
    """
    if wait_time < config.CONCESSION_WARNING_THRESHOLD:
        return config.COLOR_OPTIMAL
    elif wait_time < config.CONCESSION_CRITICAL_THRESHOLD:
        return config.COLOR_WARNING
    return config.COLOR_CRITICAL


def get_ai_response(
    client: Any,
    gate_data: Dict[str, int],
    food_data: Dict[str, int],
    user_prompt: str,
) -> str:
    """
    Generates a context-aware AI response using live stadium telemetry.

    Constructs a system prompt injected with real-time data and queries
    the Gemini model using the google-genai SDK.

    Args:
        client: The initialized google.genai.Client instance.
        gate_data (Dict[str, int]): Live gate occupancy percentages.
        food_data (Dict[str, int]): Live concession wait times in minutes.
        user_prompt (str): The sanitized user question.

    Returns:
        str: The AI-generated response text.

    Raises:
        Exception: Re-raises any API or network errors after logging.
    """
    system_context = (
        "You are the VibeFlow Stadium Command AI, a high-tech, fast, and precise assistant "
        "for managing fan flow and stadium operations.\n\n"
        f"REAL-TIME LIVE DATA:\n"
        f"- Gate Sector Loads (%): {gate_data} (Lower is better for entry/exit)\n"
        f"- Concession Wait Times (mins): {food_data} (Lower is better)\n\n"
        "Respond directly to the fan's query using this live data. Keep answers short, "
        "dynamic, and action-oriented. Provide 'Smart Route' recommendations when asked. "
        "Do not explain your data source."
    )

    try:
        response = client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=[system_context, user_prompt],
            config=types.GenerateContentConfig(
                temperature=config.GENERATION_TEMPERATURE,
                max_output_tokens=config.GENERATION_MAX_TOKENS,
                top_p=config.GENERATION_TOP_P,
                safety_settings=[
                    types.SafetySetting(
                        category="HARM_CATEGORY_HARASSMENT",
                        threshold="BLOCK_MEDIUM_AND_ABOVE",
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_HATE_SPEECH",
                        threshold="BLOCK_MEDIUM_AND_ABOVE",
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        threshold="BLOCK_MEDIUM_AND_ABOVE",
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_DANGEROUS_CONTENT",
                        threshold="BLOCK_MEDIUM_AND_ABOVE",
                    ),
                ],
            ),
        )
        return response.text
    except Exception as e:
        logger.error("Gemini API call failed: %s", str(e))
        raise


@st.cache_data
def load_css() -> str:
    """
    Caches and returns the application's custom CSS.

    Using @st.cache_data prevents this string from being recomputed on
    every rerun, improving rendering efficiency.

    Returns:
        str: Full CSS stylesheet as an HTML string.
    """
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Share+Tech+Mono&display=swap');
        html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
        [data-testid="collapsedControl"] { display: none; }
        .main .block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1500px; }
        .metric-card-optimal, .metric-card-warning, .metric-card-critical {
            background: linear-gradient(145deg, #111111 0%, #080808 100%);
            border-radius: 8px; padding: 15px 10px; text-align: center;
            border-top: 3px solid; box-shadow: 0 8px 15px rgba(0,0,0,0.5);
            position: relative; overflow: hidden;
        }
        .metric-card-optimal::before, .metric-card-warning::before, .metric-card-critical::before {
            content: ""; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
            background-size: 10px 10px; pointer-events: none; opacity: 0.5;
        }
        .metric-card-optimal { border-top-color: #ff6f00; }
        .metric-card-warning  { border-top-color: #faca2b; }
        .metric-card-critical { border-top-color: #ff4b4b; }
        .metric-value {
            font-family: 'Share Tech Mono', monospace; font-size: 2.2rem;
            font-weight: 400; margin-top: 5px; white-space: nowrap;
            text-shadow: 0 0 10px rgba(255,255,255,0.1);
        }
        .value-optimal { color: #ff6f00; text-shadow: 0 0 15px rgba(255,111,0,0.5); }
        .value-warning  { color: #faca2b; text-shadow: 0 0 15px rgba(250,202,43,0.5); }
        .value-critical { color: #ff4b4b; text-shadow: 0 0 15px rgba(255,75,75,0.5); }
        .metric-label { font-size: 0.8rem; color: #aaaaaa; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
        h1 { font-weight: 800; font-style: italic; background: -webkit-linear-gradient(45deg, #ff6f00, #ffffff);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px; text-transform: uppercase; }
        h2, h3, h4 { font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #f0f0f0; }
        .stChatFloatingInputContainer { padding-bottom: 20px; }
        .sports-panel { background: #0f0f0f; border-radius: 8px; padding: 20px; margin-top: 15px;
                        box-shadow: inset 0 0 20px rgba(0,0,0,0.8); border: 1px solid #1a1a1a; }
        .food-stand { background: #151515; padding: 15px 10px; border-radius: 5px;
                      text-align: center; border-left: 4px solid #333; font-family: 'Share Tech Mono', monospace; }
    </style>
    """


# ────────────────────────────────────────────────────────────────────────────
# STREAMLIT APP
# ────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

client = init_genai_client()
st.markdown(load_css(), unsafe_allow_html=True)

# --- Session State Initialization ---
if "data" not in st.session_state:
    st.session_state.data = generate_simulated_data()
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Stadium Command AI initialized. Ask me for real-time routing or concession updates.",
        }
    ]


def pulse_data() -> None:
    """Triggers a manual refresh of the simulated telemetry data."""
    st.session_state.data = generate_simulated_data()
    logger.info("Telemetry data manually refreshed.")


# --- Top Header ---
col_head1, col_head2 = st.columns([5, 1])
with col_head1:
    st.title(config.APP_TITLE)
with col_head2:
    st.write("")
    st.button("⚡ SYNC FEED", on_click=pulse_data, use_container_width=True)

st.markdown("<hr style='margin: 0.5em 0; border-color: #333;'>", unsafe_allow_html=True)

gate_data, food_data = st.session_state.data

# --- Main Layout ---
main_left, main_right = st.columns([1.3, 1], gap="medium")

with main_left:
    st.markdown("### Live Matchday Operations")

    total_attendance_est: int = sum(gate_data.values()) * 150
    avg_wait: int = sum(food_data.values()) // len(food_data)
    max_gate: int = max(gate_data.values())
    flow_status, flow_class = get_flow_status(max_gate)
    wait_class: str = (
        "optimal" if avg_wait < config.CONCESSION_WARNING_THRESHOLD
        else ("warning" if avg_wait < config.CONCESSION_CRITICAL_THRESHOLD else "critical")
    )

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            f'<div class="metric-card-optimal" role="status" aria-label="Estimated Attendance">'
            f'<div class="metric-label" aria-hidden="true">Est. Attendance</div>'
            f'<div class="metric-value value-optimal" aria-live="polite">{total_attendance_est:,}</div></div>',
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f'<div class="metric-card-{wait_class}" role="status" aria-label="Average Concession Wait">'
            f'<div class="metric-label" aria-hidden="true">Avg Concession Wait</div>'
            f'<div class="metric-value value-{wait_class}" aria-live="polite">{avg_wait}M</div></div>',
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f'<div class="metric-card-{flow_class}" role="status" aria-label="Gate Flow Status">'
            f'<div class="metric-label" aria-hidden="true">Gate Flow</div>'
            f'<div class="metric-value value-{flow_class}" aria-live="polite">{flow_status}</div></div>',
            unsafe_allow_html=True,
        )

    # Density Chart
    st.markdown("<div class='sports-panel' role='region' aria-label='Sector Density Report'>", unsafe_allow_html=True)
    st.markdown("#### Sector Density")
    df_gates = pd.DataFrame(list(gate_data.items()), columns=["Gate", "Occupancy"])
    df_gates["Color"] = df_gates["Occupancy"].apply(get_bar_color)

    fig = go.Figure(
        data=[
            go.Bar(
                x=df_gates["Gate"],
                y=df_gates["Occupancy"],
                marker_color=df_gates["Color"],
                text=df_gates["Occupancy"].apply(lambda x: f"{x}%"),
                textposition="auto",
                textfont=dict(family="Share Tech Mono", size=14, color="white"),
                hovertemplate="<b>%{x}</b><br>Load: %{y}%<extra></extra>",
                marker_line_width=0,
            )
        ]
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color="#f0f0f0", font_family="Outfit", showlegend=False,
        yaxis=dict(range=[0, 100], gridcolor="rgba(255,255,255,0.05)", title="", showticklabels=False),
        xaxis=dict(title="", showgrid=False, tickfont=dict(size=12, family="Outfit")),
        margin=dict(l=0, r=0, t=10, b=0), height=220,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Concessions
    st.markdown("#### Concessions Status")
    food_cols = st.columns(3)
    for i, (stand, wait) in enumerate(food_data.items()):
        color = get_concession_color(wait)
        with food_cols[i % 3]:
            st.markdown(
                f"<div class='food-stand' style='border-left-color: {color};' "
                f"role='status' aria-label='Wait time for {stand}'>"
                f"<div style='font-family:Outfit;font-size:0.8rem;color:#888;text-transform:uppercase;' aria-hidden='true'>{stand}</div>"
                f"<div style='font-size:1.4rem;color:{color};' aria-live='polite'>{wait} MIN</div></div>",
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

with main_right:
    st.markdown("### ⚡ Smart Routing AI")

    chat_container = st.container(border=True)
    with chat_container:
        for msg in st.session_state.messages:
            avatar = "⚡" if msg["role"] == "assistant" else "👤"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

    if user_input := st.chat_input("E.g., Which gate has the shortest wait?"):
        if not sanitize_prompt(user_input):
            st.error("🔒 Unsafe prompt detected. Request blocked by Security Filter.")
        else:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with chat_container:
                with st.chat_message("user", avatar="👤"):
                    st.markdown(user_input)
                with st.chat_message("assistant", avatar="⚡"):
                    if client:
                        try:
                            with st.spinner("Analyzing stadium telemetry..."):
                                reply = get_ai_response(client, gate_data, food_data, user_input)
                                st.markdown(reply)
                                st.session_state.messages.append({"role": "assistant", "content": reply})
                        except Exception:
                            st.error("Connection to AI network interrupted. Please retry.")
                    else:
                        fallback = "Please configure your `GOOGLE_API_KEY` in the `.env` file."
                        st.warning(fallback)
                        st.session_state.messages.append({"role": "assistant", "content": fallback})
