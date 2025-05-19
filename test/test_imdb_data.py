import os
import gzip
import csv
from pprint import pprint

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


def test_imdb_data():
    """Test reading IMDB data for Kupa Rashit."""
    print("\n=== Testing IMDB Data for Kupa Rashit ===\n")
    
    # Test episode data
    print("1. Reading episode data...")
    episodes = read_imdb_dataset("title.episode.tsv.gz")
    kupa_episodes = [ep for ep in episodes if ep['parentTconst'] == SHOW_ID]
    print(f"Found {len(kupa_episodes)} episodes for Kupa Rashit")
    if kupa_episodes:
        print("\nSample episode data:")
        pprint(kupa_episodes[0])
    
    # Test title data
    print("\n2. Reading title data...")
    titles = read_imdb_dataset("title.basics.tsv.gz")
    kupa_titles = [t for t in titles if t['tconst'] == SHOW_ID]
    print(f"Found {len(kupa_titles)} title entries for Kupa Rashit")
    if kupa_titles:
        print("\nTitle data:")
        pprint(kupa_titles[0])

    # Test rating data
    print("\n3. Reading rating data...")
    ratings = read_imdb_dataset("title.ratings.tsv.gz")


    # Show combined data for first episode
    if kupa_episodes:
        print("\n5. Combined data for first 3 episodes:")
        for ep in kupa_episodes[:3]:
            ep_id = ep['tconst']
            episode_data = {
                "season": ep['seasonNumber'],
                "episode_num": ep['episodeNumber'],
                "title": next((t['primaryTitle'] for t in titles if t['tconst'] == ep_id), "No title found"),
                "rating": next((r['averageRating'] for r in ratings if r['tconst'] == ep_id), "No rating found")
            }
            pprint(episode_data)
            print("-" * 40)

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    print("Please download these files from https://datasets.imdbws.com/ and place them in the 'data' directory:")
    print("1. title.episode.tsv.gz")
    print("2. title.basics.tsv.gz")
    print("3. title.ratings.tsv.gz")
    
    input("\nPress Enter after downloading the files...")
    
    test_imdb_data() 