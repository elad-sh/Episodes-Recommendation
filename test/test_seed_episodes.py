import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Test with just a few episodes
TEST_EPISODES = [
    {"season": 1, "episode_num": 1, "title": "Mine From Home", "description": "Amnon will do everything to not pay for the snack he brought from home. Shira has to share an office with Nissim and Anatoly who transformed the office to a synagogue.", "characters": ["Amnon", "Shira", "Nissim", "Anatoly", "Kochava"], "rating": 8.6},
    {"season": 1, "episode_num": 2, "title": "Shelf Wars", "description": "A pricing error causes chaos in the store.", "characters": ["Ramzi", "Nissim"], "rating": 8.5},
    {"season": 1, "episode_num": 3, "title": "The New Employee", "description": "A new employee joins the team and causes unexpected changes.", "characters": ["Amnon", "Shira", "Kochava"], "rating": 8.4}
]

def seed_test_episodes():
    """Seed the database with test episode data."""
    try:
        # Connect to database
        conn = psycopg2.connect(os.getenv("SUPABASE_DB_URL"))
        cur = conn.cursor()
        
        print(f"Inserting {len(TEST_EPISODES)} test episodes...")
        
        # Insert episodes
        for ep in TEST_EPISODES:
            cur.execute("""
                INSERT INTO episodes (season, episode_num, title, description, characters, rating)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (season, episode_num) 
                DO UPDATE SET 
                    title = EXCLUDED.title,
                    description = EXCLUDED.description,
                    characters = EXCLUDED.characters,
                    rating = EXCLUDED.rating
            """, (
                ep["season"],
                ep["episode_num"],
                ep["title"],
                ep["description"],
                ep["characters"],
                ep["rating"]
            ))
            print(f"✅ Inserted episode {ep['season']}.{ep['episode_num']}: {ep['title']}")
        
        conn.commit()
        print("\n✅ Successfully seeded test episodes")
        
    except Exception as e:
        print(f"❌ Error seeding database: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("Running the seeding function")
    seed_test_episodes() 