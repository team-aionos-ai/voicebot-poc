import streamlit as st
import streamlit.components.v1 as components
import requests
import time
import json
from llm_generation import get_solutions_from_openai
from prompts import feedback_prompt, scorecard_prompt
import concurrent.futures

# Set page configuration
st.set_page_config(
    layout="wide",
    page_title="Amadeus Voicebot",
)

# Function to reset API data
def call_reset_api():
    reset_endpoint = "http://13.201.227.194:8502/reset_transcript"
    try:
        response = requests.post(reset_endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to reset. Status code: {response.status_code}, Response: {response.text}"}
    except Exception as e:
        return {"error": str(e)}
    
# Define functions to be executed in parallel
def fetch_openai_response(prompt, transcript):
    response = get_solutions_from_openai(prompt, str(transcript))
    return json.loads(response)

# Function to fetch transcript data
def fetch_transcript(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return None

# Function to determine background and text colors based on score
def get_dynamic_colors(score):
    if score <= 1:
        return "#ffebeb", "#d9534f", "#6b6b6b"
    elif score == 2:
        return "#fff4e5", "#ff9800", "#6b6b6b"
    elif score == 3:
        return "#ffffe5", "#f9a825", "#6b6b6b"
    elif score == 4:
        return "#e8f5e9", "#4caf50", "#6b6b6b"
    else:
        return "#e0f2f1", "#00796b", "#6b6b6b"

# Function to display Evaluation and Feedback tabs
def display_tabs(openai_response, scorecard_data):
    tabs = st.tabs(["Scorecard","Evaluation", "Feedback"])
    
    #Scorecard
    with tabs[0]:
        # st.markdown("## Scorecard")
        
        columns = st.columns(2)  # Arrange categories in two columns for better space usage
        category_index = 0
        
        for category, details in scorecard_data["Scorecard"].items():
            score = sum(1 for decision in details.values() if decision == "Yes")  # Calculate score (0-3)
            total = len(details)

            with columns[category_index % 2]:  # Alternate categories between two columns
                with st.container(border = True):
                    st.markdown(
                        f"""
                        <div style='display: flex; justify-content: space-between; align-items: center; padding: 10px; border-radius: 8px; margin-bottom: 10px;'>
                            <span style='font-weight: bold; font-size: 16px;'>{category}</span>
                            <span style='background-color: #EAEAEA; color: #333333; padding: 4px 10px; border-radius: 12px; font-size: 14px; font-weight: 500;'>
                                {score}/{total}
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    # st.markdown(
                    #     f"""
                    #     <div style='display: flex; justify-content: space-between; align-items: center;'>
                    #         <span style='font-weight: bold; font-size: 16px;'>{category}</span>
                    #         <span style='background-color: #007bff; color: white; padding: 6px 12px; border-radius: 20px; font-size: 14px;'>
                    #             {score}/3
                    #         </span>
                    #     </div>
                    #     """,
                    #     unsafe_allow_html=True
                    # )
                    
                    for parameter, decision in details.items():
                        status_icon = "✅" if decision == "Yes" else "❌"
                        status_color = "#388E3C" if decision == "Yes" else "#D32F2F"
                        
                        st.markdown(
                            f"""
                            <div style='display: flex; align-items: center; background-color: #FAFAFA; padding: 8px; border-radius: 6px; margin-bottom: 4px; 
                            border-left: 4px solid {status_color}; font-size: 14px; color: #333333; font-weight: 500;'>
                                <span style='font-size: 18px; font-weight: bold; color: {status_color};'>{status_icon}</span>
                                <span style='margin-left: 10px;'>{parameter}</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
            category_index += 1  # Move to the next column index

    # Evaluation Tab
    with tabs[1]:
        # st.markdown("## Evaluation")
        evaluation = openai_response.get("Evaluation", {})
        sorted_evaluation = sorted(evaluation.items(), key=lambda x: x[1]['Score'])
        
        for parameter, details in sorted_evaluation:
            bg_color, text_color, content_color = get_dynamic_colors(details['Score'])
            st.markdown(f"""
                <div style='background-color: {bg_color}; padding: 15px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'>
                    <h4 style='color: {text_color};'>{parameter} <span style='float: right; background-color: {text_color}; color: white; padding: 5px 10px; border-radius: 20px; font-size: 14px;'>Score: {details['Score']}/5</span></h4>
                    <p style='color: {content_color};'>{details['Justification']}</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Feedback Tab
    with tabs[2]:
        # st.markdown("## Feedback")
        feedback = openai_response.get("Feedback", {})
        
        st.markdown("Strengths")
        for strength, details in feedback.get("Strengths", {}).items():
            st.markdown(f"""
                <div style='background-color: #dff5dc; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                    <h5 style='color: #2e7d32;'>{strength}</h5>
                    <p style='color: #6b6b6b;'><b>Example:</b> {details['Example']}</p>
                    <p style='color: #6b6b6b;'><b>Impact:</b> {details['Impact']}</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("Areas for Improvement")
        for issue, details in feedback.get("Areas for Improvement", {}).items():
            st.markdown(f"""
                <div style='background-color: #e3eafc; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                    <h5 style='color: #2c3e50;'>{issue}</h5>
                    <p style='color: #6b6b6b;'><b>Example:</b> {details['Example']}</p>
                    <p style='color: #6b6b6b;'><b>Recommendation:</b> {details['Recommendation']}</p>
                </div>
            """, unsafe_allow_html=True)

# Main function
def main():
    call_reset_api()
    openai_called = False
    scorecard_called = False
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Long modules
        # components.html(
        #     """
        #     <iframe src="https://app.millis.ai/agents/embedded?id=-OHg1xY4twj3sCGHpnxP&k=HqUpIgSZIlO91bEHmgILHqYuRwPg5c7t" 
        #     width="100%" height="500" style="border: none;" allow="microphone">
        #     </iframe>
        #     """,
        #     height=500,
        # )

        #Short modules
        components.html(
            """
            <iframe src="https://app.millis.ai/agents/embedded?id=-OIAm1v3O1sdhQrVq-pL&k=HqUpIgSZIlO91bEHmgILHqYuRwPg5c7t" width="100%" height="500" style="border: none;" allow="microphone"></iframe>
            """,
            height=500,
        )
    
    with col2:
        step_placeholder = col2.empty()
        api_url = "http://13.201.227.194:8502/get_transcript"
        
        while True:
            transcript_data = fetch_transcript(api_url)
            if transcript_data:
                if len(str(transcript_data)) > 100 and not openai_called:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future_openai = executor.submit(fetch_openai_response, feedback_prompt, transcript_data)
                        future_scorecard = executor.submit(fetch_openai_response, scorecard_prompt, transcript_data)

                        # Retrieve the results
                        openai_response = future_openai.result()
                        openai_called = True

                        scorecard_data = future_scorecard.result()
                        scorecard_called = True
                    # openai_response = get_solutions_from_openai(feedback_prompt, str(transcript_data))
                    # openai_response = json.loads(openai_response)
                    # openai_called = True

                    # # Second LLM call for scorecard generation
                    # scorecard_response = get_solutions_from_openai(scorecard_prompt, str(transcript_data))
                    # scorecard_data = json.loads(scorecard_response)
                    # scorecard_called = True
                    break
            else:
                step_placeholder.markdown("No Transcript available.")
            time.sleep(2)
    
    if openai_called and scorecard_called:
        with col2:
            display_tabs(openai_response, scorecard_data)

if __name__ == "__main__":
    main()