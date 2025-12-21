"""
Vercel Serverless Function for Six Degrees Flask API.
"""

import os
import sys
import logging

# Add backend to path so we can import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from flask import Flask
from flask_cors import CORS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def create_serverless_app() -> Flask:
    """Create Flask app configured for Vercel serverless."""
    app = Flask(__name__)
    
    # Configuration for serverless
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "prod-secret-key"),
        DATABASE="/tmp/sixdegrees.db",  # Vercel writable directory
        TESTING=False,
    )
    
    # Enable CORS for all origins in production
    CORS(app, origins="*")
    
    # Initialize database on cold start
    init_database(app.config["DATABASE"])
    
    # Register blueprints
    from app.routes.game_routes import game_bp
    from app.routes.stats_routes import stats_bp
    
    app.register_blueprint(game_bp, url_prefix="/api/game")
    app.register_blueprint(stats_bp, url_prefix="/api/stats")
    
    # Health check endpoint
    @app.route("/api/health")
    def health_check():
        from app.services.game_engine import GameEngine
        engine = GameEngine(db_path=app.config["DATABASE"])
        total_games = engine.get_total_games()
        return {
            "status": "healthy", 
            "game": "Six Degrees",
            "total_games_played": total_games
        }
    
    # Root API endpoint
    @app.route("/api")
    def api_root():
        return {"message": "Six Degrees API", "version": "1.0.0"}
    
    return app


