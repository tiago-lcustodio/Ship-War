from settings import DEFAULT_LEVEL_DURATION


# =========================================================
# CAMPAIGN
# =========================================================

MAINLINE_LEVELS = [
    1, 2, 3, 4, 5,
    6, 7, 8, 9, 10
]

SECRET_LEVELS = [
    11, 12, 13, 14
]


NEXT_MAINLINE = {
    1: 2,
    2: 3,
    3: 4,
    4: 5,
    5: 6,
    6: 7,
    7: 8,
    8: 9,
    9: 10
}


# =========================================================
# MAP
# =========================================================

MAP_LOCATIONS = {

    1: {
        "name": "EARTH",
        "position": (75, 545),
        "sprite": None
    },

    2: {
        "name": "UPPER ATMOSPHERE",
        "position": (120, 490),
        "sprite": None
    },

    3: {
        "name": "MOON",
        "position": (175, 430),
        "sprite": None
    },

    4: {
        "name": "LUNAR ORBIT",
        "position": (235, 370),
        "sprite": None
    },

    5: {
        "name": "MARS",
        "position": (305, 320),
        "sprite": None
    },

    6: {
        "name": "ASTEROID BELT",
        "position": (370, 270),
        "sprite": None
    },

    7: {
        "name": "JUPITER",
        "position": (435, 225),
        "sprite": None
    },

    8: {
        "name": "SATURN",
        "position": (505, 180),
        "sprite": None
    },

    9: {
        "name": "OUTER SYSTEM",
        "position": (575, 130),
        "sprite": None
    },

    10: {
        "name": "DEEP SPACE STATION",
        "position": (650, 80),
        "sprite": None
    },

    11: {
        "name": "VENUS",
        "position": (310, 455),
        "sprite": None
    },

    12: {
        "name": "URANUS",
        "position": (575, 250),
        "sprite": None
    },

    13: {
        "name": "NEPTUNE",
        "position": (625, 330),
        "sprite": None
    },

    14: {
        "name": "PLUTO",
        "position": (655, 420),
        "sprite": None
    }
}


MAP_CONNECTIONS = [

    # Main route.
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 8),
    (8, 9),
    (9, 10),

    # Hidden routes.
    (4, 11),
    (8, 12),
    (12, 13),
    (13, 14)
]


# =========================================================
# SHIPS
# =========================================================

SHIPS = {

    0: {
        "id": 0,
        "name": "CLASSIC SAUCER",
        "sprite": "player.png",
        "speed": 420,
        "price": 0,

        # Primary weapon cooldown x 0.90.
        "primary_cooldown_modifier": 0.90,

        "secondary_cooldown_modifier": 1.00,
        "shield_recharge_modifier": 1.00
    },

    1: {
        "id": 1,
        "name": "INTERCEPTOR",
        "sprite": "player_02.png",
        "speed": 370,
        "price": 6500,

        "primary_cooldown_modifier": 1.00,

        # Secondary weapons recharge 15% faster.
        "secondary_cooldown_modifier": 0.85,

        "shield_recharge_modifier": 1.00
    },

    2: {
        "id": 2,
        "name": "HEAVY SAUCER",
        "sprite": "player_03.png",
        "speed": 310,
        "price": 10500,

        "primary_cooldown_modifier": 1.00,
        "secondary_cooldown_modifier": 1.00,

        # Shields recharge 25% faster.
        "shield_recharge_modifier": 0.75
    }
}


# =========================================================
# PRIMARY WEAPONS
# =========================================================
#
# max_hits:
#     1 = normal projectile
#     3 = can hit three different enemies
#
# =========================================================

