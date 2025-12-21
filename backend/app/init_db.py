"""
Database initialization script for Six Degrees.

Creates tables and populates with word association data.
"""

from app.models.database import Database
from app.models.word_graph import WordGraph


# Word associations - curated semantic connections
# Each tuple: (word1, word2) represents a valid connection
WORD_ASSOCIATIONS = [
    # Nature & Elements
    ("OCEAN", "WAVE"), ("WAVE", "BEACH"), ("BEACH", "SAND"),
    ("SAND", "DESERT"), ("DESERT", "CAMEL"), ("CAMEL", "HUMP"),
    ("OCEAN", "FISH"), ("FISH", "SWIM"), ("SWIM", "POOL"),
    ("POOL", "WATER"), ("WATER", "RAIN"), ("RAIN", "CLOUD"),
    ("CLOUD", "SKY"), ("SKY", "BLUE"), ("BLUE", "COLOR"),
    ("WATER", "DRINK"), ("DRINK", "THIRST"), ("THIRST", "DESERT"),
    
    # Technology
    ("KEYBOARD", "TYPE"), ("TYPE", "WRITE"), ("WRITE", "PEN"),
    ("PEN", "INK"), ("INK", "SQUID"), ("SQUID", "OCEAN"),
    ("KEYBOARD", "COMPUTER"), ("COMPUTER", "SCREEN"), ("SCREEN", "MOVIE"),
    ("MOVIE", "ACTOR"), ("ACTOR", "STAGE"), ("STAGE", "THEATER"),
    ("COMPUTER", "MOUSE"), ("MOUSE", "CHEESE"), ("CHEESE", "PIZZA"),
    ("COMPUTER", "CODE"), ("CODE", "SECRET"), ("SECRET", "SPY"),
    
    # Animals
    ("DOG", "BARK"), ("BARK", "TREE"), ("TREE", "LEAF"),
    ("LEAF", "FALL"), ("FALL", "AUTUMN"), ("AUTUMN", "SEASON"),
    ("DOG", "PET"), ("PET", "CAT"), ("CAT", "MEOW"),
    ("CAT", "WHISKER"), ("WHISKER", "BEARD"), ("BEARD", "FACE"),
    ("BIRD", "FLY"), ("FLY", "AIRPLANE"), ("AIRPLANE", "TRAVEL"),
    ("BIRD", "NEST"), ("NEST", "EGG"), ("EGG", "BREAKFAST"),
    ("FISH", "SCALE"), ("SCALE", "WEIGHT"), ("WEIGHT", "HEAVY"),
    
    # Food & Cooking
    ("PIZZA", "CHEESE"), ("PIZZA", "ITALY"), ("ITALY", "ROME"),
    ("ROME", "ANCIENT"), ("ANCIENT", "HISTORY"), ("HISTORY", "BOOK"),
    ("BOOK", "READ"), ("READ", "GLASSES"), ("GLASSES", "EYE"),
    ("BREAKFAST", "MORNING"), ("MORNING", "SUN"), ("SUN", "STAR"),
    ("STAR", "SPACE"), ("SPACE", "ROCKET"), ("ROCKET", "FAST"),
    ("COFFEE", "MORNING"), ("COFFEE", "BEAN"), ("BEAN", "PLANT"),
    ("PLANT", "GROW"), ("GROW", "TALL"), ("TALL", "GIRAFFE"),
    
    # Music & Arts
    ("MUSIC", "SONG"), ("SONG", "BIRD"), ("SONG", "SING"),
    ("SING", "VOICE"), ("VOICE", "LOUD"), ("LOUD", "NOISE"),
    ("MUSIC", "PIANO"), ("PIANO", "KEY"), ("KEY", "LOCK"),
    ("LOCK", "DOOR"), ("DOOR", "HOUSE"), ("HOUSE", "HOME"),
    ("GUITAR", "STRING"), ("STRING", "ROPE"), ("ROPE", "CLIMB"),
    ("CLIMB", "MOUNTAIN"), ("MOUNTAIN", "SNOW"), ("SNOW", "WINTER"),
    ("PAINT", "ART"), ("ART", "MUSEUM"), ("MUSEUM", "HISTORY"),
    ("PAINT", "COLOR"), ("COLOR", "RAINBOW"), ("RAINBOW", "RAIN"),
    
    # Sports & Games
    ("BALL", "GAME"), ("GAME", "PLAY"), ("PLAY", "FUN"),
    ("FUN", "LAUGH"), ("LAUGH", "JOKE"), ("JOKE", "FUNNY"),
    ("BALL", "KICK"), ("KICK", "FOOT"), ("FOOT", "SHOE"),
    ("SHOE", "LEATHER"), ("LEATHER", "COW"), ("COW", "MILK"),
    ("MILK", "DRINK"), ("SWIM", "RACE"), ("RACE", "CAR"),
    ("CAR", "DRIVE"), ("DRIVE", "ROAD"), ("ROAD", "TRIP"),
    
    # Weather & Seasons
    ("WINTER", "COLD"), ("COLD", "ICE"), ("ICE", "SKATE"),
    ("SKATE", "WHEEL"), ("WHEEL", "SPIN"), ("SPIN", "DIZZY"),
    ("SUMMER", "HOT"), ("HOT", "FIRE"), ("FIRE", "BURN"),
    ("BURN", "CANDLE"), ("CANDLE", "LIGHT"), ("LIGHT", "SUN"),
    ("SPRING", "FLOWER"), ("FLOWER", "BEE"), ("BEE", "HONEY"),
    ("HONEY", "SWEET"), ("SWEET", "CANDY"), ("CANDY", "SUGAR"),
    
    # Body & Health
    ("FACE", "SMILE"), ("SMILE", "HAPPY"), ("HAPPY", "JOY"),
    ("JOY", "CELEBRATION"), ("CELEBRATION", "PARTY"), ("PARTY", "BALLOON"),
    ("BALLOON", "FLOAT"), ("FLOAT", "BOAT"), ("BOAT", "SAIL"),
    ("SAIL", "WIND"), ("WIND", "BLOW"), ("BLOW", "CANDLE"),
    ("EYE", "SEE"), ("SEE", "LOOK"), ("LOOK", "MIRROR"),
    ("MIRROR", "REFLECT"), ("REFLECT", "THINK"), ("THINK", "BRAIN"),
    ("BRAIN", "SMART"), ("SMART", "PHONE"), ("PHONE", "CALL"),
    
    # Work & School
    ("BOOK", "LIBRARY"), ("LIBRARY", "QUIET"), ("QUIET", "SILENCE"),
    ("SILENCE", "NIGHT"), ("NIGHT", "MOON"), ("MOON", "SPACE"),
    ("SCHOOL", "LEARN"), ("LEARN", "TEACH"), ("TEACH", "TEACHER"),
    ("TEACHER", "CLASS"), ("CLASS", "STUDENT"), ("STUDENT", "STUDY"),
    ("STUDY", "EXAM"), ("EXAM", "TEST"), ("TEST", "PASS"),
    ("PASS", "FAIL"), ("FAIL", "TRY"), ("TRY", "EFFORT"),
    
    # Home & Family
    ("HOME", "FAMILY"), ("FAMILY", "LOVE"), ("LOVE", "HEART"),
    ("HEART", "BEAT"), ("BEAT", "DRUM"), ("DRUM", "MUSIC"),
    ("HOUSE", "ROOF"), ("ROOF", "TOP"), ("TOP", "MOUNTAIN"),
    ("BED", "SLEEP"), ("SLEEP", "DREAM"), ("DREAM", "NIGHT"),
    ("KITCHEN", "COOK"), ("COOK", "CHEF"), ("CHEF", "HAT"),
    ("HAT", "HEAD"), ("HEAD", "BRAIN"),
    
    # Transportation
    ("CAR", "WHEEL"), ("AIRPLANE", "WING"), ("WING", "BIRD"),
    ("TRAIN", "TRACK"), ("TRACK", "FOLLOW"), ("FOLLOW", "LEADER"),
    ("LEADER", "PRESIDENT"), ("PRESIDENT", "COUNTRY"), ("COUNTRY", "FLAG"),
    ("BOAT", "OCEAN"), ("ROCKET", "SPACE"), ("BIKE", "PEDAL"),
    ("PEDAL", "FOOT"), ("BICYCLE", "CHAIN"), ("CHAIN", "LINK"),
    
    # Abstract & Emotions
    ("HAPPY", "SAD"), ("SAD", "CRY"), ("CRY", "TEAR"),
    ("TEAR", "WATER"), ("ANGER", "RED"), ("RED", "FIRE"),
    ("FEAR", "DARK"), ("DARK", "NIGHT"), ("BRAVE", "HERO"),
    ("HERO", "CAPE"), ("CAPE", "FLY"), ("PEACE", "QUIET"),
    ("QUIET", "LIBRARY"), ("HOPE", "LIGHT"), ("LIGHT", "BRIGHT"),
    
    # Time & Space
    ("TIME", "CLOCK"), ("CLOCK", "TICK"), ("TICK", "BUG"),
    ("BUG", "INSECT"), ("INSECT", "ANT"), ("ANT", "SMALL"),
    ("SMALL", "TINY"), ("TINY", "HUGE"), ("HUGE", "ELEPHANT"),
    ("ELEPHANT", "TRUNK"), ("TRUNK", "TREE"), ("FAST", "SLOW"),
    ("SLOW", "TURTLE"), ("TURTLE", "SHELL"), ("SHELL", "BEACH"),
    
    # More connections for density
    ("STAR", "NIGHT"), ("OCEAN", "BLUE"), ("FIRE", "WARM"),
    ("WARM", "COLD"), ("SNOW", "WHITE"), ("WHITE", "COLOR"),
    ("BLACK", "COLOR"), ("BLACK", "NIGHT"), ("GREEN", "GRASS"),
    ("GRASS", "LAWN"), ("LAWN", "HOUSE"), ("YELLOW", "SUN"),
    ("YELLOW", "BANANA"), ("BANANA", "MONKEY"), ("MONKEY", "CLIMB"),
    ("ORANGE", "FRUIT"), ("FRUIT", "APPLE"), ("APPLE", "TREE"),
    ("APPLE", "PHONE"), ("GOLD", "TREASURE"), ("TREASURE", "PIRATE"),
    ("PIRATE", "SHIP"), ("SHIP", "OCEAN"), ("SILVER", "MOON"),
    ("DIAMOND", "RING"), ("RING", "WEDDING"), ("WEDDING", "LOVE"),
    ("KING", "CROWN"), ("CROWN", "GOLD"), ("QUEEN", "KING"),
    ("CASTLE", "KING"), ("CASTLE", "STONE"), ("STONE", "ROCK"),
    ("ROCK", "MUSIC"), ("ROCK", "MOUNTAIN"), ("PAPER", "WRITE"),
    ("PAPER", "BOOK"), ("PEN", "WRITE"), ("PENCIL", "DRAW"),
    ("DRAW", "ART"), ("PICTURE", "FRAME"), ("FRAME", "GLASS"),
    ("GLASS", "WINDOW"), ("WINDOW", "HOUSE"), ("WINDOW", "SEE"),
    
    # Colors - all colors connect to COLOR
    ("YELLOW", "COLOR"), ("RED", "COLOR"), ("GREEN", "COLOR"),
    ("ORANGE", "COLOR"), ("PURPLE", "COLOR"), ("PINK", "COLOR"),
    ("BROWN", "COLOR"), ("GRAY", "COLOR"), ("GOLD", "COLOR"),
    ("BLUE", "COLOR"), ("WHITE", "COLOR"), ("BLACK", "COLOR"),
    
    # More obvious connections people might try
    ("SUN", "LIGHT"), ("SUN", "HOT"), ("SUN", "YELLOW"),
    ("MOON", "NIGHT"), ("MOON", "STAR"), ("MOON", "LIGHT"),
    ("WATER", "OCEAN"), ("WATER", "BLUE"), ("WATER", "WET"),
    ("FIRE", "HOT"), ("FIRE", "LIGHT"), ("FIRE", "ORANGE"),
    ("TREE", "GREEN"), ("TREE", "WOOD"), ("WOOD", "FIRE"), ("WOOD", "BARK"),
    ("BIRD", "SING"), ("BIRD", "SKY"), ("BIRD", "FEATHER"),
    ("DOG", "ANIMAL"), ("CAT", "ANIMAL"), ("FISH", "ANIMAL"),
    ("ANIMAL", "NATURE"), ("NATURE", "TREE"), ("NATURE", "OCEAN"),
    ("FOOD", "EAT"), ("EAT", "BREAKFAST"), ("EAT", "HUNGRY"),
    ("HUNGRY", "FOOD"), ("FOOD", "PIZZA"), ("FOOD", "FRUIT"),
    ("HAPPY", "SMILE"), ("SAD", "FROWN"), ("FROWN", "FACE"),
    ("DANCE", "MUSIC"), ("DANCE", "PARTY"), ("SING", "MUSIC"),
    ("RUN", "FAST"), ("WALK", "SLOW"), ("RUN", "RACE"),
    ("WORK", "JOB"), ("JOB", "MONEY"), ("MONEY", "GOLD"),
    ("MONEY", "BANK"), ("BANK", "RIVER"), ("RIVER", "WATER"),
    ("CLOUD", "WHITE"), ("CLOUD", "RAIN"), ("RAIN", "WET"),
    ("WET", "WATER"), ("DRY", "DESERT"), ("HOT", "COLD"),
    
    # Entertainment & Media
    ("MOVIE", "FILM"), ("FILM", "CAMERA"), ("CAMERA", "PHOTO"),
    ("PHOTO", "PICTURE"), ("PICTURE", "ART"), ("TV", "SCREEN"),
    ("TV", "WATCH"), ("WATCH", "TIME"), ("WATCH", "SEE"),
    ("BOOK", "STORY"), ("STORY", "TALE"), ("TALE", "FAIRY"),
    ("FAIRY", "MAGIC"), ("MAGIC", "WIZARD"), ("WIZARD", "HARRY"),
    ("HARRY", "POTTER"), ("POTTER", "CLAY"), ("CLAY", "EARTH"),
    ("GAME", "VIDEO"), ("VIDEO", "YOUTUBE"), ("YOUTUBE", "INTERNET"),
    ("INTERNET", "WEB"), ("WEB", "SPIDER"), ("SPIDER", "INSECT"),
    ("NETFLIX", "MOVIE"), ("NETFLIX", "STREAM"), ("STREAM", "RIVER"),
    
    # Sports expanded
    ("SOCCER", "BALL"), ("SOCCER", "GOAL"), ("GOAL", "SCORE"),
    ("SCORE", "POINT"), ("POINT", "TIP"), ("TIP", "TOP"),
    ("BASKETBALL", "BALL"), ("BASKETBALL", "HOOP"), ("HOOP", "RING"),
    ("TENNIS", "BALL"), ("TENNIS", "RACKET"), ("RACKET", "NOISE"),
    ("GOLF", "BALL"), ("GOLF", "GREEN"), ("GOLF", "CLUB"),
    ("CLUB", "DANCE"), ("CLUB", "GROUP"), ("GROUP", "TEAM"),
    ("TEAM", "GAME"), ("TEAM", "PLAYER"), ("PLAYER", "GAME"),
    ("GYM", "EXERCISE"), ("EXERCISE", "HEALTH"), ("HEALTH", "DOCTOR"),
    ("DOCTOR", "HOSPITAL"), ("HOSPITAL", "SICK"), ("SICK", "ILL"),
    ("YOGA", "EXERCISE"), ("YOGA", "STRETCH"), ("STRETCH", "LONG"),
    
    # Food expanded
    ("BURGER", "FOOD"), ("BURGER", "MEAT"), ("MEAT", "COW"),
    ("CHICKEN", "BIRD"), ("CHICKEN", "FOOD"), ("CHICKEN", "EGG"),
    ("RICE", "FOOD"), ("RICE", "ASIA"), ("ASIA", "CHINA"),
    ("CHINA", "COUNTRY"), ("CHINA", "PLATE"), ("PLATE", "FOOD"),
    ("PASTA", "ITALY"), ("PASTA", "FOOD"), ("SUSHI", "JAPAN"),
    ("JAPAN", "ASIA"), ("JAPAN", "COUNTRY"), ("SUSHI", "FISH"),
    ("BREAD", "FOOD"), ("BREAD", "TOAST"), ("TOAST", "BREAKFAST"),
    ("CAKE", "BIRTHDAY"), ("BIRTHDAY", "PARTY"), ("CAKE", "SWEET"),
    ("ICE CREAM", "COLD"), ("ICE CREAM", "SWEET"), ("CHOCOLATE", "SWEET"),
    ("CHOCOLATE", "BROWN"), ("CHOCOLATE", "CANDY"), ("COOKIE", "SWEET"),
    ("COOKIE", "BAKE"), ("BAKE", "OVEN"), ("OVEN", "KITCHEN"),
    ("SALT", "TASTE"), ("TASTE", "TONGUE"), ("TONGUE", "MOUTH"),
    ("MOUTH", "FACE"), ("PEPPER", "SPICE"), ("SPICE", "HOT"),
    ("VEGETABLE", "FOOD"), ("VEGETABLE", "GREEN"), ("VEGETABLE", "PLANT"),
    ("SALAD", "VEGETABLE"), ("SALAD", "HEALTHY"), ("HEALTHY", "HEALTH"),
    
    # Animals expanded
    ("LION", "ANIMAL"), ("LION", "KING"), ("LION", "AFRICA"),
    ("AFRICA", "CONTINENT"), ("CONTINENT", "EARTH"), ("EARTH", "PLANET"),
    ("TIGER", "ANIMAL"), ("TIGER", "STRIPE"), ("STRIPE", "LINE"),
    ("BEAR", "ANIMAL"), ("BEAR", "FOREST"), ("FOREST", "TREE"),
    ("WOLF", "ANIMAL"), ("WOLF", "HOWL"), ("HOWL", "MOON"),
    ("SNAKE", "ANIMAL"), ("SNAKE", "SLITHER"), ("SLITHER", "SLIDE"),
    ("FROG", "ANIMAL"), ("FROG", "JUMP"), ("JUMP", "HIGH"),
    ("HORSE", "ANIMAL"), ("HORSE", "RIDE"), ("RIDE", "CAR"),
    ("HORSE", "RACE"), ("RABBIT", "ANIMAL"), ("RABBIT", "HOP"),
    ("HOP", "JUMP"), ("DEER", "ANIMAL"), ("DEER", "FOREST"),
    ("SHARK", "FISH"), ("SHARK", "OCEAN"), ("SHARK", "TEETH"),
    ("TEETH", "MOUTH"), ("WHALE", "OCEAN"), ("WHALE", "BIG"),
    ("BIG", "LARGE"), ("LARGE", "HUGE"), ("DOLPHIN", "OCEAN"),
    ("DOLPHIN", "SMART"), ("OWL", "BIRD"), ("OWL", "NIGHT"),
    ("EAGLE", "BIRD"), ("EAGLE", "FLY"), ("PENGUIN", "BIRD"),
    ("PENGUIN", "ICE"), ("PENGUIN", "COLD"), ("PARROT", "BIRD"),
    ("PARROT", "TALK"), ("TALK", "SPEAK"), ("SPEAK", "VOICE"),
    ("BUTTERFLY", "INSECT"), ("BUTTERFLY", "FLY"), ("BUTTERFLY", "COLOR"),
    
    # Places & Geography
    ("CITY", "TOWN"), ("TOWN", "SMALL"), ("CITY", "BIG"),
    ("CITY", "BUILDING"), ("BUILDING", "TALL"), ("BUILDING", "HOUSE"),
    ("PARK", "TREE"), ("PARK", "GRASS"), ("PARK", "PLAY"),
    ("BEACH", "OCEAN"), ("BEACH", "SUN"), ("BEACH", "VACATION"),
    ("VACATION", "TRAVEL"), ("TRAVEL", "TRIP"), ("TRIP", "JOURNEY"),
    ("JOURNEY", "ADVENTURE"), ("ADVENTURE", "FUN"), ("ADVENTURE", "EXPLORE"),
    ("EXPLORE", "DISCOVER"), ("DISCOVER", "FIND"), ("FIND", "SEARCH"),
    ("SEARCH", "GOOGLE"), ("GOOGLE", "INTERNET"), ("GOOGLE", "SEARCH"),
    ("ISLAND", "OCEAN"), ("ISLAND", "BEACH"), ("ISLAND", "TROPICAL"),
    ("TROPICAL", "HOT"), ("TROPICAL", "PALM"), ("PALM", "TREE"),
    ("JUNGLE", "FOREST"), ("JUNGLE", "TROPICAL"), ("JUNGLE", "ANIMAL"),
    ("CAVE", "DARK"), ("CAVE", "BAT"), ("BAT", "NIGHT"),
    ("BAT", "FLY"), ("VOLCANO", "FIRE"), ("VOLCANO", "MOUNTAIN"),
    ("VOLCANO", "LAVA"), ("LAVA", "HOT"), ("LAVA", "RED"),
    
    # Weather expanded
    ("STORM", "RAIN"), ("STORM", "WIND"), ("STORM", "THUNDER"),
    ("THUNDER", "LOUD"), ("THUNDER", "LIGHTNING"), ("LIGHTNING", "FAST"),
    ("LIGHTNING", "ELECTRIC"), ("ELECTRIC", "POWER"), ("POWER", "STRONG"),
    ("STRONG", "MUSCLE"), ("MUSCLE", "BODY"), ("BODY", "HUMAN"),
    ("HUMAN", "PERSON"), ("PERSON", "PEOPLE"), ("PEOPLE", "CROWD"),
    ("CROWD", "MANY"), ("MANY", "FEW"), ("FOG", "CLOUD"),
    ("FOG", "GRAY"), ("SUNNY", "SUN"), ("SUNNY", "BRIGHT"),
    ("BRIGHT", "LIGHT"), ("WINDY", "WIND"), ("RAINY", "RAIN"),
    ("SNOWY", "SNOW"), ("CLOUDY", "CLOUD"), ("WEATHER", "RAIN"),
    ("WEATHER", "SUN"), ("WEATHER", "CLOUD"), ("CLIMATE", "WEATHER"),
    
    # Technology expanded
    ("LAPTOP", "COMPUTER"), ("LAPTOP", "WORK"), ("DESKTOP", "COMPUTER"),
    ("TABLET", "SCREEN"), ("TABLET", "TOUCH"), ("TOUCH", "FEEL"),
    ("FEEL", "EMOTION"), ("EMOTION", "HAPPY"), ("EMOTION", "SAD"),
    ("ROBOT", "MACHINE"), ("MACHINE", "ENGINE"), ("ENGINE", "CAR"),
    ("AI", "ROBOT"), ("AI", "SMART"), ("AI", "COMPUTER"),
    ("APP", "PHONE"), ("APP", "DOWNLOAD"), ("DOWNLOAD", "INTERNET"),
    ("EMAIL", "SEND"), ("SEND", "MAIL"), ("MAIL", "LETTER"),
    ("LETTER", "WRITE"), ("LETTER", "ALPHABET"), ("ALPHABET", "ABC"),
    ("TEXT", "MESSAGE"), ("MESSAGE", "SEND"), ("TEXT", "WRITE"),
    ("WIFI", "INTERNET"), ("WIFI", "CONNECT"), ("CONNECT", "LINK"),
    ("LINK", "CHAIN"), ("BATTERY", "POWER"), ("BATTERY", "CHARGE"),
    ("CHARGE", "ELECTRIC"), ("PRINTER", "PAPER"), ("PRINTER", "INK"),
    
    # Music expanded
    ("GUITAR", "MUSIC"), ("PIANO", "MUSIC"), ("DRUM", "BEAT"),
    ("VIOLIN", "STRING"), ("VIOLIN", "MUSIC"), ("FLUTE", "MUSIC"),
    ("FLUTE", "BLOW"), ("TRUMPET", "MUSIC"), ("TRUMPET", "LOUD"),
    ("BAND", "MUSIC"), ("BAND", "GROUP"), ("CONCERT", "MUSIC"),
    ("CONCERT", "LIVE"), ("LIVE", "ALIVE"), ("ALIVE", "LIFE"),
    ("LIFE", "LIVE"), ("LIFE", "DEATH"), ("DEATH", "END"),
    ("END", "START"), ("START", "BEGIN"), ("BEGIN", "NEW"),
    ("NEW", "OLD"), ("OLD", "ANCIENT"), ("SINGER", "SING"),
    ("SINGER", "VOICE"), ("RAPPER", "MUSIC"), ("RAP", "MUSIC"),
    ("HIP HOP", "MUSIC"), ("JAZZ", "MUSIC"), ("CLASSICAL", "MUSIC"),
    ("ROCK", "MUSIC"), ("POP", "MUSIC"), ("POP", "POPULAR"),
    ("POPULAR", "FAMOUS"), ("FAMOUS", "STAR"), ("CELEBRITY", "FAMOUS"),
    
    # Emotions & States
    ("ANGRY", "EMOTION"), ("ANGRY", "RED"), ("ANGRY", "MAD"),
    ("MAD", "CRAZY"), ("CRAZY", "WILD"), ("WILD", "ANIMAL"),
    ("WILD", "FREE"), ("FREE", "FREEDOM"), ("FREEDOM", "LIBERTY"),
    ("SCARED", "FEAR"), ("SCARED", "AFRAID"), ("AFRAID", "FEAR"),
    ("NERVOUS", "SCARED"), ("NERVOUS", "SHAKE"), ("SHAKE", "MOVE"),
    ("MOVE", "WALK"), ("MOVE", "DANCE"), ("EXCITED", "HAPPY"),
    ("EXCITED", "ENERGY"), ("ENERGY", "POWER"), ("TIRED", "SLEEP"),
    ("TIRED", "EXHAUSTED"), ("EXHAUSTED", "TIRED"), ("BORED", "BORING"),
    ("BORING", "DULL"), ("DULL", "SHARP"), ("SHARP", "KNIFE"),
    ("KNIFE", "CUT"), ("CUT", "BLOOD"), ("BLOOD", "RED"),
    ("BLOOD", "BODY"), ("LOVE", "HEART"), ("HATE", "ANGRY"),
    ("HATE", "DISLIKE"), ("LIKE", "LOVE"), ("LIKE", "ENJOY"),
    ("ENJOY", "FUN"), ("SURPRISE", "SHOCK"), ("SHOCK", "ELECTRIC"),
    
    # School & Education
    ("MATH", "NUMBER"), ("NUMBER", "COUNT"), ("COUNT", "MANY"),
    ("SCIENCE", "EXPERIMENT"), ("EXPERIMENT", "TEST"), ("SCIENCE", "LAB"),
    ("LAB", "SCIENTIST"), ("SCIENTIST", "SMART"), ("HISTORY", "PAST"),
    ("PAST", "OLD"), ("PAST", "TIME"), ("FUTURE", "TIME"),
    ("FUTURE", "TOMORROW"), ("TOMORROW", "DAY"), ("DAY", "NIGHT"),
    ("ENGLISH", "LANGUAGE"), ("LANGUAGE", "SPEAK"), ("LANGUAGE", "WORD"),
    ("WORD", "LETTER"), ("WORD", "SPEAK"), ("HOMEWORK", "SCHOOL"),
    ("HOMEWORK", "STUDY"), ("GRADE", "SCHOOL"), ("GRADE", "SCORE"),
    ("UNIVERSITY", "SCHOOL"), ("UNIVERSITY", "COLLEGE"), ("COLLEGE", "STUDENT"),
    ("PROFESSOR", "TEACHER"), ("PROFESSOR", "UNIVERSITY"), ("DEGREE", "GRADUATE"),
    ("GRADUATE", "SCHOOL"), ("GRADUATE", "FINISH"), ("FINISH", "END"),
    
    # Space & Universe
    ("PLANET", "SPACE"), ("PLANET", "EARTH"), ("MARS", "PLANET"),
    ("MARS", "RED"), ("VENUS", "PLANET"), ("JUPITER", "PLANET"),
    ("SATURN", "PLANET"), ("SATURN", "RING"), ("GALAXY", "SPACE"),
    ("GALAXY", "STAR"), ("UNIVERSE", "SPACE"), ("UNIVERSE", "BIG"),
    ("ASTRONAUT", "SPACE"), ("ASTRONAUT", "ROCKET"), ("NASA", "SPACE"),
    ("NASA", "ROCKET"), ("ALIEN", "SPACE"), ("ALIEN", "UFO"),
    ("UFO", "FLY"), ("UFO", "SKY"), ("METEOR", "SPACE"),
    ("METEOR", "ROCK"), ("ASTEROID", "SPACE"), ("ASTEROID", "ROCK"),
    ("ORBIT", "SPACE"), ("ORBIT", "CIRCLE"), ("CIRCLE", "ROUND"),
    ("ROUND", "BALL"), ("GRAVITY", "FALL"), ("GRAVITY", "EARTH"),
    
    # Household & Daily Life
    ("CHAIR", "SIT"), ("SIT", "DOWN"), ("DOWN", "UP"),
    ("UP", "HIGH"), ("TABLE", "EAT"), ("TABLE", "WOOD"),
    ("SOFA", "SIT"), ("SOFA", "COMFORTABLE"), ("COMFORTABLE", "SOFT"),
    ("SOFT", "HARD"), ("HARD", "DIFFICULT"), ("DIFFICULT", "EASY"),
    ("EASY", "SIMPLE"), ("SIMPLE", "COMPLEX"), ("LAMP", "LIGHT"),
    ("LAMP", "ELECTRIC"), ("CURTAIN", "WINDOW"), ("CURTAIN", "FABRIC"),
    ("FABRIC", "CLOTH"), ("CLOTH", "CLOTHES"), ("CLOTHES", "WEAR"),
    ("WEAR", "DRESS"), ("DRESS", "CLOTHES"), ("SHIRT", "CLOTHES"),
    ("PANTS", "CLOTHES"), ("SHOES", "FEET"), ("FEET", "WALK"),
    ("SOCKS", "FEET"), ("HAT", "HEAD"), ("JACKET", "COLD"),
    ("JACKET", "CLOTHES"), ("BLANKET", "WARM"), ("BLANKET", "BED"),
    ("PILLOW", "BED"), ("PILLOW", "SOFT"), ("TOWEL", "DRY"),
    ("TOWEL", "BATHROOM"), ("BATHROOM", "SHOWER"), ("SHOWER", "WATER"),
    ("SOAP", "CLEAN"), ("CLEAN", "DIRTY"), ("DIRTY", "MUD"),
    ("MUD", "RAIN"), ("MUD", "BROWN"), ("TOOTHBRUSH", "TEETH"),
    ("TOOTHBRUSH", "CLEAN"), ("SHAMPOO", "HAIR"), ("HAIR", "HEAD"),
    
    # Numbers & Math concepts
    ("ONE", "NUMBER"), ("TWO", "NUMBER"), ("THREE", "NUMBER"),
    ("ZERO", "NUMBER"), ("ZERO", "NOTHING"), ("NOTHING", "EMPTY"),
    ("EMPTY", "FULL"), ("FULL", "COMPLETE"), ("COMPLETE", "FINISH"),
    ("HALF", "PART"), ("PART", "WHOLE"), ("WHOLE", "COMPLETE"),
    ("ADD", "MATH"), ("ADD", "PLUS"), ("PLUS", "MORE"),
    ("MORE", "LESS"), ("LESS", "FEW"), ("SUBTRACT", "MINUS"),
    ("MINUS", "LESS"), ("MULTIPLY", "MATH"), ("DIVIDE", "MATH"),
    ("DIVIDE", "SPLIT"), ("SPLIT", "BREAK"), ("BREAK", "FIX"),
    ("FIX", "REPAIR"), ("REPAIR", "BROKEN"), ("BROKEN", "BREAK"),
    
    # Verbs & Actions
    ("THROW", "BALL"), ("THROW", "CATCH"), ("CATCH", "GRAB"),
    ("GRAB", "HOLD"), ("HOLD", "HAND"), ("HAND", "FINGER"),
    ("FINGER", "POINT"), ("PUSH", "PULL"), ("PULL", "DRAG"),
    ("DRAG", "MOVE"), ("LIFT", "HEAVY"), ("LIFT", "UP"),
    ("DROP", "FALL"), ("DROP", "DOWN"), ("CLIMB", "UP"),
    ("SLIDE", "DOWN"), ("SLIDE", "PLAYGROUND"), ("PLAYGROUND", "PLAY"),
    ("SWING", "PLAYGROUND"), ("SWING", "BACK"), ("BACK", "FRONT"),
    ("FRONT", "FACE"), ("OPEN", "CLOSE"), ("CLOSE", "NEAR"),
    ("NEAR", "FAR"), ("FAR", "DISTANCE"), ("DISTANCE", "LONG"),
    ("LONG", "SHORT"), ("SHORT", "TALL"), ("BUILD", "CREATE"),
    ("CREATE", "MAKE"), ("MAKE", "BUILD"), ("DESTROY", "BREAK"),
    
    # Nature expanded
    ("FLOWER", "ROSE"), ("ROSE", "RED"), ("ROSE", "LOVE"),
    ("TULIP", "FLOWER"), ("DAISY", "FLOWER"), ("SUNFLOWER", "SUN"),
    ("SUNFLOWER", "YELLOW"), ("SUNFLOWER", "FLOWER"), ("GARDEN", "FLOWER"),
    ("GARDEN", "PLANT"), ("SEED", "PLANT"), ("SEED", "GROW"),
    ("ROOT", "TREE"), ("ROOT", "GROUND"), ("GROUND", "EARTH"),
    ("GROUND", "FLOOR"), ("FLOOR", "WALK"), ("CEILING", "ROOF"),
    ("CEILING", "UP"), ("WALL", "HOUSE"), ("WALL", "BRICK"),
    ("BRICK", "RED"), ("BRICK", "BUILD"), ("STONE", "HARD"),
    ("STONE", "GRAY"), ("PEBBLE", "SMALL"), ("PEBBLE", "STONE"),
    ("BOULDER", "BIG"), ("BOULDER", "ROCK"), ("CLIFF", "HIGH"),
    ("CLIFF", "ROCK"), ("WATERFALL", "WATER"), ("WATERFALL", "FALL"),
    ("LAKE", "WATER"), ("LAKE", "FISH"), ("POND", "WATER"),
    ("POND", "SMALL"), ("STREAM", "WATER"), ("CREEK", "WATER"),
]


def init_database():
    """Initialize database with schema and word data."""
    print("Initializing Six Degrees database...")
    
    db = Database("data/sixdegrees.db")
    db.init_schema()
    
    graph = WordGraph(db)
    
    # Collect all unique words
    words = set()
    for word1, word2 in WORD_ASSOCIATIONS:
        words.add(word1)
        words.add(word2)
    
    print(f"Adding {len(words)} words...")
    for word in words:
        graph.add_word(word)
    
    print(f"Adding {len(WORD_ASSOCIATIONS)} connections...")
    for word1, word2 in WORD_ASSOCIATIONS:
        graph.add_connection(word1, word2)
    
    print("Database initialized successfully!")
    print(f"  Words: {graph.word_count()}")
    print(f"  Connections: {graph.connection_count()}")


if __name__ == "__main__":
    init_database()

