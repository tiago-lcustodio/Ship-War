import base64
import hashlib
import secrets

from dataclasses import dataclass


SECRET = b"SHIP_WAR_RETRO_2026_V4"


def level_bit(level_number):

    return 1 << (
        level_number - 1
    )


@dataclass
class GameProgress:

    next_level: int = 1

    money: int = 0

    max_hp: int = 3

    continues: int = 0

    flags: int = 0

    nav_core_parts: int = 0

    completed_mask: int = 0
    discovered_mask: int = 1

    # =====================================================
    # NAVIGATION CHIPS
    # =====================================================

    nav_chips: int = 0


    # =====================================================
    # CURRENT LOADOUT
    # =====================================================

    ship_id: int = 0

    equipped_primary: int = 0
    equipped_secondary: int = 0
    equipped_defense: int = 0


    # =====================================================
    # OWNED EQUIPMENT
    # =====================================================

    # Pulse Cannon I / Classic Saucer already owned.
    owned_primary_mask: int = 1
    owned_secondary_mask: int = 0
    owned_defense_mask: int = 0
    owned_ships_mask: int = 1


    # =====================================================
    # COPY
    # =====================================================

    def clone(self):

        return GameProgress(

            next_level=self.next_level,

            money=self.money,

            max_hp=self.max_hp,

            continues=self.continues,

            flags=self.flags,

            nav_core_parts=self.nav_core_parts,

            completed_mask=self.completed_mask,

            discovered_mask=self.discovered_mask,

            nav_chips=self.nav_chips,

            ship_id=self.ship_id,

            equipped_primary=self.equipped_primary,

            equipped_secondary=self.equipped_secondary,

            equipped_defense=self.equipped_defense,

            owned_primary_mask=self.owned_primary_mask,

            owned_secondary_mask=self.owned_secondary_mask,

            owned_defense_mask=self.owned_defense_mask,

            owned_ships_mask=self.owned_ships_mask
        )


    # =====================================================
    # LEVELS
    # =====================================================

    def is_completed(self, level_number):

        return bool(
            self.completed_mask
            & level_bit(level_number)
        )


    def mark_completed(self, level_number):

        self.completed_mask |= (
            level_bit(level_number)
        )


    def is_discovered(self, level_number):

        return bool(
            self.discovered_mask
            & level_bit(level_number)
        )


    def discover(self, level_number):

        self.discovered_mask |= (
            level_bit(level_number)
        )


    # =====================================================
    # EQUIPMENT
    # =====================================================

    def owns_primary(self, equipment_id):

        return bool(
            self.owned_primary_mask
            & (1 << equipment_id)
        )


    def own_primary(self, equipment_id):

        self.owned_primary_mask |= (
            1 << equipment_id
        )


    def owns_secondary(self, equipment_id):

        if equipment_id == 0:
            return True

        return bool(
            self.owned_secondary_mask
            & (1 << equipment_id)
        )


    def own_secondary(self, equipment_id):

        if equipment_id > 0:

            self.owned_secondary_mask |= (
                1 << equipment_id
            )


    def owns_defense(self, equipment_id):

        if equipment_id == 0:
            return True

        return bool(
            self.owned_defense_mask
            & (1 << equipment_id)
        )


    def own_defense(self, equipment_id):

        if equipment_id > 0:

            self.owned_defense_mask |= (
                1 << equipment_id
            )


    def owns_ship(self, ship_id):

        return bool(
            self.owned_ships_mask
            & (1 << ship_id)
        )


    def own_ship(self, ship_id):

        self.owned_ships_mask |= (
            1 << ship_id
        )


# =========================================================
# PASSWORD V4
# =========================================================
#
# 17 byte payload
# + 5 byte signature
# = 22 bytes
#
# Base64 URL-safe sem == = 30 chars.
#
# =========================================================

