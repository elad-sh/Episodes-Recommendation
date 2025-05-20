from langchain.prompts import ChatPromptTemplate

EPISODE_RECOMMENDER_PROMPT = ChatPromptTemplate.from_template("""
{history}

{user_input}

{episodes_info}

Format the response as a single natural sentence that tells a story about the episode. Include the season, episode number, title, and rating, but focus on making the description engaging. Example: "I recommend Season 1, Episode 3 'The Morning of a Terror Attack' (rated 8.7/10) - it's a powerful episode where a nearby terror attack changes how everyone treats Ramzi at work, while Kochava deals with her son's unexpected interest in Esti."
""") 