PRIMARY_WEAPONS = {

    0: {
        "id": 0,
        "name": "PULSE CANNON I",

        "damage": 1,
        "cooldown": 0.20,
        "speed": 800,

        "pattern": "single",

        "max_hits": 1,

        "price": 0,

        "special": False
    },


    1: {
        "id": 1,
        "name": "PULSE CANNON II",

        "damage": 1,
        "cooldown": 0.143,
        "speed": 820,

        "pattern": "single",

        "max_hits": 1,

        "price": 2200,

        "special": False
    },


    2: {
        "id": 2,
        "name": "TWIN PULSE",

        "damage": 1,
        "cooldown": 0.22,
        "speed": 800,

        "pattern": "twin",

        "max_hits": 1,

        "price": 3800,

        "special": False
    },


    3: {
        "id": 3,
        "name": "HEAVY PULSE",

        "damage": 3,
        "cooldown": 0.40,
        "speed": 680,

        "pattern": "single",

        "max_hits": 1,

        "price": 4500,

        "special": False
    },


    4: {
        "id": 4,
        "name": "SPREAD PULSE",

        "damage": 1,
        "cooldown": 0.285,
        "speed": 760,

        "pattern": "spread",

        "max_hits": 1,

        "price": 5500,

        "special": False
    },


    # =====================================================
    # VENUS
    # =====================================================

    5: {
        "id": 5,
        "name": "PLASMA LANCE",

        "damage": 2,
        "cooldown": 0.32,
        "speed": 900,

        "pattern": "single",

        # Perfura até 3 inimigos.
        "max_hits": 3,

        "price": 6500,

        "special": True,

        "origin": "VENUS"
    },


    # =====================================================
    # PLUTO
    # =====================================================

    6: {
        "id": 6,
        "name": "ANCIENT GREY CANNON",

        "damage": 4,
        "cooldown": 0.16,
        "speed": 900,

        "pattern": "single",

        "max_hits": 1,

        # Após seis disparos entra em overheat.
        "overheat_after": 6,
        "overheat_time": 2.5,

        "price": 9000,

        "special": True,

        "origin": "PLUTO"
    }
}


# =========================================================
# SECONDARY WEAPONS
# =========================================================

SECONDARY_WEAPONS = {

    0: {
        "id": 0,
        "name": "NONE",
        "kind": "none",
        "price": 0
    },


    1: {
        "id": 1,
        "name": "MISSILE POD",

        "kind": "missile",

        "damage": 5,
        "cooldown": 3.0,
        "speed": 520,

        "price": 2800,

        "special": False
    },


    2: {
        "id": 2,
        "name": "PLASMA BOMB",

        "kind": "plasma_bomb",

        "damage": 3,
        "cooldown": 4.0,
        "speed": 430,

        "radius": 90,

        "price": 4200,

        "special": False
    },


    3: {
        "id": 3,
        "name": "EMP BURST",

        "kind": "emp",

        "damage": 1,
        "cooldown": 5.0,

        "radius": 150,
        "stun_time": 2.0,

        "price": 5000,

        "special": False
    },


    4: {
        "id": 4,
        "name": "DEFENSE BURST",

        "kind": "defense_burst",

        "cooldown": 7.0,

        "duration": 1.2,

        "price": 5500,

        "special": False
    },


    # =====================================================
    # NEPTUNE
    # =====================================================

    5: {
        "id": 5,
        "name": "CHAIN LIGHTNING",

        "kind": "chain_lightning",

        "damage": 3,
        "cooldown": 5.5,

        "targets": 3,
        "radius": 300,

        "price": 7000,

        "special": True,

        "origin": "NEPTUNE"
    }
}


# =========================================================
# DEFENSIVE MODULES
# =========================================================

DEFENSE_MODULES = {

    0: {
        "id": 0,
        "name": "NONE",
        "kind": "none",
        "price": 0
    },


    1: {
        "id": 1,
        "name": "SHIELD I",

        "kind": "shield",

        "capacity": 1,
        "recharge_time": 7.0,

        "price": 2500,

        "special": False
    },


    2: {
        "id": 2,
        "name": "SHIELD II",

        "kind": "shield",

        "capacity": 2,
        "recharge_time": 8.0,

        "price": 4800,

        "special": False
    },


    3: {
        "id": 3,
        "name": "REACTIVE ARMOR",

        "kind": "reactive",

        "cooldown": 12.0,

        "price": 5500,

        "special": False
    },


    4: {
        "id": 4,
        "name": "EMERGENCY REPAIR",

        "kind": "repair",

        "price": 6500,

        "special": False
    },


    # =====================================================
    # URANUS
    # =====================================================

    5: {
        "id": 5,
        "name": "PHASE SHIELD",

        "kind": "phase",

        # 30% de chance de ignorar completamente
        # qualquer impacto.
        "phase_chance": 0.30,

        "price": 7500,

        "special": True,

        "origin": "URANUS"
    }
}


# =========================================================
# HULL
# =========================================================

HULL_UPGRADE_PRICES = {

    3: 2000,
    4: 3200,
    5: 4800,
    6: 7000
}

MAX_PLAYER_HP = 7


