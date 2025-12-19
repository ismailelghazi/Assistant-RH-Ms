import os
import google.generativeai as genai
from ..config import get_settings

settings = get_settings()

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

class RetentionAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
    def generate_plan(self, employee_data: dict, risk_level: str) -> str:
        prompt = f"""
        You are an expert HR consultant. An employee is at {risk_level} risk of leaving.
        
        Employee Profile:
        {employee_data}
        
        Generate a personalized retention plan with 3-5 actionable steps to keep them.
        Focus on their specific pain points (e.g., low salary, lack of promotion, overtime).
        """
        
        response = self.model.generate_content(prompt)
        return response.text

def get_agent():
    return RetentionAgent()
