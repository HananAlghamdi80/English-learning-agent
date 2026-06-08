import os

KB_FOLDER = "knowledge_base"

def load_knowledge_base():
    content = ""

    for filename in os.listdir(KB_FOLDER):
        if filename.endswith(".txt"):
            path = os.path.join(KB_FOLDER, filename)
            with open(path, "r", encoding="utf-8") as file:
                content += f"\n\n--- {filename} ---\n"
                content += file.read()

    return content

def retrieve_context(query):
    knowledge = load_knowledge_base()

    if not knowledge.strip():
        return "No knowledge base content found."

    keywords = query.lower().split()
    chunks = knowledge.split("\n\n")

    relevant_chunks = []

    for chunk in chunks:
        score = sum(1 for word in keywords if word in chunk.lower())
        if score > 0:
            relevant_chunks.append(chunk)

    if not relevant_chunks:
        return knowledge[:1500]

    return "\n\n".join(relevant_chunks[:5])