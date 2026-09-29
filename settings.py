from pathlib import Path


# =========================================================
# CAMINHOS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"


# =========================================================
# JANELA
# =========================================================

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 680

FPS = 60

TITLE = "SHIP WAR"


# =========================================================
# ÁREA DO GAMEPLAY
# =========================================================

BOTTOM_PANEL_HEIGHT = 100

PLAY_AREA_BOTTOM = (
    SCREEN_HEIGHT
    - BOTTOM_PANEL_HEIGHT
)


# =========================================================
# PLAYER
# =========================================================

PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64

PLAYER_SHOT_DAMAGE = 1
PLAYER_SHOT_SPEED = 800

PLAYER_FIRE_COOLDOWN = 0.20
PLAYER_INVULNERABILITY = 0.8


# =========================================================
# ENEMY
# =========================================================

ENEMY_HIT_FLASH_TIME = 0.10


# =========================================================
# LEVEL
# =========================================================

LEVEL_INTRO_DURATION = 2.0

DEFAULT_LEVEL_DURATION = 30


# =========================================================
# BACKGROUNDS
# =========================================================

# Velocidade padrão do loop contínuo.
BACKGROUND_SPEED = 100

# No modo slow_scroll a imagem é carregada
# maior que a tela para permitir movimento
# sem precisar repetir a imagem.
SLOW_BACKGROUND_EXTRA_HEIGHT = 180


# =========================================================
# NAVIGATION CORE
# =========================================================

NAV_CORE_MESSAGE_TIME = 2.0


# =========================================================
# BOSS
# =========================================================

BOSS_THREAT_TIME = 2.5


# =========================================================
# EXPLOSÃO
# =========================================================

EXPLOSION_SIZE = 72
EXPLOSION_FRAME_TIME = 0.09


# =========================================================
# IMPACTO
# =========================================================

HIT_SPARK_LIFETIME = 0.14


# =========================================================
# SCREEN SHAKE
# =========================================================

SHAKE_PLAYER_HIT = 5
SHAKE_EXPLOSION = 3