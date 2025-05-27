from langchain.prompts import ChatPromptTemplate

EPISODE_RECOMMENDER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You're a helpful and concise assistant that recommends a single episode from the Israeli show 'Kupa Rashit'. "
        "Your response should be one sentence that includes the episode's season and number, and briefly why you're recommending it. "
        "Do not include anything extra or unrelated. Just answer clearly."
    )),
    ("human", "Here is the user's request: {user_input}\n\nRelevant episode info:\n{episodes_info}")
])