"""
ContentChainAgent ties together the PlannerAgent, ContentWriterAgent, and ContentEditorAgent
into a pipeline that turns user-provided topic(s) into polished blog posts.

✨ Enhancements:
- Feedback loop from Editor to Writer
- Topic validation before planning
- Multi-topic batch generation
- Role-switching iterative collaboration
"""

from agents.planner_agent import PlannerAgent
from agents.content_writer import ContentWriterAgent
from agents.content_editor import ContentEditorAgent
from agents.engagement_predictor import EngagementPredictorAgent
# Placeholder imports for new agents
# from agents.audience_analyzer import AudienceAnalyzerAgent
# from agents.tone_refiner_agent import ToneRefinerAgent
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

class ContentChainAgent:
    def __init__(self, model_name="gemini-1.5-flash"):  # Added model_name parameter with default
        # Initialize agents with api_key and model_name for switch to gemini-1.5-flash
        self.planner = PlannerAgent(api_key, model_name)
        self.writer = ContentWriterAgent(api_key, model_name)
        self.editor = ContentEditorAgent(api_key, model_name)
        self.engagement_predictor = EngagementPredictorAgent(api_key, model_name)  # Added initialization
        # Placeholder initializations for new agents
        # self.audience_analyzer = AudienceAnalyzerAgent(api_key, model_name)
        # self.tone_refiner = ToneRefinerAgent(api_key, model_name)

    def validate_topic(self, topic: str) -> str:
        """
        Validates the topic using the planner agent.
        If topic is invalid, returns an error message string.
        """
        validation_prompt = f"""You are a content validation expert.
Evaluate if the topic '{topic}' is suitable for generating blog content.
Reject vague topics (like "life" or "AI") and ask for more specific ones.
Respond with:
'VALID' — if acceptable
or
'INVALID: <reason and how to improve it>'"""

        result = self.planner.model.generate_content(validation_prompt).text.strip()
        return result

    def run_single_chain(self, topic: str) -> dict:
        """
        Runs the full content generation pipeline for a single topic with role-switching.
        """
        print(f"\n🔎 Validating topic: '{topic}'...")
        validation = self.validate_topic(topic)
        if not validation.startswith("VALID"):
            return {"error": f"❌ Topic '{topic}' is invalid.\n\n{validation}"}

        print("📌 Step 1: Generating content plan...\n")
        plan = self.planner.plan(topic)  # Ensure planner uses the validated topic
        print("📄 Content Plan:\n", plan)

        # Extract title, default to topic if no valid title found
        title_line = next((line for line in plan.split('\n') if "title" in line.lower()), f"Blog Title: {topic}")
        blog_topic = title_line.split(":")[-1].strip() if ":" in title_line else topic
        if not blog_topic.lower().startswith(topic.lower()):  # Check for mismatch
            print(f"⚠️ Warning: Extracted topic '{blog_topic}' differs from input '{topic}'. Forcing input topic.")
            blog_topic = topic

        print("\n✍️ Step 2: Writing initial blog post...\n")
        initial_draft = self.writer.generate_content(blog_topic)
        print("📝 Initial Draft:\n", initial_draft)

        print("\n🛠️ Step 3: First Edit Pass...\n")
        first_edit = self.editor.revise_content(initial_draft, plan)
        print("✅ First Edited Version:\n", first_edit["revised_post"])

        print("\n🔁 Step 4: Feedback Loop - Improving Draft...\n")
        improvement_prompt = f"""You're a senior blog reviewer.
Based on this editor-reviewed version, suggest 3 clear improvements for the writer, focusing on clarity and engagement:

--- Final Edited Version ---
{first_edit["revised_post"]}

Reply with the improvements only."""
        feedback = self.editor.model.generate_content(improvement_prompt).text.strip()

        print("📌 Editor Feedback:\n", feedback)

        print("\n✍️ Step 5: Writer Applies Feedback...\n")
        improved_draft = self.writer.generate_content(blog_topic, previous_draft=first_edit["revised_post"], feedback=feedback)
        print("📝 Improved Draft:\n", improved_draft)

        print("\n🔄 Step 6: Second Edit Pass with Structural Feedback...\n")
        second_edit = self.editor.revise_content(improved_draft, plan, structural_feedback=True)
        print("✅ Second Edited Version:\n", second_edit["revised_post"])

        print("\n🔁 Step 7: Second Feedback Loop - Structural Improvements...\n")
        structural_prompt = f"""You're a senior blog reviewer.
Based on this editor-reviewed version, suggest 2 structural improvements (e.g., reorganize sections, add subheadings):

--- Second Edited Version ---
{second_edit["revised_post"]}

Reply with the improvements only."""
        structural_feedback = self.editor.model.generate_content(structural_prompt).text.strip()

        print("📌 Structural Feedback:\n", structural_feedback)

        print("\n✍️ Step 8: Writer Applies Structural Feedback...\n")
        second_draft = self.writer.generate_content(blog_topic, previous_draft=second_edit["revised_post"], feedback=structural_feedback)
        print("📝 Second Draft:\n", second_draft)

        print("\n🧹 Step 9: Final Polishing...\n")
        final_post = self.editor.revise_content(second_draft, plan)
        print("✅ Final Polished Blog:\n", final_post["revised_post"])

        # Step 10: Predict Engagement
        print("\n📈 Step 10: Predicting Engagement...\n")
        engagement = self.engagement_predictor.predict_engagement(final_post["revised_post"])
        print(f"📊 Engagement Score: {engagement['score']}\nAnalysis:\n", engagement['analysis'])

        return {
            "plan": plan,
            "blog_title": blog_topic,
            "blog_post": improved_draft,
            "second_draft": second_draft,
            "edited_post": final_post["revised_post"],
            "feedback": feedback,
            "structural_feedback": structural_feedback,
            "initial_draft": initial_draft,
            "engagement_score": engagement["score"],
            "engagement_analysis": engagement["analysis"]
        }

    def run_chain(self, input_topics: str) -> dict:
        """
        Accepts a comma-separated string of topics and returns generated content for each.
        """
        topics = [t.strip() for t in input_topics.split(",") if t.strip()]
        results = {}

        for topic in topics:
            print(f"\n\n===========================\n🧠 Processing Topic: {topic}\n===========================")
            result = self.run_single_chain(topic)
            results[topic] = result

        return results