def init_database(db_path: str):
    """Initialize the SQLite database with word associations."""
    import sqlite3
    
    # Check if database already exists
    if os.path.exists(db_path):
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word1_id INTEGER NOT NULL,
            word2_id INTEGER NOT NULL,
            FOREIGN KEY (word1_id) REFERENCES words(id),
            FOREIGN KEY (word2_id) REFERENCES words(id),
            UNIQUE(word1_id, word2_id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_word TEXT NOT NULL,
            end_word TEXT NOT NULL,
            player_path TEXT,
            optimal_path TEXT,
            player_length INTEGER,
            optimal_length INTEGER,
            score INTEGER,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_words_word ON words(word)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_conn_word1 ON connections(word1_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_conn_word2 ON connections(word2_id)")
    
    # Word associations - comprehensive list
    WORD_ASSOCIATIONS = [
        # Nature & Elements
        ("SUN", "LIGHT"), ("SUN", "HEAT"), ("SUN", "DAY"), ("SUN", "STAR"),
        ("MOON", "NIGHT"), ("MOON", "STAR"), ("MOON", "TIDE"), ("MOON", "LIGHT"),
        ("STAR", "NIGHT"), ("STAR", "SKY"), ("STAR", "SPACE"), ("STAR", "BRIGHT"),
        ("WATER", "OCEAN"), ("WATER", "RIVER"), ("WATER", "RAIN"), ("WATER", "DRINK"),
        ("OCEAN", "WAVE"), ("OCEAN", "FISH"), ("OCEAN", "BEACH"), ("OCEAN", "SALT"),
        ("RIVER", "FLOW"), ("RIVER", "FISH"), ("RIVER", "BRIDGE"), ("RIVER", "BANK"),
        ("RAIN", "CLOUD"), ("RAIN", "STORM"), ("RAIN", "UMBRELLA"), ("RAIN", "WET"),
        ("CLOUD", "SKY"), ("CLOUD", "WHITE"), ("CLOUD", "FLUFFY"), ("CLOUD", "WEATHER"),
        ("SKY", "BLUE"), ("SKY", "BIRD"), ("SKY", "FLY"), ("SKY", "HIGH"),
        ("FIRE", "HEAT"), ("FIRE", "BURN"), ("FIRE", "SMOKE"), ("FIRE", "RED"),
        ("WIND", "BLOW"), ("WIND", "AIR"), ("WIND", "STORM"), ("WIND", "COLD"),
        ("EARTH", "SOIL"), ("EARTH", "PLANET"), ("EARTH", "GROUND"), ("EARTH", "NATURE"),
        ("TREE", "LEAF"), ("TREE", "WOOD"), ("TREE", "FOREST"), ("TREE", "GREEN"), ("WOOD", "BARK"),
        ("FLOWER", "PETAL"), ("FLOWER", "GARDEN"), ("FLOWER", "SMELL"), ("FLOWER", "BEE"),
        ("MOUNTAIN", "HIGH"), ("MOUNTAIN", "SNOW"), ("MOUNTAIN", "CLIMB"), ("MOUNTAIN", "ROCK"),
        ("FOREST", "TREE"), ("FOREST", "ANIMAL"), ("FOREST", "GREEN"), ("FOREST", "NATURE"),
        
        # Animals
        ("DOG", "PET"), ("DOG", "BARK"), ("DOG", "LOYAL"), ("DOG", "FRIEND"),
        ("CAT", "PET"), ("CAT", "MEOW"), ("CAT", "MOUSE"), ("CAT", "SOFT"),
        ("BIRD", "FLY"), ("BIRD", "WING"), ("BIRD", "NEST"), ("BIRD", "SING"),
        ("FISH", "SWIM"), ("FISH", "WATER"), ("FISH", "SCALE"), ("FISH", "SEA"),
        ("HORSE", "RIDE"), ("HORSE", "FAST"), ("HORSE", "FARM"), ("HORSE", "RACE"),
        ("COW", "MILK"), ("COW", "FARM"), ("COW", "GRASS"), ("COW", "MOO"),
        ("LION", "KING"), ("LION", "ROAR"), ("LION", "WILD"), ("LION", "AFRICA"),
        ("ELEPHANT", "BIG"), ("ELEPHANT", "TRUNK"), ("ELEPHANT", "GRAY"), ("ELEPHANT", "MEMORY"),
        ("MOUSE", "SMALL"), ("MOUSE", "CHEESE"), ("MOUSE", "SQUEAK"), ("MOUSE", "COMPUTER"),
        ("BEAR", "FOREST"), ("BEAR", "HONEY"), ("BEAR", "BROWN"), ("BEAR", "SLEEP"),
        ("WOLF", "HOWL"), ("WOLF", "PACK"), ("WOLF", "WILD"), ("WOLF", "NIGHT"),
        ("SNAKE", "SLITHER"), ("SNAKE", "SCALE"), ("SNAKE", "POISON"), ("SNAKE", "LONG"),
        ("BEE", "HONEY"), ("BEE", "STING"), ("BEE", "FLOWER"), ("BEE", "BUZZ"),
        ("BUTTERFLY", "WING"), ("BUTTERFLY", "COLOR"), ("BUTTERFLY", "FLY"), ("BUTTERFLY", "BEAUTIFUL"),
        
        # Colors
        ("RED", "COLOR"), ("RED", "BLOOD"), ("RED", "APPLE"), ("RED", "FIRE"),
        ("BLUE", "COLOR"), ("BLUE", "SKY"), ("BLUE", "OCEAN"), ("BLUE", "SAD"),
        ("GREEN", "COLOR"), ("GREEN", "GRASS"), ("GREEN", "NATURE"), ("GREEN", "TREE"),
        ("YELLOW", "COLOR"), ("YELLOW", "SUN"), ("YELLOW", "BRIGHT"), ("YELLOW", "BANANA"),
        ("WHITE", "COLOR"), ("WHITE", "SNOW"), ("WHITE", "PURE"), ("WHITE", "CLEAN"),
        ("BLACK", "COLOR"), ("BLACK", "NIGHT"), ("BLACK", "DARK"), ("BLACK", "SHADOW"),
        ("ORANGE", "COLOR"), ("ORANGE", "FRUIT"), ("ORANGE", "SUNSET"), ("ORANGE", "JUICE"),
        ("PURPLE", "COLOR"), ("PURPLE", "ROYAL"), ("PURPLE", "GRAPE"), ("PURPLE", "VIOLET"),
        ("PINK", "COLOR"), ("PINK", "FLOWER"), ("PINK", "SOFT"), ("PINK", "LOVE"),
        ("BROWN", "COLOR"), ("BROWN", "EARTH"), ("BROWN", "WOOD"), ("BROWN", "CHOCOLATE"),
        ("GRAY", "COLOR"), ("GRAY", "CLOUD"), ("GRAY", "OLD"), ("GRAY", "STONE"),
        ("GOLD", "COLOR"), ("GOLD", "TREASURE"), ("GOLD", "RICH"), ("GOLD", "MEDAL"),
        ("SILVER", "COLOR"), ("SILVER", "METAL"), ("SILVER", "MOON"), ("SILVER", "SHINY"),
        
        # Food & Drink
        ("FOOD", "EAT"), ("FOOD", "HUNGRY"), ("FOOD", "COOK"), ("FOOD", "TASTE"),
        ("BREAD", "FOOD"), ("BREAD", "BUTTER"), ("BREAD", "BAKE"), ("BREAD", "WHEAT"),
        ("APPLE", "FRUIT"), ("APPLE", "RED"), ("APPLE", "TREE"), ("APPLE", "SWEET"),
        ("BANANA", "FRUIT"), ("BANANA", "YELLOW"), ("BANANA", "MONKEY"), ("BANANA", "PEEL"),
        ("ORANGE", "FRUIT"), ("ORANGE", "JUICE"), ("ORANGE", "VITAMIN"), ("ORANGE", "CITRUS"),
        ("GRAPE", "FRUIT"), ("GRAPE", "WINE"), ("GRAPE", "PURPLE"), ("GRAPE", "VINE"),
        ("MILK", "DRINK"), ("MILK", "COW"), ("MILK", "WHITE"), ("MILK", "CALCIUM"),
        ("COFFEE", "DRINK"), ("COFFEE", "MORNING"), ("COFFEE", "CAFFEINE"), ("COFFEE", "HOT"),
        ("TEA", "DRINK"), ("TEA", "HOT"), ("TEA", "LEAF"), ("TEA", "CUP"),
        ("WATER", "DRINK"), ("WATER", "CLEAR"), ("WATER", "LIFE"), ("WATER", "FRESH"),
        ("MEAT", "FOOD"), ("MEAT", "PROTEIN"), ("MEAT", "COOK"), ("MEAT", "ANIMAL"),
        ("CHEESE", "FOOD"), ("CHEESE", "MILK"), ("CHEESE", "YELLOW"), ("CHEESE", "MOUSE"),
        ("EGG", "FOOD"), ("EGG", "CHICKEN"), ("EGG", "BREAKFAST"), ("EGG", "OVAL"),
        ("RICE", "FOOD"), ("RICE", "GRAIN"), ("RICE", "ASIA"), ("RICE", "WHITE"),
        ("PIZZA", "FOOD"), ("PIZZA", "CHEESE"), ("PIZZA", "ITALY"), ("PIZZA", "SLICE"),
        ("CAKE", "FOOD"), ("CAKE", "SWEET"), ("CAKE", "BIRTHDAY"), ("CAKE", "BAKE"),
        ("ICE", "COLD"), ("ICE", "FROZEN"), ("ICE", "WATER"), ("ICE", "CREAM"),
        ("CREAM", "MILK"), ("CREAM", "SOFT"), ("CREAM", "WHITE"), ("CREAM", "SWEET"),
        ("CHOCOLATE", "SWEET"), ("CHOCOLATE", "BROWN"), ("CHOCOLATE", "CANDY"), ("CHOCOLATE", "COCOA"),
        ("CANDY", "SWEET"), ("CANDY", "SUGAR"), ("CANDY", "CHILD"), ("CANDY", "TREAT"),
        ("SUGAR", "SWEET"), ("SUGAR", "WHITE"), ("SUGAR", "ENERGY"), ("SUGAR", "TASTE"),
        ("SALT", "TASTE"), ("SALT", "OCEAN"), ("SALT", "WHITE"), ("SALT", "MINERAL"),
        
        # Body & Health
        ("BODY", "HUMAN"), ("BODY", "HEALTH"), ("BODY", "PHYSICAL"), ("BODY", "SKIN"),
        ("HEART", "LOVE"), ("HEART", "BEAT"), ("HEART", "BLOOD"), ("HEART", "BODY"),
        ("BRAIN", "THINK"), ("BRAIN", "MIND"), ("BRAIN", "SMART"), ("BRAIN", "HEAD"),
        ("EYE", "SEE"), ("EYE", "VISION"), ("EYE", "COLOR"), ("EYE", "LOOK"),
        ("EAR", "HEAR"), ("EAR", "SOUND"), ("EAR", "LISTEN"), ("EAR", "MUSIC"),
        ("HAND", "TOUCH"), ("HAND", "FINGER"), ("HAND", "HOLD"), ("HAND", "WRITE"),
        ("FOOT", "WALK"), ("FOOT", "SHOE"), ("FOOT", "STEP"), ("FOOT", "LEG"),
        ("HEAD", "THINK"), ("HEAD", "HAIR"), ("HEAD", "TOP"), ("HEAD", "BRAIN"),
        ("HAIR", "HEAD"), ("HAIR", "CUT"), ("HAIR", "LONG"), ("HAIR", "STYLE"),
        ("SKIN", "BODY"), ("SKIN", "SOFT"), ("SKIN", "TOUCH"), ("SKIN", "PROTECT"),
        ("BLOOD", "RED"), ("BLOOD", "BODY"), ("BLOOD", "LIFE"), ("BLOOD", "HEART"),
        ("BONE", "BODY"), ("BONE", "HARD"), ("BONE", "SKELETON"), ("BONE", "DOG"),
        ("MUSCLE", "STRONG"), ("MUSCLE", "BODY"), ("MUSCLE", "EXERCISE"), ("MUSCLE", "FLEX"),
        ("TOOTH", "BITE"), ("TOOTH", "WHITE"), ("TOOTH", "DENTIST"), ("TOOTH", "SMILE"),
        ("MOUTH", "SPEAK"), ("MOUTH", "EAT"), ("MOUTH", "KISS"), ("MOUTH", "TASTE"),
        ("NOSE", "SMELL"), ("NOSE", "BREATHE"), ("NOSE", "FACE"), ("NOSE", "AIR"),
        ("FACE", "HUMAN"), ("FACE", "EXPRESSION"), ("FACE", "SMILE"), ("FACE", "LOOK"),
        
        # Emotions & Feelings
        ("LOVE", "HEART"), ("LOVE", "HAPPY"), ("LOVE", "ROMANCE"), ("LOVE", "CARE"),
        ("HAPPY", "JOY"), ("HAPPY", "SMILE"), ("HAPPY", "GOOD"), ("HAPPY", "LAUGH"),
        ("SAD", "CRY"), ("SAD", "BLUE"), ("SAD", "UNHAPPY"), ("SAD", "TEAR"),
        ("ANGRY", "MAD"), ("ANGRY", "RED"), ("ANGRY", "SHOUT"), ("ANGRY", "EMOTION"),
        ("FEAR", "SCARED"), ("FEAR", "DARK"), ("FEAR", "DANGER"), ("FEAR", "BRAVE"),
        ("JOY", "HAPPY"), ("JOY", "LAUGH"), ("JOY", "CELEBRATE"), ("JOY", "SMILE"),
        ("HOPE", "FUTURE"), ("HOPE", "DREAM"), ("HOPE", "WISH"), ("HOPE", "BELIEVE"),
        ("PEACE", "CALM"), ("PEACE", "WAR"), ("PEACE", "QUIET"), ("PEACE", "HARMONY"),
        ("CALM", "QUIET"), ("CALM", "PEACE"), ("CALM", "RELAX"), ("CALM", "STILL"),
        
        # Time & Concepts
        ("TIME", "CLOCK"), ("TIME", "HOUR"), ("TIME", "PASS"), ("TIME", "MOMENT"),
        ("DAY", "SUN"), ("DAY", "LIGHT"), ("DAY", "MORNING"), ("DAY", "WORK"),
        ("NIGHT", "DARK"), ("NIGHT", "MOON"), ("NIGHT", "SLEEP"), ("NIGHT", "STAR"),
        ("MORNING", "EARLY"), ("MORNING", "COFFEE"), ("MORNING", "SUNRISE"), ("MORNING", "WAKE"),
        ("EVENING", "SUNSET"), ("EVENING", "DINNER"), ("EVENING", "NIGHT"), ("EVENING", "REST"),
        ("YEAR", "TIME"), ("YEAR", "CALENDAR"), ("YEAR", "SEASON"), ("YEAR", "AGE"),
        ("MONTH", "TIME"), ("MONTH", "CALENDAR"), ("MONTH", "WEEK"), ("MONTH", "MOON"),
        ("WEEK", "DAY"), ("WEEK", "TIME"), ("WEEK", "WORK"), ("WEEK", "SEVEN"),
        ("HOUR", "TIME"), ("HOUR", "CLOCK"), ("HOUR", "MINUTE"), ("HOUR", "WAIT"),
        ("MINUTE", "TIME"), ("MINUTE", "SECOND"), ("MINUTE", "SHORT"), ("MINUTE", "CLOCK"),
        ("SECOND", "TIME"), ("SECOND", "FAST"), ("SECOND", "MOMENT"), ("SECOND", "QUICK"),
        ("PAST", "HISTORY"), ("PAST", "MEMORY"), ("PAST", "OLD"), ("PAST", "TIME"),
        ("FUTURE", "TOMORROW"), ("FUTURE", "HOPE"), ("FUTURE", "DREAM"), ("FUTURE", "TIME"),
        ("NOW", "PRESENT"), ("NOW", "TODAY"), ("NOW", "MOMENT"), ("NOW", "TIME"),
        
        # Places & Buildings
        ("HOME", "HOUSE"), ("HOME", "FAMILY"), ("HOME", "SAFE"), ("HOME", "LOVE"),
        ("HOUSE", "BUILDING"), ("HOUSE", "LIVE"), ("HOUSE", "ROOM"), ("HOUSE", "DOOR"),
        ("ROOM", "SPACE"), ("ROOM", "HOUSE"), ("ROOM", "WALL"), ("ROOM", "FLOOR"),
        ("DOOR", "OPEN"), ("DOOR", "CLOSE"), ("DOOR", "ENTER"), ("DOOR", "HOUSE"),
        ("WINDOW", "GLASS"), ("WINDOW", "LIGHT"), ("WINDOW", "VIEW"), ("WINDOW", "OPEN"),
        ("SCHOOL", "LEARN"), ("SCHOOL", "STUDENT"), ("SCHOOL", "TEACHER"), ("SCHOOL", "STUDY"),
        ("OFFICE", "WORK"), ("OFFICE", "DESK"), ("OFFICE", "COMPUTER"), ("OFFICE", "BUSINESS"),
        ("HOSPITAL", "DOCTOR"), ("HOSPITAL", "SICK"), ("HOSPITAL", "HEALTH"), ("HOSPITAL", "NURSE"),
        ("STORE", "SHOP"), ("STORE", "BUY"), ("STORE", "SELL"), ("STORE", "MONEY"),
        ("CHURCH", "RELIGION"), ("CHURCH", "PRAY"), ("CHURCH", "GOD"), ("CHURCH", "FAITH"),
        ("CITY", "URBAN"), ("CITY", "BUILDING"), ("CITY", "PEOPLE"), ("CITY", "BUSY"),
        ("TOWN", "SMALL"), ("TOWN", "CITY"), ("TOWN", "COMMUNITY"), ("TOWN", "PEOPLE"),
        ("VILLAGE", "SMALL"), ("VILLAGE", "RURAL"), ("VILLAGE", "COMMUNITY"), ("VILLAGE", "FARM"),
        ("COUNTRY", "NATION"), ("COUNTRY", "LAND"), ("COUNTRY", "RURAL"), ("COUNTRY", "FLAG"),
        ("WORLD", "EARTH"), ("WORLD", "GLOBE"), ("WORLD", "PEOPLE"), ("WORLD", "BIG"),
        
        # Objects & Things
        ("BOOK", "READ"), ("BOOK", "PAGE"), ("BOOK", "STORY"), ("BOOK", "LIBRARY"),
        ("PEN", "WRITE"), ("PEN", "INK"), ("PEN", "PAPER"), ("PEN", "DRAW"),
        ("PAPER", "WRITE"), ("PAPER", "WHITE"), ("PAPER", "THIN"), ("PAPER", "TREE"),
        ("TABLE", "FURNITURE"), ("TABLE", "EAT"), ("TABLE", "WOOD"), ("TABLE", "FLAT"),
        ("CHAIR", "SIT"), ("CHAIR", "FURNITURE"), ("CHAIR", "WOOD"), ("CHAIR", "DESK"),
        ("BED", "SLEEP"), ("BED", "REST"), ("BED", "PILLOW"), ("BED", "ROOM"),
        ("PHONE", "CALL"), ("PHONE", "TALK"), ("PHONE", "MOBILE"), ("PHONE", "RING"),
        ("COMPUTER", "TECHNOLOGY"), ("COMPUTER", "INTERNET"), ("COMPUTER", "WORK"), ("COMPUTER", "SCREEN"),
        ("CAR", "DRIVE"), ("CAR", "ROAD"), ("CAR", "FAST"), ("CAR", "WHEEL"),
        ("WHEEL", "ROUND"), ("WHEEL", "CAR"), ("WHEEL", "SPIN"), ("WHEEL", "TIRE"),
        ("KEY", "LOCK"), ("KEY", "OPEN"), ("KEY", "DOOR"), ("KEY", "METAL"),
        ("LOCK", "KEY"), ("LOCK", "SAFE"), ("LOCK", "CLOSE"), ("LOCK", "SECURE"),
        ("CLOCK", "TIME"), ("CLOCK", "TICK"), ("CLOCK", "HOUR"), ("CLOCK", "WALL"),
        ("WATCH", "TIME"), ("WATCH", "WRIST"), ("WATCH", "LOOK"), ("WATCH", "SEE"),
        ("MIRROR", "REFLECT"), ("MIRROR", "GLASS"), ("MIRROR", "FACE"), ("MIRROR", "IMAGE"),
        ("CAMERA", "PHOTO"), ("CAMERA", "PICTURE"), ("CAMERA", "LENS"), ("CAMERA", "FILM"),
        ("PICTURE", "IMAGE"), ("PICTURE", "FRAME"), ("PICTURE", "ART"), ("PICTURE", "PHOTO"),
        ("PHOTO", "CAMERA"), ("PHOTO", "MEMORY"), ("PHOTO", "IMAGE"), ("PHOTO", "PICTURE"),
        
        # Clothing
        ("CLOTHES", "WEAR"), ("CLOTHES", "FASHION"), ("CLOTHES", "FABRIC"), ("CLOTHES", "DRESS"),
        ("SHIRT", "CLOTHES"), ("SHIRT", "WEAR"), ("SHIRT", "BUTTON"), ("SHIRT", "COTTON"),
        ("PANTS", "CLOTHES"), ("PANTS", "LEG"), ("PANTS", "WEAR"), ("PANTS", "JEAN"),
        ("DRESS", "CLOTHES"), ("DRESS", "WOMAN"), ("DRESS", "WEAR"), ("DRESS", "PRETTY"),
        ("SHOE", "FOOT"), ("SHOE", "WALK"), ("SHOE", "WEAR"), ("SHOE", "LEATHER"),
        ("HAT", "HEAD"), ("HAT", "WEAR"), ("HAT", "SUN"), ("HAT", "STYLE"),
        ("COAT", "WARM"), ("COAT", "WINTER"), ("COAT", "WEAR"), ("COAT", "COLD"),
        ("JACKET", "WEAR"), ("JACKET", "WARM"), ("JACKET", "COAT"), ("JACKET", "LEATHER"),
        
        # Music & Art
        ("MUSIC", "SOUND"), ("MUSIC", "SING"), ("MUSIC", "INSTRUMENT"), ("MUSIC", "LISTEN"),
        ("SONG", "MUSIC"), ("SONG", "SING"), ("SONG", "LYRICS"), ("SONG", "MELODY"),
        ("DANCE", "MUSIC"), ("DANCE", "MOVE"), ("DANCE", "RHYTHM"), ("DANCE", "PARTY"),
        ("SING", "VOICE"), ("SING", "SONG"), ("SING", "MUSIC"), ("SING", "BIRD"),
        ("PIANO", "MUSIC"), ("PIANO", "KEY"), ("PIANO", "INSTRUMENT"), ("PIANO", "PLAY"),
        ("GUITAR", "MUSIC"), ("GUITAR", "STRING"), ("GUITAR", "PLAY"), ("GUITAR", "ROCK"),
        ("DRUM", "BEAT"), ("DRUM", "MUSIC"), ("DRUM", "RHYTHM"), ("DRUM", "LOUD"),
        ("ART", "CREATE"), ("ART", "PAINT"), ("ART", "MUSEUM"), ("ART", "BEAUTY"),
        ("PAINT", "COLOR"), ("PAINT", "BRUSH"), ("PAINT", "ART"), ("PAINT", "DRAW"),
        ("DRAW", "PEN"), ("DRAW", "PICTURE"), ("DRAW", "ART"), ("DRAW", "LINE"),
        
        # Sports & Games
        ("GAME", "PLAY"), ("GAME", "FUN"), ("GAME", "WIN"), ("GAME", "SPORT"),
        ("PLAY", "FUN"), ("PLAY", "GAME"), ("PLAY", "CHILD"), ("PLAY", "TOY"),
        ("SPORT", "GAME"), ("SPORT", "EXERCISE"), ("SPORT", "ATHLETE"), ("SPORT", "TEAM"),
        ("BALL", "ROUND"), ("BALL", "GAME"), ("BALL", "THROW"), ("BALL", "KICK"),
        ("TEAM", "GROUP"), ("TEAM", "SPORT"), ("TEAM", "WORK"), ("TEAM", "WIN"),
        ("WIN", "GAME"), ("WIN", "LOSE"), ("WIN", "VICTORY"), ("WIN", "PRIZE"),
        ("LOSE", "WIN"), ("LOSE", "GAME"), ("LOSE", "FIND"), ("LOSE", "FAIL"),
        ("RUN", "FAST"), ("RUN", "EXERCISE"), ("RUN", "LEG"), ("RUN", "MARATHON"),
        ("JUMP", "HIGH"), ("JUMP", "FLY"), ("JUMP", "LEAP"), ("JUMP", "EXERCISE"),
        ("SWIM", "WATER"), ("SWIM", "POOL"), ("SWIM", "FISH"), ("SWIM", "EXERCISE"),
        
        # Work & Education
        ("WORK", "JOB"), ("WORK", "OFFICE"), ("WORK", "MONEY"), ("WORK", "EFFORT"),
        ("JOB", "WORK"), ("JOB", "CAREER"), ("JOB", "MONEY"), ("JOB", "EMPLOY"),
        ("MONEY", "RICH"), ("MONEY", "BUY"), ("MONEY", "BANK"), ("MONEY", "WORK"),
        ("BANK", "MONEY"), ("BANK", "SAVE"), ("BANK", "RIVER"), ("BANK", "LOAN"),
        ("LEARN", "SCHOOL"), ("LEARN", "STUDY"), ("LEARN", "KNOWLEDGE"), ("LEARN", "TEACH"),
        ("TEACH", "TEACHER"), ("TEACH", "LEARN"), ("TEACH", "SCHOOL"), ("TEACH", "KNOWLEDGE"),
        ("TEACHER", "SCHOOL"), ("TEACHER", "STUDENT"), ("TEACHER", "LEARN"), ("TEACHER", "CLASS"),
        ("STUDENT", "LEARN"), ("STUDENT", "SCHOOL"), ("STUDENT", "STUDY"), ("STUDENT", "TEACHER"),
        ("STUDY", "LEARN"), ("STUDY", "BOOK"), ("STUDY", "SCHOOL"), ("STUDY", "EXAM"),
        ("READ", "BOOK"), ("READ", "LEARN"), ("READ", "WORD"), ("READ", "STORY"),
        ("WRITE", "PEN"), ("WRITE", "PAPER"), ("WRITE", "WORD"), ("WRITE", "STORY"),
        ("WORD", "LANGUAGE"), ("WORD", "SPEAK"), ("WORD", "WRITE"), ("WORD", "MEANING"),
        
        # Technology
        ("TECHNOLOGY", "COMPUTER"), ("TECHNOLOGY", "FUTURE"), ("TECHNOLOGY", "SCIENCE"), ("TECHNOLOGY", "MODERN"),
        ("INTERNET", "COMPUTER"), ("INTERNET", "WEB"), ("INTERNET", "ONLINE"), ("INTERNET", "CONNECT"),
        ("SCREEN", "COMPUTER"), ("SCREEN", "WATCH"), ("SCREEN", "DISPLAY"), ("SCREEN", "PHONE"),
        ("EMAIL", "INTERNET"), ("EMAIL", "SEND"), ("EMAIL", "MESSAGE"), ("EMAIL", "COMPUTER"),
        ("ROBOT", "MACHINE"), ("ROBOT", "TECHNOLOGY"), ("ROBOT", "FUTURE"), ("ROBOT", "METAL"),
        ("MACHINE", "WORK"), ("MACHINE", "METAL"), ("MACHINE", "TECHNOLOGY"), ("MACHINE", "ENGINE"),
        
        # Weather
        ("WEATHER", "CLIMATE"), ("WEATHER", "RAIN"), ("WEATHER", "SUN"), ("WEATHER", "FORECAST"),
        ("STORM", "RAIN"), ("STORM", "WIND"), ("STORM", "THUNDER"), ("STORM", "WEATHER"),
        ("THUNDER", "STORM"), ("THUNDER", "LOUD"), ("THUNDER", "LIGHTNING"), ("THUNDER", "SOUND"),
        ("LIGHTNING", "STORM"), ("LIGHTNING", "FAST"), ("LIGHTNING", "BRIGHT"), ("LIGHTNING", "THUNDER"),
        ("SNOW", "COLD"), ("SNOW", "WHITE"), ("SNOW", "WINTER"), ("SNOW", "ICE"),
        ("COLD", "ICE"), ("COLD", "WINTER"), ("COLD", "FREEZE"), ("COLD", "COOL"),
        ("HOT", "HEAT"), ("HOT", "SUMMER"), ("HOT", "WARM"), ("HOT", "FIRE"),
        ("WARM", "HOT"), ("WARM", "COMFORTABLE"), ("WARM", "COAT"), ("WARM", "SUN"),
        ("COOL", "COLD"), ("COOL", "FRESH"), ("COOL", "NICE"), ("COOL", "STYLE"),
        
        # Space
        ("SPACE", "UNIVERSE"), ("SPACE", "STAR"), ("SPACE", "PLANET"), ("SPACE", "ASTRONAUT"),
        ("PLANET", "EARTH"), ("PLANET", "SPACE"), ("PLANET", "ORBIT"), ("PLANET", "ROUND"),
        ("UNIVERSE", "SPACE"), ("UNIVERSE", "BIG"), ("UNIVERSE", "STAR"), ("UNIVERSE", "GALAXY"),
        ("GALAXY", "STAR"), ("GALAXY", "SPACE"), ("GALAXY", "UNIVERSE"), ("GALAXY", "MILKY"),
        ("ROCKET", "SPACE"), ("ROCKET", "FLY"), ("ROCKET", "FAST"), ("ROCKET", "LAUNCH"),
        ("ASTRONAUT", "SPACE"), ("ASTRONAUT", "MOON"), ("ASTRONAUT", "FLY"), ("ASTRONAUT", "SUIT"),
        
        # Abstract concepts
        ("LIFE", "LIVE"), ("LIFE", "DEATH"), ("LIFE", "BIRTH"), ("LIFE", "EXPERIENCE"),
        ("DEATH", "END"), ("DEATH", "LIFE"), ("DEATH", "DARK"), ("DEATH", "FEAR"),
        ("BIRTH", "BABY"), ("BIRTH", "LIFE"), ("BIRTH", "NEW"), ("BIRTH", "MOTHER"),
        ("DREAM", "SLEEP"), ("DREAM", "HOPE"), ("DREAM", "IMAGINATION"), ("DREAM", "NIGHT"),
        ("IDEA", "THINK"), ("IDEA", "BRAIN"), ("IDEA", "CREATE"), ("IDEA", "NEW"),
        ("THINK", "BRAIN"), ("THINK", "IDEA"), ("THINK", "MIND"), ("THINK", "WONDER"),
        ("MIND", "BRAIN"), ("MIND", "THINK"), ("MIND", "THOUGHT"), ("MIND", "IDEA"),
        ("MEMORY", "REMEMBER"), ("MEMORY", "BRAIN"), ("MEMORY", "PAST"), ("MEMORY", "PHOTO"),
        ("TRUTH", "HONEST"), ("TRUTH", "REAL"), ("TRUTH", "LIE"), ("TRUTH", "FACT"),
        ("LIE", "FALSE"), ("LIE", "TRUTH"), ("LIE", "DECEIVE"), ("LIE", "WRONG"),
        ("REAL", "TRUE"), ("REAL", "FAKE"), ("REAL", "ACTUAL"), ("REAL", "EXIST"),
        ("FAKE", "FALSE"), ("FAKE", "REAL"), ("FAKE", "COPY"), ("FAKE", "PRETEND"),
        
        # Actions
        ("WALK", "FOOT"), ("WALK", "MOVE"), ("WALK", "STEP"), ("WALK", "SLOW"),
        ("MOVE", "MOTION"), ("MOVE", "WALK"), ("MOVE", "CHANGE"), ("MOVE", "HOUSE"),
        ("STOP", "END"), ("STOP", "WAIT"), ("STOP", "HALT"), ("STOP", "GO"),
        ("GO", "MOVE"), ("GO", "START"), ("GO", "LEAVE"), ("GO", "STOP"),
        ("START", "BEGIN"), ("START", "GO"), ("START", "NEW"), ("START", "FIRST"),
        ("END", "FINISH"), ("END", "STOP"), ("END", "LAST"), ("END", "START"),
        ("OPEN", "DOOR"), ("OPEN", "CLOSE"), ("OPEN", "START"), ("OPEN", "WIDE"),
        ("CLOSE", "NEAR"), ("CLOSE", "SHUT"), ("CLOSE", "END"), ("CLOSE", "OPEN"),
        ("PUSH", "FORCE"), ("PUSH", "PULL"), ("PUSH", "MOVE"), ("PUSH", "BUTTON"),
        ("PULL", "PUSH"), ("PULL", "DRAG"), ("PULL", "FORCE"), ("PULL", "ATTRACT"),
        ("GIVE", "TAKE"), ("GIVE", "GIFT"), ("GIVE", "SHARE"), ("GIVE", "OFFER"),
        ("TAKE", "GIVE"), ("TAKE", "GRAB"), ("TAKE", "GET"), ("TAKE", "HOLD"),
        ("HOLD", "HAND"), ("HOLD", "GRIP"), ("HOLD", "KEEP"), ("HOLD", "CARRY"),
        ("THROW", "BALL"), ("THROW", "CATCH"), ("THROW", "TOSS"), ("THROW", "ARM"),
        ("CATCH", "THROW"), ("CATCH", "GRAB"), ("CATCH", "BALL"), ("CATCH", "HOLD"),
        ("BREAK", "FIX"), ("BREAK", "CRACK"), ("BREAK", "DESTROY"), ("BREAK", "GLASS"),
        ("FIX", "REPAIR"), ("FIX", "BREAK"), ("FIX", "SOLVE"), ("FIX", "TOOL"),
        ("BUILD", "CREATE"), ("BUILD", "CONSTRUCT"), ("BUILD", "HOUSE"), ("BUILD", "MAKE"),
        ("CREATE", "MAKE"), ("CREATE", "ART"), ("CREATE", "NEW"), ("CREATE", "BUILD"),
        ("MAKE", "CREATE"), ("MAKE", "BUILD"), ("MAKE", "DO"), ("MAKE", "PRODUCE"),
        ("DESTROY", "BREAK"), ("DESTROY", "RUIN"), ("DESTROY", "END"), ("DESTROY", "DAMAGE"),
        
        # Family
        ("FAMILY", "HOME"), ("FAMILY", "LOVE"), ("FAMILY", "PARENT"), ("FAMILY", "CHILD"),
        ("MOTHER", "PARENT"), ("MOTHER", "LOVE"), ("MOTHER", "WOMAN"), ("MOTHER", "BIRTH"),
        ("FATHER", "PARENT"), ("FATHER", "MAN"), ("FATHER", "FAMILY"), ("FATHER", "CHILD"),
        ("PARENT", "CHILD"), ("PARENT", "FAMILY"), ("PARENT", "MOTHER"), ("PARENT", "FATHER"),
        ("CHILD", "YOUNG"), ("CHILD", "PARENT"), ("CHILD", "PLAY"), ("CHILD", "GROW"),
        ("BABY", "SMALL"), ("BABY", "CHILD"), ("BABY", "CRY"), ("BABY", "BIRTH"),
        ("FRIEND", "LOVE"), ("FRIEND", "TRUST"), ("FRIEND", "HELP"), ("FRIEND", "SOCIAL"),
        ("WIFE", "HUSBAND"), ("WIFE", "MARRIAGE"), ("WIFE", "WOMAN"), ("WIFE", "LOVE"),
        ("HUSBAND", "WIFE"), ("HUSBAND", "MARRIAGE"), ("HUSBAND", "MAN"), ("HUSBAND", "LOVE"),
        ("MARRIAGE", "LOVE"), ("MARRIAGE", "WEDDING"), ("MARRIAGE", "RING"), ("MARRIAGE", "FAMILY"),
        ("WEDDING", "MARRIAGE"), ("WEDDING", "BRIDE"), ("WEDDING", "CELEBRATE"), ("WEDDING", "DRESS"),
        ("RING", "CIRCLE"), ("RING", "FINGER"), ("RING", "WEDDING"), ("RING", "GOLD"),
        
        # Size & Quantity
        ("BIG", "LARGE"), ("BIG", "SMALL"), ("BIG", "SIZE"), ("BIG", "HUGE"),
        ("SMALL", "LITTLE"), ("SMALL", "BIG"), ("SMALL", "TINY"), ("SMALL", "SIZE"),
        ("LONG", "SHORT"), ("LONG", "LENGTH"), ("LONG", "TIME"), ("LONG", "TALL"),
        ("SHORT", "LONG"), ("SHORT", "SMALL"), ("SHORT", "BRIEF"), ("SHORT", "HEIGHT"),
        ("TALL", "HIGH"), ("TALL", "SHORT"), ("TALL", "HEIGHT"), ("TALL", "LONG"),
        ("HIGH", "LOW"), ("HIGH", "TALL"), ("HIGH", "SKY"), ("HIGH", "UP"),
        ("LOW", "HIGH"), ("LOW", "DOWN"), ("LOW", "GROUND"), ("LOW", "SMALL"),
        ("FAST", "QUICK"), ("FAST", "SLOW"), ("FAST", "SPEED"), ("FAST", "RUN"),
        ("SLOW", "FAST"), ("SLOW", "SPEED"), ("SLOW", "WAIT"), ("SLOW", "TURTLE"),
        ("HEAVY", "LIGHT"), ("HEAVY", "WEIGHT"), ("HEAVY", "STRONG"), ("HEAVY", "BIG"),
        ("LIGHT", "DARK"), ("LIGHT", "SUN"), ("LIGHT", "HEAVY"), ("LIGHT", "BRIGHT"),
        ("DARK", "LIGHT"), ("DARK", "NIGHT"), ("DARK", "BLACK"), ("DARK", "SHADOW"),
        ("BRIGHT", "LIGHT"), ("BRIGHT", "DARK"), ("BRIGHT", "SUN"), ("BRIGHT", "SMART"),
        
        # Directions
        ("UP", "DOWN"), ("UP", "HIGH"), ("UP", "SKY"), ("UP", "RISE"),
        ("DOWN", "UP"), ("DOWN", "LOW"), ("DOWN", "FALL"), ("DOWN", "GROUND"),
        ("LEFT", "RIGHT"), ("LEFT", "DIRECTION"), ("LEFT", "TURN"), ("LEFT", "SIDE"),
        ("RIGHT", "LEFT"), ("RIGHT", "CORRECT"), ("RIGHT", "DIRECTION"), ("RIGHT", "TRUE"),
        ("FRONT", "BACK"), ("FRONT", "FORWARD"), ("FRONT", "FACE"), ("FRONT", "FIRST"),
        ("BACK", "FRONT"), ("BACK", "BEHIND"), ("BACK", "RETURN"), ("BACK", "REAR"),
        ("NORTH", "SOUTH"), ("NORTH", "DIRECTION"), ("NORTH", "COLD"), ("NORTH", "POLE"),
        ("SOUTH", "NORTH"), ("SOUTH", "DIRECTION"), ("SOUTH", "WARM"), ("SOUTH", "POLE"),
        ("EAST", "WEST"), ("EAST", "DIRECTION"), ("EAST", "SUNRISE"), ("EAST", "ASIA"),
        ("WEST", "EAST"), ("WEST", "DIRECTION"), ("WEST", "SUNSET"), ("WEST", "AMERICA"),
    ]
    
    # Insert words
    words = set()
    for word1, word2 in WORD_ASSOCIATIONS:
        words.add(word1)
        words.add(word2)
    
    for word in words:
        cursor.execute("INSERT OR IGNORE INTO words (word) VALUES (?)", (word.upper(),))
    
    conn.commit()
    
    # Insert connections
    for word1, word2 in WORD_ASSOCIATIONS:
        cursor.execute("SELECT id FROM words WHERE word = ?", (word1.upper(),))
        id1 = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM words WHERE word = ?", (word2.upper(),))
        id2 = cursor.fetchone()[0]
        
        # Add bidirectional connections
        cursor.execute("INSERT OR IGNORE INTO connections (word1_id, word2_id) VALUES (?, ?)", (id1, id2))
        cursor.execute("INSERT OR IGNORE INTO connections (word1_id, word2_id) VALUES (?, ?)", (id2, id1))
    
    conn.commit()
    conn.close()
    logging.info(f"Database initialized at {db_path} with {len(words)} words")


# Create the app instance for Vercel
app = create_serverless_app()

