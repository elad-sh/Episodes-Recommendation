import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class EpisodeRecommender:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv("SUPABASE_DB_URL"))
    
    def get_all_episodes(self):
        """Get all episodes from the database."""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT season, episode_num, title, description, characters, rating 
            FROM episodes 
            ORDER BY season, episode_num
        """)
        episodes = cur.fetchall()
        cur.close()
        return episodes
    
    def get_episodes_by_rating(self, min_rating=0):
        """Get episodes with rating above the minimum."""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT season, episode_num, title, description, characters, rating 
            FROM episodes 
            WHERE rating >= %s
            ORDER BY rating DESC
        """, (min_rating,))
        episodes = cur.fetchall()
        cur.close()
        return episodes
    
    def get_episodes_by_season(self, season):
        """Get all episodes from a specific season."""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT season, episode_num, title, description, characters, rating 
            FROM episodes 
            WHERE season = %s
            ORDER BY episode_num
        """, (season,))
        episodes = cur.fetchall()
        cur.close()
        return episodes
    
    def get_episodes_by_character(self, character):
        """Get episodes featuring a specific character."""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT season, episode_num, title, description, characters, rating 
            FROM episodes 
            WHERE %s = ANY(characters)
            ORDER BY season, episode_num
        """, (character,))
        episodes = cur.fetchall()
        cur.close()
        return episodes
    
    def format_episode(self, episode):
        """Format an episode tuple into a readable string."""
        season, episode_num, title, description, characters, rating = episode
        return f"Season {season}, Episode {episode_num}: {title}\nRating: {rating}/10\nCharacters: {', '.join(characters) if characters else 'N/A'}\nDescription: {description if description else 'N/A'}\n"
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close() 