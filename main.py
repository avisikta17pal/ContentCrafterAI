"""
Main file for ContentCrafter AI — a multi-agent content generation pipeline.

This runs three agents using the Google Generative AI API:
1. PlannerAgent — Plans title, video idea, tweet hooks
2. ContentWriterAgent — Writes long-form blog content
3. ContentEditorAgent — Polishes and aligns the blog with the plan

Example Usage (CLI):

🧠 Welcome to ContentCrafter AI!
📝 Enter one or more topics (comma or line-separated):
> Future of AI in Education, Space Colonization

Topic: Future of AI in Education
📄 Content Plan:
Blog Title: "The Future of Learning: AI in Education"
YouTube Idea: "How AI is Revolutionizing the Classroom"
Tweet Hooks:
- "AI isn’t the future of education. It’s the present. 🎓🤖"
- "Would you trust an AI to teach your child?"
- "Teachers + AI = Superpowers for Learning!"

📝 Original Draft (pre-feedback):
"AI is being used in education today..."

💬 Editor Feedback:
"..."

📝 Improved Draft (After Feedback):
"AI is transforming education with innovative tools..."

✅ Final Edited Blog Post:
"Artificial Intelligence is revolutionizing education..."
"""

from agents.chain_agent import ContentChainAgent
import google.api_core.exceptions
from utils.logger import log_info
import re  # Added to fix 're' not defined error

def main():
    """
    CLI for ContentCrafter AI with:
    - Topic validation with re-entry prompt
    - Multi-topic batch input
    - Full content chain with draft, feedback, and final outputs
    """
    log_info("Starting ContentCrafter AI")
    print("🧠 Welcome to ContentCrafter AI!")
    print("This AI system will help you plan, write, and refine blog content using Google's Agent Development Kit.\n")

    agent = ContentChainAgent(model_name="gemini-1.5-flash")  # Updated to specify model_name

    while True:
        raw_input = input("📝 Enter one or more topics (comma or line-separated):\n> ")
        log_info(f"User input received: {raw_input}")
        raw_topics = raw_input.replace("\n", ",").split(",")
        topics = [t.strip() for t in raw_topics if t.strip()]

        # Handle empty input
        if not topics:
            print("⚠️ No valid topics entered. Please try again.")
            log_info("No valid topics entered, prompting again")
            continue

        # Validate the first topic as a sample
        try:
            validation = agent.validate_topic(topics[0])
            log_info(f"Validating topic: {topics[0]}, Result: {validation}")
            if validation.startswith("VALID"):
                break
            print(f"⚠️ Invalid topic '{topics[0]}': {validation}\nPlease enter specific, meaningful topics.")
        except google.api_core.exceptions.ResourceExhausted as e:
            print(
                f"⚠️ API Quota Exceeded: {str(e)}\nPlease check your Google Cloud plan and billing details at "
                f"https://ai.google.dev/gemini-api/docs/rate-limits, generate a new API key at https://aistudio.google.com/, "
                f"or contact support before the June 24, 2025 deadline."
            )
            log_info(f"API Quota Exceeded: {str(e)}")
            return 1

    try:
        log_info(f"Running content generation for topics: {','.join(topics)}")
        print("\n🔄 Running content generation chain...\n")
        results = agent.run_chain(",".join(topics))

        print("\n✅ Content Generation Complete!\n")

        for topic, output in results.items():
            log_info(f"Processing output for topic: {topic}")
            print("=" * 60)
            print(f"\n📌 Topic: {topic}\n")

            if "error" in output:
                print(f"❌ Skipped due to error: {output['error']}")
                log_info(f"Error for topic {topic}: {output['error']}")
                continue

            print("🧠 Content Plan:\n", output["plan"])
            print("\n📝 Original Draft (pre-feedback):\n", output["initial_draft"])
            print("\n💬 Editor Feedback:\n", output["feedback"])
            print("\n✍️ Improved Blog Post (After Feedback):\n", output["blog_post"])
            print("\n🔄 Second Draft (After Structural Feedback):\n", output["second_draft"])
            print("\n🏗️ Structural Feedback:\n", output["structural_feedback"])
            print("\n✅ Final Edited Blog Post:\n", output["edited_post"])

            # Log and note image placeholders
            for section in ["initial_draft", "blog_post", "second_draft", "edited_post"]:
                if "Insert image here:" in output[section]:
                    log_info(f"Image placeholder found in {section} for topic {topic}: {output[section]}")
                    print(f"\n🌄 Note: Image placeholder detected in {section}. Add an image for: {re.search(r'Insert image here: (.*?)\n', output[section]).group(1)}")

            print("=" * 60)

    except google.api_core.exceptions.ResourceExhausted as e:
        print(
            f"⚠️ API Quota Exceeded: {str(e)}\nPlease check your Google Cloud plan and billing details at "
            f"https://ai.google.dev/gemini-api/docs/rate-limits, generate a new API key at https://aistudio.google.com/, "
            f"or contact support before the June 24, 2025 deadline."
        )
        log_info(f"API Quota Exceeded during processing: {str(e)}")
        return 1
    except Exception as e:
        print(f"⚠️ Error during content generation: {e}")
        log_info(f"General error during processing: {str(e)}")
        return 1

if __name__ == "__main__":
    main()