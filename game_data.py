from settings import DEFAULT_LEVEL_DURATION


# =========================================================
# CAMPANHA
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
# MAPA DO SISTEMA SOLAR
# =========================================================
#
# As coordenadas são posições na tela do mapa.
#
# O sprite é opcional.
# Se não existir, aparece um círculo.
#
# =========================================================

MAP_LOCATIONS = {

    1: {
        "name": "EARTH",
        "sprite": "location_earth.png",
        "position": (75, 545)
    },

    2: {
        "name": "UPPER ATMOSPHERE",
        "sprite": "location_atmosphere.png",
        "position": (120, 490)
    },

    3: {
        "name": "MOON",
        "sprite": "location_moon.png",
        "position": (175, 430)
    },

    4: {
        "name": "LUNAR ORBIT",
        "sprite": "location_lunar_orbit.png",
        "position": (235, 370)
    },

    5: {
        "name": "MARS",
        "sprite": "location_mars.png",
        "position": (305, 320)
    },

    6: {
        "name": "ASTEROID BELT",
        "sprite": "location_belt.png",
        "position": (370, 270)
    },

    7: {
        "name": "JUPITER",
        "sprite": "location_jupiter.png",
        "position": (435, 225)
    },

    8: {
        "name": "SATURN",
        "sprite": "location_saturn.png",
        "position": (505, 180)
    },

    9: {
        "name": "OUTER SYSTEM",
        "sprite": "location_outer_system.png",
        "position": (575, 130)
    },

    10: {
        "name": "DEEP SPACE STATION",
        "sprite": "location_station.png",
        "position": (650, 80)
    },


    # =====================================================
    # FASES SECRETAS
    # =====================================================

    11: {
        "name": "VENUS",
        "sprite": "location_venus.png",
        "position": (310, 455)
    },

    12: {
        "name": "URANUS",
        "sprite": "location_uranus.png",
        "position": (575, 250)
    },

    13: {
        "name": "NEPTUNE",
        "sprite": "location_neptune.png",
        "position": (625, 330)
    },

    14: {
        "name": "PLUTO",
        "sprite": "location_pluto.png",
        "position": (655, 420)
    }
}


# =========================================================
# TRAJETÓRIAS DO MAPA
# =========================================================

MAP_CONNECTIONS = [

    # Linha principal.
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 8),
    (8, 9),
    (9, 10),

    # Rotas secretas.
    (4, 11),       # Lunar Orbit -> Venus
    (8, 12),       # Saturn -> Uranus
    (12, 13),      # Uranus -> Neptune
    (13, 14)       # Neptune -> Pluto
]


# =========================================================
# NAVES
# =========================================================

SHIPS = {

    0: {
        "id": 0,
        "name": "CLASSIC SAUCER",
        "sprite": "player.png",
        "speed": 420,
        "base_hp": 3,
        "price": 0
    },

    1: {
        "id": 1,
        "name": "INTERCEPTOR",
        "sprite": "player_02.png",
        "speed": 370,
        "base_hp": 4,
        "price": 30000
    },

    2: {
        "id": 2,
        "name": "HEAVY SAUCER",
        "sprite": "player_03.png",
        "speed": 310,
        "base_hp": 6,
        "price": 65000
    }
}


# =========================================================
# INIMIGOS
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

        "reward": 110,

        "movement": "horizontal"
    }
}


# =========================================================
# BOSSES
# =========================================================
#
# IMPORTANTE:
# O boss só será criado se a fase ainda NÃO tiver sido
# completada.
#
# Replays da fase não terão boss.
#
# =========================================================

BOSS_TYPES = {

    # Futuramente:
    #
    # "lunar_commander": {
    #     "name": "LUNAR COMMANDER",
    #     "sprite": "boss_lunar.png",
    #     "width": 120,
    #     "height": 100,
    #     "hp": 25,
    #     "min_speed": 50,
    #     "max_speed": 80,
    #     "min_fire_time": 0.8,
    #     "max_fire_time": 1.4,
    #     "shot_speed": 320,
    #     "damage": 1,
    #     "reward": 3000,
    #     "movement": "horizontal",
    #     "threat":
    #         "YOU SHOULD HAVE STAYED ON EARTH."
    # }
}