# =========================================================
# ENEMIES
# =========================================================
#
# As artes ainda podem usar enemy_n1.png.
# Estamos separando comportamento/balanceamento da arte.
#
# =========================================================

ENEMY_TYPES = {

    "basic": {

        "name": "BASIC FIGHTER",
        "sprite": "enemy_n1.png",

        "width": 56,
        "height": 56,

        "hp": 3,

        "min_speed": 90,
        "max_speed": 140,

        "min_fire_time": 1.8,
        "max_fire_time": 3.2,

        "shot_speed": 280,

        "damage": 1,

        # Antes era 110.
        "reward": 11,

        "movement": "horizontal"
    },


    "fast": {

        "name": "FAST INTERCEPTOR",
        "sprite": "enemy_n1.png",

        "width": 50,
        "height": 50,

        "hp": 2,

        "min_speed": 160,
        "max_speed": 220,

        "min_fire_time": 1.5,
        "max_fire_time": 2.6,

        "shot_speed": 310,

        "damage": 1,

        "reward": 14,

        "movement": "zigzag"
    },


    "armored": {

        "name": "ARMORED FIGHTER",
        "sprite": "enemy_n1.png",

        "width": 62,
        "height": 62,

        "hp": 5,

        "min_speed": 65,
        "max_speed": 100,

        "min_fire_time": 1.6,
        "max_fire_time": 2.6,

        "shot_speed": 290,

        "damage": 1,

        "reward": 22,

        "movement": "horizontal"
    },


    "ace": {

        "name": "ACE FIGHTER",
        "sprite": "enemy_n1.png",

        "width": 54,
        "height": 54,

        "hp": 4,

        "min_speed": 130,
        "max_speed": 180,

        "min_fire_time": 1.2,
        "max_fire_time": 2.0,

        "shot_speed": 340,

        "damage": 1,

        "reward": 26,

        "movement": "zigzag"
    },


    "heavy": {

        "name": "HEAVY ATTACK SHIP",
        "sprite": "enemy_n1.png",

        "width": 68,
        "height": 68,

        "hp": 7,

        "min_speed": 55,
        "max_speed": 85,

        "min_fire_time": 1.3,
        "max_fire_time": 2.0,

        "shot_speed": 320,

        "damage": 2,

        "reward": 38,

        "movement": "horizontal"
    },


    "elite": {

        "name": "ELITE FIGHTER",
        "sprite": "enemy_n1.png",

        "width": 58,
        "height": 58,

        "hp": 9,

        "min_speed": 110,
        "max_speed": 160,

        "min_fire_time": 0.9,
        "max_fire_time": 1.6,

        "shot_speed": 370,

        "damage": 2,

        "reward": 55,

        "movement": "zigzag"
    }
}


BOSS_TYPES = {}


# =========================================================
# DROPS
# =========================================================

COMMON_DROP_CHANCE = 0.15

COMMON_DROPS = [

    {
        "type": "credits",
        "weight": 75,

        # Antes era 100.
        "value": 10
    },

    {
        "type": "health",
        "weight": 25,
        "value": 1
    }
]


# Chance adicional e independente.
#
# Aproximadamente 1,5% por inimigo após a Lua.
# É raro, mas um jogador que repete missões pode achar chips.

NAV_CHIP_DROP_CHANCE = 0.015


# =========================================================
# SECRET ROUTES
# =========================================================

SECRET_ROUTES = {

    4: {
        "target": 11,
        "message": "VENUS ROUTE DISCOVERED"
    },

    8: {
        "target": 12,
        "message": "URANUS ROUTE DISCOVERED"
    },

    12: {
        "target": 13,
        "message": "NEPTUNE ROUTE DISCOVERED"
    },

    13: {
        "target": 14,
        "message": "PLUTO ROUTE DISCOVERED"
    }
}


# =========================================================
# MERCHANTS
# =========================================================

MERCHANT_SPECIES = {

    "gray": {
        "name": "GRAY",
        "portrait_prefix": "merchant_gray"
    },

    "reptilian": {
        "name": "REPTILIAN",
        "portrait_prefix": "merchant_reptilian"
    },

    "mantid": {
        "name": "MANTID",
        "portrait_prefix": "merchant_mantid"
    }
}


MERCHANT_MOODS = {

    "happy": {
        "name": "HAPPY",
        "price_modifier": 0.80
    },

    "sad": {
        "name": "SAD",
        "price_modifier": 1.00
    },

    "angry": {
        "name": "ANGRY",
        "price_modifier": 1.20
    }
}


