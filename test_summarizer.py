from summarizer import summarize_text

if __name__ == "__main__":
    sample_text = """
    Artificial Intelligence (AI) is a branch of computer science that aims
    to create systems capable of performing tasks that typically require
    human intelligence. These tasks include reasoning, learning,
    perception, and language understanding.
    """

    print("Summarizing...")
    summary = summarize_text(sample_text)
    print("\n--- SUMMARY ---\n")
    print(summary)
