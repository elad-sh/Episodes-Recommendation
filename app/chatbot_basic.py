import os
import warnings
from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceHub
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from episode_recommender import EpisodeRecommender
from prompts import EPISODE_RECOMMENDER_PROMPT

# Suppress LangChain deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

load_dotenv()

llm = HuggingFaceHub(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    model_kwargs={"temperature": 0.5, "max_new_tokens": 256}
)

recommender = EpisodeRecommender()

def analyze_user_query(user_input, memory):
    """Analyze user input to determine what kind of recommendation they want."""
    # Convert to lowercase for easier matching
    query = user_input.lower()
    
    # Check for acknowledgments or confirmations
    acknowledgment_phrases = ["ok", "okay", "sure", "yes", "i will", "i'll watch", "thanks", "thank you"]
    if any(phrase in query for phrase in acknowledgment_phrases):
        return "acknowledgment"  # Special flag to indicate acknowledgment
    
    # Check for season-specific queries
    if "season" in query:
        try:
            # Try to extract season number
            season_num = int(''.join(filter(str.isdigit, query)))
            episodes = recommender.get_episodes_by_season(season_num)
            if episodes:
                # Sort by rating for season-specific queries
                episodes.sort(key=lambda x: x[5], reverse=True)  # x[5] is the rating
                return [episodes[0]]  # Return only the highest rated episode
        except ValueError:
            pass
    
    # Check for rating-specific queries
    if "rated" in query or "rating" in query or "best" in query:
        episodes = recommender.get_episodes_by_rating(8.0)  # Get episodes rated 8.0 or higher
        return [episodes[0]]  # Return only the highest rated episode
    
    # Check for character-specific queries
    characters = ["dudu", "shlomi", "miki", "nati", "yossi"]
    for char in characters:
        if char in query:
            episodes = recommender.get_episodes_by_character(char)
            if episodes:
                episodes.sort(key=lambda x: x[5], reverse=True)  # Sort by rating
                return [episodes[0]]  # Return only the highest rated episode
    
    # Check memory for previous context
    chat_history = memory.chat_memory.messages
    if chat_history:
        # Look for mentions of seasons, characters, or ratings in previous messages
        for message in reversed(chat_history):
            if message.type == "human":
                prev_query = message.content.lower()
                if "season" in prev_query:
                    try:
                        season_num = int(''.join(filter(str.isdigit, prev_query)))
                        episodes = recommender.get_episodes_by_season(season_num)
                        if episodes:
                            episodes.sort(key=lambda x: x[5], reverse=True)
                            return [episodes[0]]
                    except ValueError:
                        pass
                for char in characters:
                    if char in prev_query:
                        episodes = recommender.get_episodes_by_character(char)
                        if episodes:
                            episodes.sort(key=lambda x: x[5], reverse=True)
                            return [episodes[0]]
    
    # Default: return top rated episode
    episodes = recommender.get_episodes_by_rating(7.5)
    return [episodes[0]] if episodes else []

def clean_response(response):
    # Split the response by "Assistant:" and take the last part
    if "Assistant:" in response:
        response = response.split("Assistant:")[-1].strip()
    return response

def run_chat():
    print("📺 Kupa Rashit Episode Recommender — type 'exit' to quit\n")
    print("I can help you find the perfect episode to watch! You can ask about:")
    print("- Episodes from specific seasons (e.g., 'best episodes in season 1')")
    print("- Episodes featuring certain characters")
    print("- Highly rated episodes")
    print("- Or just tell me what you're in the mood for!\n")
    
    # Initialize conversation memory with newer approach
    memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True,
        output_key="output"
    )
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Get relevant episodes based on user query and conversation history
        relevant_episodes = analyze_user_query(user_input, memory)
        
        if relevant_episodes == "acknowledgment":
            print("Bot: Great! Enjoy watching! Would you like another recommendation?")
            continue
            
        if not relevant_episodes:
            print("No episodes found matching your criteria.")
            continue
        
        episodes_info = recommender.format_episode(relevant_episodes[0])

        messages = EPISODE_RECOMMENDER_PROMPT.format_messages(
            user_input=user_input,
            episodes_info=episodes_info
        )
        response = llm.invoke(messages)
        
        # Save the interaction to memory
        memory.save_context({"input": user_input}, {"output": response})
        
        # Clean and print the response
        print("Bot:", clean_response(response))

if __name__ == "__main__":
    try:
        run_chat()
    finally:
        recommender.close()

