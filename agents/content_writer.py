"""
content_writer.py

Defines the ContentWriterAgent, responsible for generating a long-form blog post
based on the planner’s topic or blog title. Can also improve upon a previous version
using feedback from the ContentEditorAgent.

🔁 Example Usage:

Input:
    topic = "AI in Education"
    feedback = "The intro needs to be stronger, avoid repetition..."

Output (string):
    A revised and improved blog post based on the topic and editor feedback.
"""

import google.generativeai as genai

class ContentWriterAgent:
    """
    The ContentWriterAgent generates or improves a blog post using a given topic.
    Can optionally use feedback to regenerate improved versions.
    """

    def __init__(self, api_key: str, model_name="gemini-1.5-flash"):  # Added model_name parameter with default
        """
        Initializes the ContentWriterAgent with the provided API key.

        Args:
            api_key (str): Your Google Generative AI API key.
            model_name (str, optional): The Gemini model to use. Defaults to "gemini-1.5-flash" for hackathon quota compatibility.
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)  # Updated to use model_name

    def generate_content(self, topic: str, previous_draft: str = None, feedback: str = None) -> str:
        """
        Generates a detailed blog post on a given topic or regenerates it using feedback.

        Args:
            topic (str): The subject to write about.
            previous_draft (str, optional): The original blog post draft to improve.
            feedback (str, optional): Editor feedback to use for revision.

        Returns:
            str: The newly generated or improved blog post.
        """
        print(f"Generating content for topic: {topic}")  # Added debug print
        if previous_draft and feedback:
            prompt = f"""
You are a skilled content writer. Here's a blog post draft on the topic '{topic}', along with editorial feedback.

Your task:
- Revise and rewrite the blog post.
- Use the feedback to improve weak areas.
- Make it more engaging, well-structured, and informative.

--- Feedback from Editor ---
{feedback}

--- Original Draft ---
{previous_draft}

Return the improved blog post only.
            """
        else:
            prompt = f"""
Write a detailed blog post on the topic: '{topic}'.
Make it informative, engaging, structured with subheadings, and easy to understand.
Avoid fluff and repetition. Provide examples or evidence where possible.
            """

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"⚠️ Error generating content: {str(e)}"