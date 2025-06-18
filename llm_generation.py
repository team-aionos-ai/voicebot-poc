import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

def get_solutions_from_openai(system_prompt, user_prompt):
    try:
        openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        openai_response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
             messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
             )

        return openai_response.choices[0].message.content
    except Exception as e:
        return f"Error in backup OpenAI call: {str(e)}"
