---
title: "Building VibeFlow: A Real-Time AI Stadium Command Center with Gemini 2.5 Flash"
published: false
description: "How I built a High-Vis sports dashboard for the PromptWars challenge using Streamlit, Plotly, and Gemini 2.5 Flash."
tags: "python, ai, streamlit, promptwars"
---

# 🏟️ Building VibeFlow: A Real-Time AI Stadium Command Center

If you've ever been to a massive sporting event or a stadium concert, you know the struggle: you're hungry, but you don't know which concession stand has the shortest line. Or the game ends, and you're stuck in a 40-minute bottleneck at the main gate. 

For the **PromptWars Challenge**, I set out to solve this exact problem. 

Enter **VibeFlow** — a real-time, AI-powered stadium management dashboard designed to monitor crowd density and intelligently route fans using generative AI. 

Here is a breakdown of how I built it, the tech stack I used, and how I turned a standard chatbot into a context-aware "Smart Routing AI."

---

## 🛠️ The Tech Stack

I wanted the dashboard to be fast, interactive, and visually striking. I chose:
*   **Frontend & Framework**: [Streamlit](https://streamlit.io/) – The fastest way to build Python data apps.
*   **Data Visualization**: [Plotly](https://plotly.com/) – For creating the live density map.
*   **Generative AI**: `gemini-2.5-flash` via the `google-generativeai` SDK.
*   **Styling**: Pure CSS injected via Streamlit markdown to achieve a unique "High-Vis Orange Scoreboard" aesthetic. 

---

## 🎨 The Design: Breaking the "Boring Dashboard" Mold

Most data dashboards look like spreadsheets on steroids. Because VibeFlow is designed for the sports and entertainment sector, it needed to feel like a **Command Center**. 

I used custom CSS to inject a dark mode theme (`#050505` background), paired with `Outfit` (sans-serif) and `Share Tech Mono` (digital/scoreboard) fonts. The real magic comes from the **High-Vis Orange (`#ff6f00`)** accents, complete with glassmorphism effects, dynamic glowing drop-shadows on metric cards, and a subtle grid pattern that mimics the look of a giant stadium Jumbotron. 

---

## ⚡ The Core Features

### 1. Live Telemetry & Data Pulse
To make the app realistic, I built a `pulse_data()` function that simulates live IoT feeds. It tracks:
*   **Sector Density**: Occupancy percentages for four main stadium gates.
*   **Concession Waits**: Live wait times (in minutes) for three major food stands.

Every time the user clicks **"⚡ SYNC FEED"**, the data randomizes. The UI instantly updates: bars on the Plotly chart shift, and status indicators flash Green (Optimal), Yellow (Warning), or Red (Critical) depending on the load.

### 2. Context-Aware "Smart Routing AI"
This is where the PromptWars magic happens. 

Instead of just slapping a generic ChatGPT wrapper on the side of the screen, I integrated `gemini-2.5-flash` and gave it a very specific persona: **The VibeFlow Stadium Command AI**. 

Every time a user asks a question (e.g., *"Which gate has the shortest wait?"*), the app injects the *current, live* stadium data directly into the system prompt:

```python
context = f"""
You are the VibeFlow Stadium Command AI, a high-tech, fast, and precise assistant for managing fan flow and stadium operations.

REAL-TIME LIVE DATA:
- Gate Sector Loads (%): {gate_data} (Lower is better for entry/exit)
- Concession Wait Times (mins): {food_data} (Lower is better)

Respond directly to the fan's query using this live data. Keep your answers short, dynamic, and action-oriented. Give them a "Smart Route" recommendation if they ask for directions. Do not explain where you got the data.
"""
```

Because the AI is contextually aware of the exact state of the dashboard, if the North Gate suddenly hits 95% capacity, the AI will actively tell fans to avoid it and route them to the South Gate instead. **It turns a reactive chatbot into a proactive, data-driven navigation tool.**

---

## 🚀 Deployment

The app is fully containerized using a lightweight `Dockerfile` that exposes port `8080`, making it a breeze to deploy on platforms like Google Cloud Run. 

---

## 🏆 Final Thoughts

Building VibeFlow for PromptWars was a fantastic experience in bridging data visualization with Generative AI. It proves that LLMs are incredibly powerful when you don't just ask them questions, but rather feed them real-time telemetry and give them a highly specific task. 

If you want to check out the code, run it locally, or try out the AI prompts yourself, check out the repository!

**[Link to your GitHub Repo here!]**

*Have you built any cool tools with Gemini 2.5 Flash? Let me know in the comments!*