# =========================================================
# MARKET ITEMS
# =========================================================

MARKET_ITEMS = {

    "hull_upgrade": {
        "name": "HULL UPGRADE",
        "type": "hull"
    },


    "nav_chip": {
        "name": "FORBIDDEN NAV CHIP",
        "type": "nav_chip"
    },


    # PRIMARY ------------------------------------------------

    "primary_1": {
        "name": PRIMARY_WEAPONS[1]["name"],
        "type": "primary",
        "equipment_id": 1
    },

    "primary_2": {
        "name": PRIMARY_WEAPONS[2]["name"],
        "type": "primary",
        "equipment_id": 2
    },

    "primary_3": {
        "name": PRIMARY_WEAPONS[3]["name"],
        "type": "primary",
        "equipment_id": 3
    },

    "primary_4": {
        "name": PRIMARY_WEAPONS[4]["name"],
        "type": "primary",
        "equipment_id": 4
    },

    "primary_5": {
        "name": PRIMARY_WEAPONS[5]["name"],
        "type": "primary",
        "equipment_id": 5
    },

    "primary_6": {
        "name": PRIMARY_WEAPONS[6]["name"],
        "type": "primary",
        "equipment_id": 6
    },


    # SECONDARY ----------------------------------------------

    "secondary_1": {
        "name": SECONDARY_WEAPONS[1]["name"],
        "type": "secondary",
        "equipment_id": 1
    },

    "secondary_2": {
        "name": SECONDARY_WEAPONS[2]["name"],
        "type": "secondary",
        "equipment_id": 2
    },

    "secondary_3": {
        "name": SECONDARY_WEAPONS[3]["name"],
        "type": "secondary",
        "equipment_id": 3
    },

    "secondary_4": {
        "name": SECONDARY_WEAPONS[4]["name"],
        "type": "secondary",
        "equipment_id": 4
    },

    "secondary_5": {
        "name": SECONDARY_WEAPONS[5]["name"],
        "type": "secondary",
        "equipment_id": 5
    },


    # DEFENSE ------------------------------------------------

    "defense_1": {
        "name": DEFENSE_MODULES[1]["name"],
        "type": "defense",
        "equipment_id": 1
    },

    "defense_2": {
        "name": DEFENSE_MODULES[2]["name"],
        "type": "defense",
        "equipment_id": 2
    },

    "defense_3": {
        "name": DEFENSE_MODULES[3]["name"],
        "type": "defense",
        "equipment_id": 3
    },

    "defense_4": {
        "name": DEFENSE_MODULES[4]["name"],
        "type": "defense",
        "equipment_id": 4
    },

    "defense_5": {
        "name": DEFENSE_MODULES[5]["name"],
        "type": "defense",
        "equipment_id": 5
    },


    # SHIPS --------------------------------------------------

    "ship_1": {
        "name": SHIPS[1]["name"],
        "type": "ship",
        "equipment_id": 1
    },

    "ship_2": {
        "name": SHIPS[2]["name"],
        "type": "ship",
        "equipment_id": 2
    }
}


# =========================================================
# TRADING POSTS
# =========================================================

TRADING_POSTS = {

    "lunar_exchange": {

        "name": "TRANQUILITY EXCHANGE",

        "location": 4,

        "stock": [
            "hull_upgrade",
            "primary_1",
            "defense_1",
            "nav_chip"
        ],

        "nav_chip_price": 2500
    },


    "ceres_market": {

        "name": "CERES SCRAP MARKET",

        "location": 6,

        "stock": [
            "hull_upgrade",
            "primary_2",
            "secondary_1",
            "secondary_2",
            "ship_1",
            "nav_chip"
        ],

        "nav_chip_price": 3500
    },


    "ringward_bazaar": {

        "name": "RINGWARD BAZAAR",

        "location": 8,

        "stock": [
            "hull_upgrade",
            "primary_3",
            "secondary_3",
            "defense_2",
            "ship_1",
            "nav_chip"
        ],

        "nav_chip_price": 5000
    },


    "outer_depot": {

        "name": "OUTER REACH DEPOT",

        "location": 9,

        "stock": [
            "hull_upgrade",
            "primary_4",
            "secondary_4",
            "defense_3",
            "defense_4",
            "ship_2",
            "nav_chip"
        ],

        "nav_chip_price": 6500
    },


    # =====================================================
    # SECRET MARKETS
    # =====================================================

    "venus_market": {

        "name": "VENUS CLOUD EXCHANGE",

        "location": 11,

        # Só UM equipamento especial.
        "stock": [
            "primary_5",
            "hull_upgrade",
            "nav_chip"
        ],

        "nav_chip_price": 4500
    },


    "uranus_market": {

        "name": "URANUS BLUE MARKET",

        "location": 12,

        "stock": [
            "defense_5",
            "hull_upgrade",
            "nav_chip"
        ],

        "nav_chip_price": 5000
    },


    "neptune_market": {

        "name": "NEPTUNE DEEP BAZAAR",

        "location": 13,

        "stock": [
            "secondary_5",
            "hull_upgrade",
            "nav_chip"
        ],

        "nav_chip_price": 5500
    },


    "pluto_market": {

        "name": "PLUTO LAST OUTPOST",

        "location": 14,

        "stock": [
            "primary_6",
            "hull_upgrade"
        ]
    }
}


