import json
import random
from pathlib import Path

VOICE_CONFIG_PATH = Path(__file__).parent / "voice_config.json"

def load_voice_config():
    with open(VOICE_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_random_phrase(config, category):
    phrases = config["default"]["phrases"].get(category, {}).get("random", [])
    if not phrases:
        return ""
    choice = random.choice(phrases)
    if isinstance(choice, list):
        choice = choice[0]
    return choice.get("text", "")