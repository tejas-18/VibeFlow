# 🏟️ VibeFlow - Stadium Command Center

VibeFlow is a real-time, interactive stadium management dashboard built for the **PromptWars Challenge**. The goal of VibeFlow is to improve the stadium experience for attendees by intelligently managing crowd movement, monitoring concession wait times, and utilizing generative AI to provide dynamic "Smart Routing."

The application features a unique, high-energy **High-Vis Orange Scoreboard** aesthetic designed specifically for the sports sector.

---

## ⚡ Key Features

1. **Live Density Map Dashboard**: A real-time, color-coded visual representation of stadium gate occupancy (using Plotly).
2. **Concession Telemetry**: Live monitoring of wait times across all major food stands.
3. **Smart Routing AI**: Powered by `gemini-2.5-flash`, the integrated AI concierge dynamically reads the live stadium telemetry to give fans the absolute best routes and recommendations to avoid bottlenecks.
4. **Data Pulse Engine**: Simulates a live IoT data feed. Every time you hit "SYNC FEED", the dashboard randomizes the occupancy and wait times, forcing the AI to dynamically update its strategies.

---

## 🛠️ Setup & Installation

### Local Deployment
1. Ensure you have Python 3.10+ installed.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Google API Key:
   - Open the `.env` file.
   - Replace `your_google_api_key_here` with your actual Google Gemini API key.
4. Run the Streamlit application:
   ```bash
   streamlit run main.py
   ```

### Docker / Cloud Run Deployment
A production-ready `Dockerfile` is included to deploy easily to Google Cloud Run.
1. Build the image:
   ```bash
   docker build -t vibeflow .
   ```
2. Run the container locally (passing your API key):
   ```bash
   docker run -p 8080:8080 -e GOOGLE_API_KEY="your_api_key" vibeflow
   ```

---

## 🤖 Smart Routing AI: Sample Prompts

The embedded AI Concierge uses the *actual* data currently displayed on the dashboard. Every time you "SYNC FEED", the AI's answers will change based on the new conditions. 

Here are some sample prompts you can try:

### Fan Routing
* *"I'm arriving at the stadium now, which gate is the absolute fastest to get through?"*
* *"The North Gate looks packed. What is my best alternative?"*
* *"I'm parked near the East Gate, is it safe to enter there or should I walk around?"*

### Concession Management
* *"I'm starving. Where is the absolute shortest line to get food right now?"*
* *"I really want sushi, but is it worth the wait compared to the other stands?"*
* *"Which food stand is currently struggling the most with wait times?"*

### Advanced Operations
* *"Give me a quick summary of the current stadium bottlenecks."*
* *"I want to grab food and then find my seat. Give me a strategy on which gate to enter and which stand to hit up based on the current loads."*

---

*Built with Streamlit, Plotly, and Google Gemini.*
