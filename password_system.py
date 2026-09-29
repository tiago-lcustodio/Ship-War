import base64
import hashlib
import secrets
import struct

from dataclasses import dataclass


SECRET = b"SHIP_WAR_RETRO_2026_V3"


# =========================================================
# HELPERS
# =========================================================

def level_bit(
    level_number
):

    return (
        1
        << (
            level_number - 1
        )
    )


# =========================================================
# GAME PROGRESS
# =========================================================

@dataclass
class GameProgress:

    # Agora representa a localização atual no mapa.
    next_level: int = 1

    money: int = 0

    max_hp: int = 3

    continues: int = 0

    primary_weapon: int = 0

    flags: int = 0

    ship_id: int = 0

    nav_core_parts: int = 0

    # 14 bits possíveis.
    completed_mask: int = 0

    # Level 1 conhecido desde o início.
    discovered_mask: int = 1

    # 4 bits usados atualmente.
    route_items_mask: int = 0


    # =====================================================
    # LEVEL COMPLETION
    # =====================================================

    def is_completed(
        self,
        level_number
    ):

        return bool(
            self.completed_mask
            & level_bit(
                level_number
            )
        )


    def mark_completed(
        self,
        level_number
    ):

        self.completed_mask |= (
            level_bit(
                level_number
            )
        )


    # =====================================================
    # DISCOVERY
    # =====================================================

    def is_discovered(
        self,
        level_number
    ):

        return bool(
            self.discovered_mask
            & level_bit(
                level_number
            )
        )


    def discover(
        self,
        level_number
    ):

        self.discovered_mask |= (
            level_bit(
                level_number
            )
        )


    # =====================================================
    # ROUTE ITEMS
    # =====================================================

    def has_route_item_bit(
        self,
        bit_number
    ):

        return bool(
            self.route_items_mask
            & (
                1 << bit_number
            )
        )


    def add_route_item_bit(
        self,
        bit_number
    ):

        self.route_items_mask |= (
            1 << bit_number
        )


    def consume_route_item_bit(
        self,
        bit_number
    ):

        self.route_items_mask &= ~(
            1 << bit_number
        )


# =========================================================
# VERSION 3
# =========================================================
#
# 17 bytes payload
# +
# 5 bytes signature
# =
# 22 bytes
#
# Base64 sem == = 30 caracteres.
#
# =========================================================

def generate_password(
    progress
):

    version = 3


    money = max(
        0,
        min(
            progress.money,
            0xFFFFFF
        )
    )


    ship_core = (

        (
            progress.ship_id
            & 0b11
        )

        |

        (
            (
                progress.nav_core_parts
                & 0b11
            )
            << 2
        )
    )


    meta = (

        (
            progress.continues
            & 0x0F
        )

        |

        (
            (
                progress.flags
                & 0x0F
            )
            << 4
        )
    )


    nonce = (
        secrets.token_bytes(
            3
        )
    )


    payload = bytearray()


    payload.append(
        version
    )


    payload.append(
        progress.next_level
    )


    payload.extend(
        money.to_bytes(
            3,
            "big"
        )
    )


    payload.append(
        progress.max_hp
    )


    payload.append(
        progress.primary_weapon
    )


    payload.append(
        ship_core
    )


    payload.extend(
        progress.completed_mask
        .to_bytes(
            2,
            "big"
        )
    )


    payload.extend(
        progress.discovered_mask
        .to_bytes(
            2,
            "big"
        )
    )


    payload.append(
        progress.route_items_mask
    )


    payload.append(
        meta
    )


    payload.extend(
        nonce
    )


    payload = bytes(
        payload
    )


    signature = (
        hashlib.sha256(
            SECRET + payload
        ).digest()[:5]
    )


    raw = (
        payload
        + signature
    )


    return (
        base64.urlsafe_b64encode(
            raw
        )
        .decode("ascii")
        .rstrip("=")
    )


# =========================================================
# DECODE
# =========================================================

def decode_password(
    password
):

    password = (
        password.strip()
    )


    if len(password) != 30:

        return None


    try:

        raw = (
            base64.urlsafe_b64decode(
                (
                    password
                    + "=="
                ).encode(
                    "ascii"
                )
            )
        )

    except Exception:

        return None


    if len(raw) != 22:

        return None


    payload = raw[:17]

    signature = raw[17:]


    version = payload[0]


    # =====================================================
    # VERSION 3
    # =====================================================

    if version == 3:

        expected = (
            hashlib.sha256(
                SECRET + payload
            ).digest()[:5]
        )


        if signature != expected:

            return None


        current_location = (
            payload[1]
        )


        money = int.from_bytes(
            payload[2:5],
            "big"
        )


        max_hp = (
            payload[5]
        )


        primary_weapon = (
            payload[6]
        )


        ship_core = (
            payload[7]
        )


        ship_id = (
            ship_core
            & 0b11
        )


        nav_core_parts = (
            (
                ship_core
                >> 2
            )
            & 0b11
        )


        completed_mask = (
            int.from_bytes(
                payload[8:10],
                "big"
            )
        )


        discovered_mask = (
            int.from_bytes(
                payload[10:12],
                "big"
            )
        )


        route_items_mask = (
            payload[12]
        )


        meta = (
            payload[13]
        )


        continues = (
            meta
            & 0x0F
        )


        flags = (
            (
                meta
                >> 4
            )
            & 0x0F
        )


        if not (
            1
            <= current_location
            <= 14
        ):

            return None


        if not (
            0 <= ship_id <= 2
        ):

            return None


        if not (
            0
            <= nav_core_parts
            <= 3
        ):

            return None


        return GameProgress(

            next_level=
            current_location,

            money=
            money,

            max_hp=
            max_hp,

            continues=
            continues,

            primary_weapon=
            primary_weapon,

            flags=
            flags,

            ship_id=
            ship_id,

            nav_core_parts=
            nav_core_parts,

            completed_mask=
            completed_mask,

            discovered_mask=
            discovered_mask,

            route_items_mask=
            route_items_mask
        )


    # =====================================================
    # VERSION 2 COMPATIBILITY
    # =====================================================

    elif version == 2:

        OLD_SECRET = (
            b"SHIP_WAR_RETRO_2026_V2"
        )


        expected = (
            hashlib.sha256(
                OLD_SECRET
                + payload
            ).digest()[:5]
        )


        if signature != expected:

            return None


        try:

            (
                _,
                next_level,
                money,
                max_hp,
                continues,
                primary_weapon,
                flags,
                ship_id,
                nav_core_parts,
                _reserved,
                _nonce

            ) = struct.unpack(
                ">BBIBBBBBBB4s",
                payload
            )

        except struct.error:

            return None


        completed = 0

        discovered = 0


        for level in range(
            1,
            next_level + 1
        ):

            discovered |= (
                level_bit(
                    level
                )
            )


        for level in range(
            1,
            next_level
        ):

            completed |= (
                level_bit(
                    level
                )
            )


        return GameProgress(

            next_level=
            next_level,

            money=
            money,

            max_hp=
            max_hp,

            continues=
            continues,

            primary_weapon=
            primary_weapon,

            flags=
            flags,

            ship_id=
            ship_id,

            nav_core_parts=
            nav_core_parts,

            completed_mask=
            completed,

            discovered_mask=
            discovered,

            route_items_mask=0
        )


    return None