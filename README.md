# Amadeus Voicebot

## Project Overview
Amadeus Voicebot is a voice-based interactive system designed to manage conversations and metadata between a Millis interface and a Streamlit app. The project consists of two primary components:

1. **api_call.py** - This script handles the backend API calls, managing the conversation and metadata exchange between Millis and the Streamlit app.
2. **visual_voicebot_main.py** - This is the Streamlit application that provides a visual interface for the Millis App, demonstrating the voicebot's capabilities.
3. **practice_main.py** - This is the Streamlit application that provides a visual interface for the Millis App, demonstrating the voicebot's capabilities.

Additionally, this project includes two Proof of Concepts (POCs):

### 1. Visual Bot
This POC provides step-by-step guidance using voice while displaying written guidance in real-time alongside it. It is designed to help users follow instructions effectively with both auditory and visual aids.

### 2. Practice Simulation
This POC is a simulation tool where trainee agents can interact with an AI-powered customer voicebot. It walks the trainee through step-by-step processes for handling queries and provides a detailed scorecard and report at the end to evaluate their performance.

## API Endpoints
The following APIs are hosted in **api_call.py**:

- `receive_step_details`
- `get_step_details`
- `reset_step_details`
- `receive_transcript`
- `get_transcript`
- `reset_transcript`

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd Amadeus-Voicebot
   ```

2. **Set Up Virtual Environment**
   Ensure you have Python installed. Then, create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   Make sure to install all required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Run the API Server**
   To start the backend API server on port 8502:
   ```bash
   python api_call.py
   ```

2. **Run the Streamlit App**
   To launch the Streamlit app on port 8504:
   ```bash
   python -m streamlit run visual_voicebot_main.py --server.port 8504
   ```
3. **Run the Streamlit App for Practice**
   To launch the Streamlit app on port 8505:
   ```bash
   python -m streamlit run practice_main.py --server.port 8505
   ```


## Project Structure
```
Amadeus-Voicebot/
├── api_call.py
├── prompts.py
├── llm_generation.py
├── practice_main.py
├── visual_voicebot_main.py
├── venv/
├── .streamlit/
├── requirements.txt
└── README.md
```

## Notes
- Ensure that both the API server and the Streamlit app are running simultaneously for full functionality.
- Adjust the port numbers if necessary to avoid conflicts with other services on your machine.

---

For any queries or contributions, please reach out to anukrit.jain@aionos.ai or abhi.srivastava@aionos.ai.