def generate_password(progress):

    payload = bytearray()


    # 0
    payload.append(4)


    # 1
    payload.append(
        progress.next_level & 0xFF
    )


    # 2..4
    money = max(
        0,
        min(
            progress.money,
            0xFFFFFF
        )
    )

    payload.extend(
        money.to_bytes(
            3,
            "big"
        )
    )


    # 5
    payload.append(
        progress.max_hp & 0xFF
    )


    # 6
    #
    # bits 0-1 = ship
    # bits 2-4 = primary
    # bits 5-7 = secondary

    packed_equipment = (

        (progress.ship_id & 0b11)

        |

        (
            (
                progress.equipped_primary
                & 0b111
            )
            << 2
        )

        |

        (
            (
                progress.equipped_secondary
                & 0b111
            )
            << 5
        )
    )

    payload.append(
        packed_equipment
    )


    # 7
    #
    # bits 0-2 = defense
    # bits 3-4 = nav core
    # bits 5-7 = nav chips

    packed_status = (

        (
            progress.equipped_defense
            & 0b111
        )

        |

        (
            (
                progress.nav_core_parts
                & 0b11
            )
            << 3
        )

        |

        (
            (
                min(
                    progress.nav_chips,
                    7
                )
                & 0b111
            )
            << 5
        )
    )

    payload.append(
        packed_status
    )


    # 8
    payload.append(

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


    # 9..10
    payload.extend(
        progress.completed_mask.to_bytes(
            2,
            "big"
        )
    )


    # 11..12
    payload.extend(
        progress.discovered_mask.to_bytes(
            2,
            "big"
        )
    )


    # 13
    payload.append(
        progress.owned_primary_mask
        & 0xFF
    )


    # 14
    payload.append(
        progress.owned_secondary_mask
        & 0xFF
    )


    # 15
    payload.append(
        progress.owned_defense_mask
        & 0xFF
    )


    # 16
    #
    # low 3 bits = ships
    # remaining bits = tiny nonce

    nonce = (
        secrets.randbits(5)
        << 3
    )

    payload.append(

        nonce

        |

        (
            progress.owned_ships_mask
            & 0b111
        )
    )


    payload = bytes(payload)


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


def decode_password(password):

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


    if version != 4:

        return None


    expected = (
        hashlib.sha256(
            SECRET + payload
        ).digest()[:5]
    )


    if signature != expected:

        return None


    next_level = (
        payload[1]
    )


    money = int.from_bytes(
        payload[2:5],
        "big"
    )


    max_hp = (
        payload[5]
    )


    equipment = (
        payload[6]
    )


    ship_id = (
        equipment
        & 0b11
    )


    equipped_primary = (
        (
            equipment
            >> 2
        )
        & 0b111
    )


    equipped_secondary = (
        (
            equipment
            >> 5
        )
        & 0b111
    )


    status = (
        payload[7]
    )


    equipped_defense = (
        status
        & 0b111
    )


    nav_core_parts = (
        (
            status
            >> 3
        )
        & 0b11
    )


    nav_chips = (
        (
            status
            >> 5
        )
        & 0b111
    )


    meta = (
        payload[8]
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


    completed_mask = (
        int.from_bytes(
            payload[9:11],
            "big"
        )
    )


    discovered_mask = (
        int.from_bytes(
            payload[11:13],
            "big"
        )
    )


    owned_primary_mask = (
        payload[13]
    )


    owned_secondary_mask = (
        payload[14]
    )


    owned_defense_mask = (
        payload[15]
    )


    owned_ships_mask = (
        payload[16]
        & 0b111
    )


    if not (
        1 <= next_level <= 14
    ):

        return None


    if not (
        3 <= max_hp <= 7
    ):

        return None


    if ship_id > 2:

        return None


    if nav_core_parts > 3:

        return None


    progress = GameProgress(

        next_level=next_level,

        money=money,

        max_hp=max_hp,

        continues=continues,

        flags=flags,

        nav_core_parts=nav_core_parts,

        completed_mask=completed_mask,

        discovered_mask=discovered_mask,

        nav_chips=nav_chips,

        ship_id=ship_id,

        equipped_primary=equipped_primary,

        equipped_secondary=equipped_secondary,

        equipped_defense=equipped_defense,

        owned_primary_mask=owned_primary_mask,

        owned_secondary_mask=owned_secondary_mask,

        owned_defense_mask=owned_defense_mask,

        owned_ships_mask=owned_ships_mask
    )


    # Proteções mínimas.
    progress.own_primary(0)
    progress.own_ship(0)


    return progress