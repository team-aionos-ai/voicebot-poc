import streamlit as st
import streamlit.components.v1 as components
import requests
import time
import json

# Set page configuration
st.set_page_config(
    layout="wide",
    page_title="Amadeus Voicebot",
)

if 'steps_list' not in st.session_state:
    st.session_state['steps_list'] = []

def call_reset_api():
    """
    Calls the reset_step_details API to reset the step details.
    
    Parameters:
        base_url (str): The base URL of the Flask server (e.g., "http://localhost:5000").
    
    Returns:
        dict: The response from the API.
    """

    reset_endpoint = "http://13.201.227.194:8502/reset_step_details"
    # reset_endpoint = f"{base_url}/reset_step_details"
    
    try:
        # Send POST request to the reset endpoint
        response = requests.post(reset_endpoint)
        
        # Check if the response was successful
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to reset. Status code: {response.status_code}, Response: {response.text}"}
    
    except Exception as e:
        return {"error": str(e)}


def main():
    call_reset_api()
    # Divide the layout into two columns
    col1, col2 = st.columns(2)

# Embed the iframe in the first column
    with col1:
        # st.markdown("### Voicebot")
        components.html(
            """
            <iframe 
                src="https://app.millis.ai/agents/embedded?id=-OGf6xnNO-3Ix6gGrA3z&k=HqUpIgSZIlO91bEHmgILHqYuRwPg5c7t" 
                width="100%" 
                height="500" 
                style="border: none;" 
                allow="microphone">
            </iframe>
            """,
            height=500,
        )

    # Add space to display step details in the second column
    with col2:
        with st.container(height=500, border=False):
            # st.markdown("### Step Details")

            # Placeholder to dynamically update the content
            step_placeholder = st.empty()

            # URL of the local API to fetch step details
            # api_url = "http://172.31.3.215:8502/get_step_details"
            api_url = "http://13.201.227.194:8502/get_step_details"

            def format_step_data(step_data):
                """Format the step data into collapsible UI elements"""

                step_card = ""
                # Remove duplicates
                unique_dict_list = [dict(t) for t in {tuple(sorted(d.items())) for d in step_data}]

                # Check if the length of unique_dict_list is 2 and remove the entry with step_number = '0'
                try:
                    unique_dict_list = [d for d in unique_dict_list if d.get('step_number') != '0']
                except:
                    pass

                try:
                    # Sort the list based on step_number (as integers)
                    sorted_dict_list = sorted(unique_dict_list, key=lambda x: int(x['step_number']), reverse=True)

                    # Convert step_number back to string (already a string, but this ensures consistency)
                    for d in sorted_dict_list:
                        d['step_number'] = str(d['step_number'])
                except:
                    sorted_dict_list = unique_dict_list

                for i, single_step in enumerate(sorted_dict_list):
                    description = single_step.get("description", "No description provided.")
                    command = single_step.get("command", "N/A")
                    additional_info = single_step.get("additional_info", "N/A")
                    step_number = single_step.get("step_number", "Step")

                    # Highlight the current step (Assuming the first step is the most recent/current step)
                    if i == 0:
                        # Current step style
                        highlight_style = """
                            background-color: #E3F2FD; 
                            border: 3px solid #1976D2; 
                            box-shadow: 0 0 20px rgba(25, 118, 210, 0.8); 
                            color: #0D47A1;
                            animation: fadeInNewCard 0.8s ease-in-out forwards;
                        """
                        additional_info_style = "color: #0D47A1; font-style: normal;"
                        command_style = """
                            background-color: #FFFFFF; 
                            border: 1px solid #E0E0E0; 
                            color: #4A4A4A;
                        """
                    else:
                        # Grayed-out style for non-current steps
                        highlight_style = """
                            background-color: #F5F5F5; 
                            border: 1px solid #B0BEC5; 
                            color: #607D8B;
                        """
                        additional_info_style = "color: #90A4AE;"
                        command_style = """
                            background-color: #F9F9F9; 
                            border: 1px solid #D0D0D0; 
                            color: #B0B0B0;
                        """

                    step_card += f"""
                    <div style="padding: 15px; border-radius: 10px; margin-bottom: 10px; {highlight_style}">
                        <p><strong>{step_number}: {description}</strong></p>
                        <div style="border-radius: 5px; padding: 10px; margin-top: 10px; display: flex; justify-content: space-between; align-items: center; {command_style}">
                            <span style="font-family: monospace;">{command}</span>
                        </div>
                        <details style="margin-top: 10px;">
                            <summary style="cursor: pointer; font-weight: bold; {additional_info_style}">Additional Information</summary>
                            <p style="margin-left: 10px; margin-top: 5px; {additional_info_style}">{additional_info}</p>
                        </details>
                    </div>
                    """
                    step_card += """
                    <style>
                    @keyframes fadeInNewCard {
                        0% { opacity: 0; transform: translateY(-15px); }
                        100% { opacity: 1; transform: translateY(0); }
                    }

                    @keyframes fadeOutOldCard {
                        0% { opacity: 1; transform: translateY(0); }
                        100% { opacity: 0.5; transform: translateY(10px); }
                    }
                    </style>
                    """

                return step_card



            while True:
                try:
                    # Fetch the latest step details from the API
                    response = requests.get(api_url)
                    # st.write(response.json())
                    if response.status_code == 200:
                        step_data = response.json()
                        print("STEPS DATA: ",step_data)
                        st.session_state['steps_list'].append(step_data)
                        # Display the step details in the second column
                        formatted_step_data = format_step_data(st.session_state['steps_list'])
                        step_placeholder.markdown(formatted_step_data, unsafe_allow_html=True)

                    else:
                        step_placeholder.markdown("No step details available.")
                except Exception as e:
                    step_placeholder.markdown(f"Error fetching step details: {e}")

                # Poll the API every 2 seconds
                time.sleep(2)

if __name__ == "__main__":
    main()