# =========================================================
# ITENS DE ROTA
# =========================================================
#
# Cada item ocupa 1 bit no password.
#
# Ele pode futuramente ser comprado, encontrado,
# dado por NPC, etc.
#
# =========================================================

ROUTE_ITEM_BITS = {

    "venus_coordinates": 0,
    "uranus_coordinates": 1,
    "neptune_coordinates": 2,
    "pluto_coordinates": 3
}


ROUTE_ITEM_NAMES = {

    "venus_coordinates":
        "VENUS COORDINATE CHIP",

    "uranus_coordinates":
        "URANUS COORDINATE CHIP",

    "neptune_coordinates":
        "NEPTUNE COORDINATE CHIP",

    "pluto_coordinates":
        "PLUTO COORDINATE CHIP"
}


# =========================================================
# ROTAS SECRETAS
# =========================================================
#
# TAB dentro da fase correspondente.
#
# O item é consumido.
#
# =========================================================

SECRET_ROUTES = {

    4: {
        "target": 11,
        "item": "venus_coordinates",
        "message": "VENUS ROUTE DISCOVERED"
    },

    8: {
        "target": 12,
        "item": "uranus_coordinates",
        "message": "URANUS ROUTE DISCOVERED"
    },

    12: {
        "target": 13,
        "item": "neptune_coordinates",
        "message": "NEPTUNE ROUTE DISCOVERED"
    },

    13: {
        "target": 14,
        "item": "pluto_coordinates",
        "message": "PLUTO ROUTE DISCOVERED"
    }
}


# =========================================================
# DROPS
# =========================================================

COMMON_DROP_CHANCE = 0.20


COMMON_DROPS = [
    {
        "type": "credits",
        "weight": 70,
        "value": 100
    },

    {
        "type": "health",
        "weight": 30,
        "value": 1
    }
]


# Pequena chance do item de rota aparecer
# na região onde pode ser usado.
#
# Assim ele pode ser comprado OU encontrado.

ROUTE_DROP_BY_LEVEL = {

    4: {
        "item": "venus_coordinates",
        "chance": 0.04
    },

    8: {
        "item": "uranus_coordinates",
        "chance": 0.04
    },

    12: {
        "item": "neptune_coordinates",
        "chance": 0.04
    },

    13: {
        "item": "pluto_coordinates",
        "chance": 0.04
    }
}


# =========================================================
# MERCADORES
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
# ITENS DE MERCADO
# =========================================================

MARKET_ITEMS = {

    "hp_upgrade": {

        "id": "hp_upgrade",

        "name": "+1 HULL",

        "type": "hp_upgrade",

        "description":
            "Increase maximum hull integrity by 1.",

        "price": 8000,

        "max_hp": 8
    },


    "ship_1": {

        "id": "ship_1",

        "name": "INTERCEPTOR",

        "type": "ship",

        "description":
            "Balanced alien combat craft.",

        "price": SHIPS[1]["price"],

        "ship_id": 1
    },


    "ship_2": {

        "id": "ship_2",

        "name": "HEAVY SAUCER",

        "type": "ship",

        "description":
            "Heavy armor. Lower agility.",

        "price": SHIPS[2]["price"],

        "ship_id": 2
    },


    # =====================================================
    # CHIPS DE ROTA
    # =====================================================

    "route_venus": {

        "id": "route_venus",

        "name":
            "VENUS COORDINATE CHIP",

        "type": "route_item",

        "route_item":
            "venus_coordinates",

        "description":
            "Contains an unregistered route to Venus.",

        "price": 5500
    },


    "route_uranus": {

        "id": "route_uranus",

        "name":
            "URANUS COORDINATE CHIP",

        "type": "route_item",

        "route_item":
            "uranus_coordinates",

        "description":
            "A strange route beyond Saturn.",

        "price": 9000
    },


    "route_neptune": {

        "id": "route_neptune",

        "name":
            "NEPTUNE COORDINATE CHIP",

        "type": "route_item",

        "route_item":
            "neptune_coordinates",

        "description":
            "Coordinates buried in alien telemetry.",

        "price": 12000
    },


    "route_pluto": {

        "id": "route_pluto",

        "name":
            "PLUTO COORDINATE CHIP",

        "type": "route_item",

        "route_item":
            "pluto_coordinates",

        "description":
            "A route to the edge of the old system.",

        "price": 16000
    }
}


