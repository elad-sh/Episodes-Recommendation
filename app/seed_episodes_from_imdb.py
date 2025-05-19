import psycopg2
from dotenv import load_dotenv
import os
import gzip
import csv

load_dotenv()

# IMDB ID for Kupa Rashit
SHOW_ID = "tt8796226"

def read_imdb_dataset(filename):
    """Read and parse an IMDB dataset file."""
    try:
        with gzip.open(f"data/{filename}", 'rt', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            return list(reader)
    except FileNotFoundError:
        print(f"❌ File not found: data/{filename}")
        return []
    except Exception as e:
        print(f"❌ Error reading {filename}: {str(e)}")
        return []

def get_episodes():
    """Get all episodes for Kupa Rashit."""
    # Get episode information
    episodes = read_imdb_dataset("title.episode.tsv.gz")
    kupa_episodes = [ep for ep in episodes if ep['parentTconst'] == SHOW_ID]
    
    # Get titles
    titles = read_imdb_dataset("title.basics.tsv.gz")
    title_dict = {t['tconst']: t for t in titles}
    
    # Get ratings
    ratings = read_imdb_dataset("title.ratings.tsv.gz")
    rating_dict = {r['tconst']: r for r in ratings}
    
    # Combine all information
    episode_data = []
    for ep in kupa_episodes:
        ep_id = ep['tconst']
        title_info = title_dict.get(ep_id, {})
        rating_info = rating_dict.get(ep_id, {})
        
        episode_data.append({
            "season": int(ep['seasonNumber']),
            "episode_num": int(ep['episodeNumber']),
            "title": title_info.get('primaryTitle', ''),
            "rating": float(rating_info.get('averageRating', 0)),
            "description": "",  # We'll update this manually
            "characters": []    # Empty array for characters
        })
    
    return episode_data

def seed_episodes():
    """Seed the database with episode data."""
    try:
        # Connect to database
        conn = psycopg2.connect(os.getenv("SUPABASE_DB_URL"))
        cur = conn.cursor()
        
        # Get episodes
        episodes = get_episodes()
        print(f"Found {len(episodes)} episodes to insert")
        
        # Insert episodes
        for ep in episodes:
            cur.execute("""
                INSERT INTO episodes (season, episode_num, title, description, characters, rating)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (season, episode_num) 
                DO UPDATE SET 
                    title = EXCLUDED.title,
                    rating = EXCLUDED.rating,
                    characters = EXCLUDED.characters
            """, (
                ep["season"],
                ep["episode_num"],
                ep["title"],
                ep["description"],
                ep["characters"],
                ep["rating"]
            ))
        
        conn.commit()
        print("✅ Successfully seeded episode data")
        
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
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    print("Please download these files from https://datasets.imdbws.com/ and place them in the 'data' directory:")
    print("1. title.episode.tsv.gz")
    print("2. title.basics.tsv.gz")
    print("3. title.ratings.tsv.gz")
    
    input("Press Enter after downloading the files...")
    
    seed_episodes() 