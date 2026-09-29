from pathlib import Path


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"


# =========================================================
# WINDOW
# =========================================================

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 680

FPS = 60
TITLE = "SHIP WAR"


# =========================================================
# PLAY AREA
# =========================================================

BOTTOM_PANEL_HEIGHT = 100
PLAY_AREA_BOTTOM = (
    SCREEN_HEIGHT
    - BOTTOM_PANEL_HEIGHT
)


# =========================================================
# PLAYER
# =========================================================

# A largura é a referência.
# A altura agora é calculada automaticamente
# pela proporção original do PNG.
PLAYER_WIDTH = 82

# Mantido apenas por compatibilidade
# com algum arquivo antigo que ainda importe.
PLAYER_HEIGHT = 64

PLAYER_INVULNERABILITY = 0.8


# =========================================================
# LEVEL
# =========================================================

LEVEL_INTRO_DURATION = 2.0

DEFAULT_LEVEL_DURATION = 90


# =========================================================
# BACKGROUND
# =========================================================

BACKGROUND_SPEED = 100

SLOW_BACKGROUND_EXTRA_HEIGHT = 180


# =========================================================
# EFFECTS
# =========================================================

ENEMY_HIT_FLASH_TIME = 0.10

NAV_CORE_MESSAGE_TIME = 2.0
BOSS_THREAT_TIME = 2.5

EXPLOSION_SIZE = 72
EXPLOSION_FRAME_TIME = 0.09

HIT_SPARK_LIFETIME = 0.14


# =========================================================
# SHAKE
# =========================================================

SHAKE_PLAYER_HIT = 5
SHAKE_EXPLOSION = 3