# =========================================================
# ITENS ESPECIAIS
# =========================================================
#
# Vamos preencher esta lista depois.
#
# Os mercados secretos já estão preparados para sortear
# até 3 itens daqui.
#
# =========================================================

SPECIAL_MARKET_POOL = []


# =========================================================
# TRADING POSTS
# =========================================================
#
# "location" indica onde ele aparece no mapa.
#
# Os mercados secretos têm 3 slots reservados
# para itens especiais.
#
# =========================================================

TRADING_POSTS = {

    "lunar_exchange": {

        "name":
            "TRANQUILITY EXCHANGE",

        "location": 4,

        "stock": [
            "hp_upgrade",
            "route_venus"
        ]
    },


    "ceres_market": {

        "name":
            "CERES SCRAP MARKET",

        "location": 6,

        "stock": [
            "hp_upgrade",
            "ship_1"
        ]
    },


    "ringward_bazaar": {

        "name":
            "RINGWARD BAZAAR",

        "location": 8,

        "stock": [
            "hp_upgrade",
            "ship_1",
            "route_uranus"
        ]
    },


    "outer_depot": {

        "name":
            "OUTER REACH DEPOT",

        "location": 9,

        "stock": [
            "hp_upgrade",
            "ship_1",
            "ship_2"
        ]
    },


    # =====================================================
    # SECRET MARKETS
    # =====================================================

    "venus_market": {

        "name":
            "VENUS CLOUD EXCHANGE",

        "location": 11,

        "stock": [],

        "special_slots": 3
    },


    "uranus_market": {

        "name":
            "URANUS BLUE MARKET",

        "location": 12,

        "stock": [
            "route_neptune"
        ],

        "special_slots": 3
    },


    "neptune_market": {

        "name":
            "NEPTUNE DEEP BAZAAR",

        "location": 13,

        "stock": [
            "route_pluto"
        ],

        "special_slots": 3
    },


    "pluto_market": {

        "name":
            "PLUTO LAST OUTPOST",

        "location": 14,

        "stock": [],

        "special_slots": 3
    }
}


# =========================================================
# LEVELS
# =========================================================

