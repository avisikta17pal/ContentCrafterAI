# agents/tone_refiner_agent.py
import google.generativeai as genai

class ToneRefinerAgent:
    def __init__(self, api_key: str, model_name="gemini-1.5-flash"):  # Added model_name parameter with default
        """
        Initializes the ToneRefinerAgent with the provided API key.

        Args:
            api_key (str): Your Google Generative AI API key.
            model_name (str, optional): The Gemini model to use. Defaults to "gemini-1.5-flash" for hackathon quota compatibility.
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)  # Updated to use model_name

    def refine_tone(self, draft: str, goals: str, title: str) -> dict:
        """
        Analyzes the blog title and goals to determine the intended emotional tone,
        then refines the draft to align with this tone and provides feedback.

        Args:
            draft (str): The initial blog post draft to refine.
            goals (str): The original content goals provided by PlannerAgent.
            title (str): The blog post title to guide the tone.

        Returns:
            dict: {
                "refined_post": (str) The tone-adjusted blog post,
                "tone_feedback": (str) Explanation of tone adjustments
            }
        """
        prompt = f"""You are a tone expert. Analyze the blog title '{title}' and goals to determine the intended emotional tone.
Refine the draft to align with this tone and explain changes.

--- GOALS ---
{goals}

--- BLOG TITLE ---
{title}

--- DRAFT ---
{draft}

Return in format:
### Refined Post:
<content>
### Tone Feedback:
<explanation>"""
        response = self.model.generate_content(prompt)
        output = response.text.strip()
        if "### Tone Feedback:" in output:
            refined, feedback = output.split("### Tone Feedback:", 1)
            post = refined.replace("### Refined Post:", "").strip()
            tone_feedback = feedback.strip()
        else:
            post = output
            tone_feedback = ""
        return {"refined_post": post, "tone_feedback": tone_feedback}