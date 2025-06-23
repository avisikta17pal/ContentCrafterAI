import google.generativeai as genai

class AudienceAnalyzerAgent:
    def __init__(self, api_key: str, model_name="gemini-1.5-flash"):  # Added model_name parameter with default
        """
        Initializes the AudienceAnalyzerAgent with the provided API key.

        Args:
            api_key (str): Your Google Generative AI API key.
            model_name (str, optional): The Gemini model to use. Defaults to "gemini-1.5-flash" for hackathon quota compatibility.
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)  # Updated to use model_name

    def generate_audience_profile(self, topic: str) -> str:
        """
        Generates an audience profile for the topic.

        Args:
            topic: str, the topic to analyze.

        Returns:
            str: formatted audience profile
        """
        prompt = f"""
You are a market research expert. Analyze the topic '{topic}' and generate a probable audience profile, including:
- Demographics: (e.g., age, profession, location)
- Interests: (e.g., tech, education)
- Reading Goals: (e.g., beginner, professional)

Return a formatted profile like this:

### Audience Profile
**Demographics**: <details>
**Interests**: <details>
**Reading Goals**: <details>
"""
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error generating audience profile: {str(e)}"