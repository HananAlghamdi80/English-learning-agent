from memory import save_session
from rag import retrieve_context
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def english_learning_agent(
    user_message,
    learner_name="Hanan",
    learner_level="I don't know",
    learner_goal="Improve English",
    mode="Conversation Practice"
):
    # RAG
    context = retrieve_context(user_message)

    prompt = f"""
You are an English Learning Agent for Saudi tech learners.

Learner Profile:
- Name: {learner_name}
- Current English Level: {learner_level}
- Learning Goal: {learner_goal}
- Practice Mode: {mode}

Your responsibilities:
- Assess English level when needed
- Correct grammar mistakes
- Improve vocabulary
- Give feedback
- Generate exercises
- Help with interview preparation
- Support role-playing scenarios
- Use the knowledge base context when relevant
- Keep responses clear, practical, and encouraging

Knowledge Base Context:
{context}

User Message:
{user_message}

Instructions:
- If mode is "Level Assessment", ask diagnostic questions and estimate the CEFR level.
- If mode is "Grammar Feedback", correct the sentence, explain the mistake, and give an improved version.
- If mode is "Job Interview Role-play", act as an interviewer and ask one question at a time.
- If mode is "Daily Task", generate a short personalized English practice task.
- If mode is "Progress Summary", summarize the learner's progress and suggest next steps.
- If mode is "Conversation Practice", continue a natural English conversation.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an English Learning Coach for Saudi tech learners."
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
    )

    answer = response.choices[0].message.content

    # Long-term memory: save practice history
    save_session(
        learner_name=learner_name,
        mode=mode,
        user_message=user_message
    )

    return answer


if __name__ == "__main__":
    user_input = input("You: ")

    answer = english_learning_agent(
        user_message=user_input,
        learner_name="Hanan",
        learner_level="A2",
        learner_goal="Job interviews",
        mode="Grammar Feedback"
    )

    print("\nAgent:")
    print(answer)