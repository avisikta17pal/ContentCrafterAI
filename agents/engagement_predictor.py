import google.generativeai as genai

class EngagementPredictorAgent:
    def __init__(self, api_key: str, model_name="gemini-1.5-flash"):  # Added model_name parameter with default
        """
        Initializes the EngagementPredictorAgent with the provided API key.

        Args:
            api_key (str): Your Google Generative AI API key.
            model_name (str, optional): The Gemini model to use. Defaults to "gemini-1.5-flash" for hackathon quota compatibility.
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)  # Updated to use model_name

    def predict_engagement(self, blog: str) -> dict:
        """
        Analyzes the blog for engagement and predicts a score (1–10).

        Args:
            blog: str, the blog post to analyze.

        Returns:
            dict: {
                "score": int, engagement score,
                "analysis": str, explanation of score
            }
        """
        prompt = f"""
You are an engagement expert. Evaluate the blog post for the following criteria:
- **Length**: Is it appropriate? (Ideal range: ~500–1500 words, too short or too long reduces engagement.)
- **Emotional Impact**: Does it evoke curiosity, excitement, or empathy? (Strong emotional hooks increase scores.)
- **CTA Presence**: Is there a clear call-to-action (e.g., read more, support a cause)? (A strong CTA boosts engagement.)
- **Formatting**: Are headings, lists, and paragraphs clear and well-structured? (Good formatting enhances readability.)

Assign a score from 1 to 10 based on these criteria and provide a detailed explanation.

--- Blog Post ---
{blog}

Return in the following format:
```markdown
### Engagement Score: <score>
### Analysis:
<explanation of the score based on the criteria above>
```
"""
        try:
            response = self.model.generate_content(prompt)
            output = response.text.strip()

            score = 5  # Default score if parsing fails
            analysis = "No analysis provided."
            if "### Analysis:" in output:
                score_part = output.split("### Engagement Score:")[1].split("\n")[0].strip()
                analysis_part = output.split("### Analysis:")[1].strip()
                try:
                    score = int(score_part)
                    if score < 1 or score > 10:
                        raise ValueError("Score out of range (1-10)")
                except ValueError as ve:
                    analysis = f"Failed to parse score: {score_part}. Error: {str(ve)}"
                else:
                    analysis = analysis_part
            else:
                analysis = "Unexpected response format."

            return {
                "score": score,
                "analysis": analysis
            }
        except Exception as e:
            return {
                "score": 0,
                "analysis": f"Error predicting engagement: {str(e)}"
            }