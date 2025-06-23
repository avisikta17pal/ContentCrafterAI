"""
planner_agent.py

Defines the PlannerAgent, responsible for generating a structured content plan
including blog titles, video ideas, and tweet hooks using the Gemini model.
Also validates the quality of the topic.

🔁 Example Usage:

Input:
    topic = "AI in Education"

Output (string):
    Blog Title: "The Future of Learning: AI in Education"
    YouTube Idea: "How AI is Revolutionizing the Classroom"
    Tweet Hooks:
    - "AI isn’t the future of education. It’s the present. 🎓🤖"
    - "Would you trust an AI to teach your child?"
    - "Teachers + AI = Superpowers for Learning!"
"""

import google.generativeai as genai

class PlannerAgent:
    """
    The PlannerAgent generates a content plan (title, YouTube idea, tweets) for a given topic.
    Also performs topic validation and requests rephrasing if needed.
    """

    def __init__(self, api_key: str, model_name="gemini-1.5-flash"):  # Added model_name parameter with default
        """
        Initializes the PlannerAgent with the provided API key.

        Args:
            api_key (str): Your Google Generative AI API key.
            model_name (str, optional): The Gemini model to use. Defaults to "gemini-1.5-flash" for hackathon quota compatibility.
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)  # Updated to use model_name

    def plan(self, topic: str) -> str:
        """
        Validates the topic and generates a content strategy for the given topic.

        Args:
            topic (str): The subject to plan content for.

        Returns:
            str: A formatted content plan OR a message asking for better topic input.
        """

        prompt = f"""
You are an expert content strategist. Evaluate this topic: "{topic}"

Step 1: Determine if the topic is clear, specific, and suitable for a blog post.
If it is vague (e.g. "Technology"), irrelevant (e.g. "My cat's name"), or nonsensical,
kindly explain why and ask the user to provide a more specific and meaningful topic.

Step 2: If the topic is valid, generate:
- Blog Title
- YouTube Video Idea
- 3 Tweet Hooks

Respond accordingly.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"⚠️ Error generating content plan: {str(e)}"