# =========================================================
# LEVELS
# =========================================================

LEVELS = {

    1: {
        "number": 1,
        "name": "EARTH",

        "duration": DEFAULT_LEVEL_DURATION,

        "background": "background_01.png",
        "background_mode": "scroll",
        "background_speed": 100,

        "max_enemies": 3,
        "enemy_types": ["basic"],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title": "ESCAPE",

        "briefing": [
            "Nihl has spent decades",
            "stranded on this world.",
            "",
            "His Navigation Core is broken.",
            "",
            "Now the humans have found him.",
            "It is time to leave."
        ]
    },


    2: {
        "number": 2,
        "name": "UPPER ATMOSPHERE",

        "duration": DEFAULT_LEVEL_DURATION,

        "background": "background_02.png",
        "background_mode": "scroll",
        "background_speed": 100,

        "max_enemies": 3,

        "enemy_types": [
            "basic",
            "fast"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title": "THE SECRET SKY",

        "briefing": [
            "These are not ordinary fighters.",
            "",
            "Humanity has been hiding",
            "more than Nihl expected.",
            "",
            "Keep climbing."
        ]
    },


    3: {
        "number": 3,
        "name": "THE MOON",

        "duration": DEFAULT_LEVEL_DURATION,

        "background": "background_03.png",
        "background_mode": "scroll",
        "background_speed": 90,

        "max_enemies": 3,

        "enemy_types": [
            "basic",
            "fast"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": 1,

        "briefing_title": "A FAMILIAR SIGNAL",

        "briefing": [
            "A Grey signal is coming",
            "from the lunar surface.",
            "",
            "It matches part of Nihl's",
            "damaged Navigation Core.",
            "",
            "Someone brought it here."
        ]
    },


    4: {
        "number": 4,
        "name": "LUNAR ORBIT",

        "duration": DEFAULT_LEVEL_DURATION,

        "background": "background_04.png",
        "background_mode": "slow_scroll",
        "background_speed": 4,

        "max_enemies": 3,

        "enemy_types": [
            "fast",
            "armored"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title": "THE OTHER HUMANITY",

        "briefing": [
            "Stations surround the Moon.",
            "",
            "Humanity reached space",
            "long before Earth was told.",
            "",
            "Nihl is no longer alone up here."
        ]
    },


    5: {
        "number": 5,
        "name": "MARS",

        "duration": DEFAULT_LEVEL_DURATION,

        "background": "background_05.png",
        "background_mode": "scroll",
        "background_speed": 95,

        "max_enemies": 4,

        "enemy_types": [
            "fast",
            "armored",
            "ace"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title": "THE RED FRONTIER",

        "briefing": [
            "Mars is no empty world.",
            "",
            "Humans, aliens and mercenaries",
            "trade beneath Earth's silence.",
            "",
            "Nihl needs a way through."
        ]
    },


    6: {
        "number": 6,
        "name": "ASTEROID BELT",

        "duration": DEFAULT_LEVEL_DURATION,

        "background": "background_06.png",
        "background_mode": "scroll",
        "background_speed": 80,

        "max_enemies": 4,

        "enemy_types": [
            "armored",
            "ace"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": 2,

        "briefing_title": "SECOND SIGNAL",

        "briefing": [
            "The Core speaks again.",
            "",
            "Its second fragment is somewhere",
            "inside pirate territory.",
            "",
            "Nothing out here is free."
        ]
    },


    7: {
        "number": 7,
        "name": "JUPITER",

        "duration": DEFAULT_LEVEL_DURATION,

        "background": "background_07.png",
        "background_mode": "static",
        "background_speed": 0,

        "max_enemies": 4,

        "enemy_types": [
            "armored",
            "heavy"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title": "THE GIANT",

        "briefing": [
            "The inner worlds are behind him.",
            "",
            "Jupiter blocks the route outward.",
            "",
            "Its storms have destroyed",
            "ships far larger than Nihl's."
        ]
    },


    8: {
        "number": 8,
        "name": "SATURN",

        "duration": DEFAULT_LEVEL_DURATION,

        "background": "background_08.png",
        "background_mode": "static",
        "background_speed": 0,

        "max_enemies": 4,

        "enemy_types": [
            "ace",
            "heavy"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title": "THE RINGS",

        "briefing": [
            "Saturn marks the edge",
            "of the crowded routes.",
            "",
            "Beyond the rings, old maps",
            "become unreliable.",
            "",
            "Nihl keeps going."
        ]
    },


    9: {
        "number": 9,
        "name": "OUTER SYSTEM",

        "duration": DEFAULT_LEVEL_DURATION,

        "background": "background_09.png",
        "background_mode": "slow_scroll",
        "background_speed": 3,

        "max_enemies": 4,

        "enemy_types": [
            "heavy",
            "elite"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title": "THE LAST SIGNAL",

        "briefing": [
            "The Sun is becoming distant.",
            "",
            "But the final Core fragment",
            "is finally clear.",
            "",
            "It is transmitting from a station",
            "at the edge of known traffic."
        ]
    },


    10: {
        "number": 10,
        "name": "DEEP SPACE STATION",

        "duration": DEFAULT_LEVEL_DURATION,

        "background": "background_10.png",
        "background_mode": "static",
        "background_speed": 0,

        "max_enemies": 4,

        "enemy_types": [
            "heavy",
            "elite"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": 3,

        "briefing_title": "THE WAY HOME",

        "briefing": [
            "The final fragment is here.",
            "",
            "Once the Core is restored,",
            "Nihl can leave this star.",
            "",
            "If that is still what he wants."
        ]
    },


    # =====================================================
    # SECRET LEVELS
    # =====================================================

    11: {
        "number": 11,
        "name": "VENUS",

        "duration": DEFAULT_LEVEL_DURATION,

        "background": "background_venus.png",
        "background_mode": "scroll",
        "background_speed": 80,

        "max_enemies": 4,

        "enemy_types": [
            "fast",
            "armored",
            "ace"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title": "BENEATH THE CLOUDS",

        "briefing": [
            "The illegal coordinates were real.",
            "",
            "Something is broadcasting",
            "from beneath Venusian clouds.",
            "",
            "Nihl has no reason to investigate.",
            "So naturally, he does."
        ]
    },


    12: {
        "number": 12,
        "name": "URANUS",

        "duration": DEFAULT_LEVEL_DURATION,

        "background": "background_uranus.png",
        "background_mode": "static",
        "background_speed": 0,

        "max_enemies": 4,

        "enemy_types": [
            "armored",
            "heavy"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title": "THE BLUE SILENCE",

        "briefing": [
            "Few ships travel this far.",
            "",
            "A lonely trading signal",
            "calls from the darkness.",
            "",
            "Maybe treasure.",
            "Maybe trouble."
        ]
    },


    13: {
        "number": 13,
        "name": "NEPTUNE",

        "duration": DEFAULT_LEVEL_DURATION,

        "background": "background_neptune.png",
        "background_mode": "static",
        "background_speed": 0,

        "max_enemies": 4,

        "enemy_types": [
            "heavy",
            "elite"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title": "THE DEEP ROUTE",

        "briefing": [
            "The Uranian route",
            "leads farther outward.",
            "",
            "An ancient relay still transmits",
            "near Neptune.",
            "",
            "Someone wants it forgotten."
        ]
    },


    14: {
        "number": 14,
        "name": "PLUTO",

        "duration": DEFAULT_LEVEL_DURATION,

        "background": "background_pluto.png",
        "background_mode": "slow_scroll",
        "background_speed": 2,

        "max_enemies": 4,

        "enemy_types": [
            "elite",
            "heavy"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title": "THE OLD EDGE",

        "briefing": [
            "Beyond Neptune lies an old route",
            "almost erased from every chart.",
            "",
            "There is nothing Nihl needs here.",
            "",
            "That has never stopped him before."
        ]
    }
}