LEVELS = {

    1: {
        "number": 1,
        "name": "EARTH",

        "duration":
            DEFAULT_LEVEL_DURATION,

        "background":
            "background_01.png",

        "background_mode":
            "scroll",

        "background_speed": 100,

        "max_enemies": 3,

        "enemy_types": [
            "basic"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title":
            "ESCAPE",

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

        "duration":
            DEFAULT_LEVEL_DURATION,

        "background":
            "background_02.png",

        "background_mode":
            "scroll",

        "background_speed": 100,

        "max_enemies": 3,

        "enemy_types": [
            "basic"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title":
            "THE SECRET SKY",

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

        "duration":
            DEFAULT_LEVEL_DURATION,

        "background":
            "background_03.png",

        "background_mode":
            "scroll",

        "background_speed": 90,

        "max_enemies": 3,

        "enemy_types": [
            "basic"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": 1,

        "briefing_title":
            "A FAMILIAR SIGNAL",

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

        "duration":
            DEFAULT_LEVEL_DURATION,

        "background":
            "background_04.png",

        "background_mode":
            "slow_scroll",

        "background_speed": 4,

        "max_enemies": 3,

        "enemy_types": [
            "basic"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title":
            "THE OTHER HUMANITY",

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

        "duration":
            DEFAULT_LEVEL_DURATION,

        "background":
            "background_05.png",

        "background_mode":
            "scroll",

        "background_speed": 95,

        "max_enemies": 3,

        "enemy_types": [
            "basic"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title":
            "THE RED FRONTIER",

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

        "duration":
            DEFAULT_LEVEL_DURATION,

        "background":
            "background_06.png",

        "background_mode":
            "scroll",

        "background_speed": 80,

        "max_enemies": 3,

        "enemy_types": [
            "basic"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": 2,

        "briefing_title":
            "SECOND SIGNAL",

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

        "duration":
            DEFAULT_LEVEL_DURATION,

        "background":
            "background_07.png",

        "background_mode":
            "static",

        "background_speed": 0,

        "max_enemies": 3,

        "enemy_types": [
            "basic"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title":
            "THE GIANT",

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

        "duration":
            DEFAULT_LEVEL_DURATION,

        "background":
            "background_08.png",

        "background_mode":
            "static",

        "background_speed": 0,

        "max_enemies": 3,

        "enemy_types": [
            "basic"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title":
            "THE RINGS",

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

        "duration":
            DEFAULT_LEVEL_DURATION,

        "background":
            "background_09.png",

        "background_mode":
            "slow_scroll",

        "background_speed": 3,

        "max_enemies": 3,

        "enemy_types": [
            "basic"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title":
            "THE LAST SIGNAL",

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

        "duration":
            DEFAULT_LEVEL_DURATION,

        "background":
            "background_10.png",

        "background_mode":
            "static",

        "background_speed": 0,

        "max_enemies": 3,

        "enemy_types": [
            "basic"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": 3,

        "briefing_title":
            "THE WAY HOME",

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
    # VENUS
    # =====================================================

    11: {
        "number": 11,
        "name": "VENUS",

        "duration":
            DEFAULT_LEVEL_DURATION,

        "background":
            "background_venus.png",

        "background_mode":
            "scroll",

        "background_speed": 80,

        "max_enemies": 3,

        "enemy_types": [
            "basic"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title":
            "BENEATH THE CLOUDS",

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


    # =====================================================
    # URANUS
    # =====================================================

    12: {
        "number": 12,
        "name": "URANUS",

        "duration":
            DEFAULT_LEVEL_DURATION,

        "background":
            "background_uranus.png",

        "background_mode":
            "static",

        "background_speed": 0,

        "max_enemies": 3,

        "enemy_types": [
            "basic"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title":
            "THE BLUE SILENCE",

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


    # =====================================================
    # NEPTUNE
    # =====================================================

    13: {
        "number": 13,
        "name": "NEPTUNE",

        "duration":
            DEFAULT_LEVEL_DURATION,

        "background":
            "background_neptune.png",

        "background_mode":
            "static",

        "background_speed": 0,

        "max_enemies": 3,

        "enemy_types": [
            "basic"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title":
            "THE DEEP ROUTE",

        "briefing": [

            "The Uranian coordinates",
            "lead farther outward.",

            "",

            "An ancient relay still transmits",
            "near Neptune.",

            "",

            "Someone wants it forgotten."
        ]
    },


    # =====================================================
    # PLUTO
    # =====================================================

    14: {
        "number": 14,
        "name": "PLUTO",

        "duration":
            DEFAULT_LEVEL_DURATION,

        "background":
            "background_pluto.png",

        "background_mode":
            "slow_scroll",

        "background_speed": 2,

        "max_enemies": 3,

        "enemy_types": [
            "basic"
        ],

        "environment": None,
        "boss": None,

        "nav_core_piece": None,

        "briefing_title":
            "THE OLD EDGE",

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