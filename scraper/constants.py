from dataclasses import dataclass

@dataclass
class CategoryConfig:
    name: str
    filter: int = 0

# Game Action	GAME_ACTION
# Game Adventure	GAME_ADVENTURE
# Game Arcade	GAME_ARCADE
# Game Board	GAME_BOARD
# Game Card	GAME_CARD
# Game Casino	GAME_CASINO
# Game Casual	GAME_CASUAL
# Game Educational	GAME_EDUCATIONAL
# Game Music	GAME_MUSIC
# Game Puzzle	GAME_PUZZLE
# Game Racing	GAME_RACING
# Game Role Playing	GAME_ROLE_PLAYING
# Game Simulation	GAME_SIMULATION
# Game Sports	GAME_SPORTS
# Game Strategy	GAME_STRATEGY
# Game Trivia	GAME_TRIVIA
# Game Word	GAME_WORD

category_list = [
    CategoryConfig(name='BEAUTY', filter=0),
    CategoryConfig(name='DATING', filter=0),
    CategoryConfig(name='EDUCATION', filter=20),
    CategoryConfig(name='HEALTH_AND_FITNESS', filter=20),
    CategoryConfig(name='LIFESTYLE', filter=20),
    CategoryConfig(name='PARENTING', filter=20),
    CategoryConfig(name='PRODUCTIVITY', filter=20),
    CategoryConfig(name='SHOPPING', filter=20),
    CategoryConfig(name='SOCIAL', filter=20),
    CategoryConfig(name='BOOKS_AND_REFERENCE', filter=20),
    CategoryConfig(name='EVENTS', filter=0),
    CategoryConfig(name='FOOD_AND_DRINK', filter=20),
]


