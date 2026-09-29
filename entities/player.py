import math
import random
import pygame

from settings import (
    SCREEN_WIDTH,
    PLAY_AREA_BOTTOM,
    PLAYER_INVULNERABILITY
)

from game_data import (
    PRIMARY_WEAPONS,
    SECONDARY_WEAPONS,
    DEFENSE_MODULES
)

from entities.projectile import (
    Projectile
)


# =========================================================
# WEAPON COLORS
# =========================================================
#
# Todas usam o MESMO PNG.
#
# O código apenas aplica uma tonalidade diferente.
#
# =========================================================

PRIMARY_SHOT_COLORS = {

    0: (120, 220, 255),     # Pulse I - cyan

    1: (80, 255, 255),      # Pulse II - cyan intenso

    2: (100, 255, 150),     # Twin - verde

    3: (255, 170, 70),      # Heavy - laranja

    4: (255, 100, 190),     # Spread - rosa

    5: (190, 100, 255),     # Plasma Lance - violeta

    6: (255, 245, 170)      # Ancient Grey - dourado claro
}


SECONDARY_SHOT_COLORS = {

    1: (255, 210, 80),      # Missile

    2: (255, 90, 220),      # Plasma bomb

    3: (100, 180, 255),     # EMP

    4: (120, 255, 220),     # Defense burst

    5: (130, 180, 255)      # Chain lightning
}


class Player(
    pygame.sprite.Sprite
):

    def __init__(
        self,
        image,
        shot_image,
        ship_config,
        progress
    ):

        super().__init__()


        # =====================================================
        # SPRITE
        # =====================================================

        self.image = image

        self.shot_image = (
            shot_image
        )


        # =====================================================
        # SHIP
        # =====================================================

        self.ship_config = (
            ship_config
        )


        self.ship_id = (
            ship_config[
                "id"
            ]
        )


        self.ship_name = (
            ship_config[
                "name"
            ]
        )


        self.speed = (
            ship_config[
                "speed"
            ]
        )


        # =====================================================
        # HULL / MONEY
        # =====================================================

        self.max_hp = (
            progress.max_hp
        )


        self.hp = (
            self.max_hp
        )


        self.money = (
            progress.money
        )


        # =====================================================
        # LOADOUT
        # =====================================================

        self.primary_id = (
            progress.equipped_primary
        )


        self.secondary_id = (
            progress.equipped_secondary
        )


        self.defense_id = (
            progress.equipped_defense
        )


        # Compatibilidade.
        self.primary_weapon = (
            self.primary_id
        )

        self.secondary_weapon = (
            self.secondary_id
        )

        self.defense_module = (
            self.defense_id
        )


        # =====================================================
        # EQUIPMENT CONFIG
        # =====================================================

        self.primary = (
            PRIMARY_WEAPONS[
                self.primary_id
            ]
        )


        self.secondary = (
            SECONDARY_WEAPONS[
                self.secondary_id
            ]
        )


        self.defense = (
            DEFENSE_MODULES[
                self.defense_id
            ]
        )


        # =====================================================
        # EQUIPMENT NAMES
        # =====================================================

        self.weapon_name = (
            self.primary[
                "name"
            ]
        )


        self.secondary_name = (
            self.secondary[
                "name"
            ]
        )


        self.defense_name = (
            self.defense[
                "name"
            ]
        )


        # =====================================================
        # POSITION
        # =====================================================

        self.position = (
            pygame.Vector2(
                SCREEN_WIDTH / 2,
                PLAY_AREA_BOTTOM - 80
            )
        )


        self.rect = (
            self.image.get_rect(
                center=self.position
            )
        )


        # =====================================================
        # TIMERS
        # =====================================================

        self.primary_timer = 0

        self.secondary_timer = 0

        self.invulnerable_timer = 0


        # =====================================================
        # ANCIENT GREY CANNON
        # =====================================================

        self.overheat_shots = 0

        self.overheat_timer = 0


        # =====================================================
        # DEFENSE
        # =====================================================

        self.shield_capacity = (
            self.defense.get(
                "capacity",
                0
            )
        )


        self.shield_points = (
            self.shield_capacity
        )


        self.shield_recharge_timer = 0


        self.reactive_timer = 0


        self.emergency_repair_used = (
            False
        )


    # =====================================================
    # HITBOX
    # =====================================================

    @property
    def hitbox(self):

        width = int(
            self.rect.width
            * 0.45
        )


        height = int(
            self.rect.height
            * 0.60
        )


        hitbox = pygame.Rect(
            0,
            0,
            width,
            height
        )


        hitbox.center = (
            self.rect.center
        )


        return hitbox


    # =====================================================
    # TINT PROJECTILE
    # =====================================================

    def tint_shot(
        self,
        image,
        color
    ):

        """
        Preserva transparência e detalhes do PNG,
        alterando apenas sua tonalidade.

        Funciona melhor quando shot_player.png
        é branco/claro.
        """

        tinted = (
            image.copy()
        )


        tinted.fill(

            (
                color[0],
                color[1],
                color[2],
                255
            ),

            special_flags=
            pygame.BLEND_RGBA_MULT
        )


        return tinted


    def get_primary_shot_image(
        self
    ):

        color = (
            PRIMARY_SHOT_COLORS.get(
                self.primary_id,
                (
                    255,
                    255,
                    255
                )
            )
        )


        return self.tint_shot(
            self.shot_image,
            color
        )


    def get_secondary_shot_image(
        self
    ):

        color = (
            SECONDARY_SHOT_COLORS.get(
                self.secondary_id,
                (
                    255,
                    255,
                    255
                )
            )
        )


        return self.tint_shot(
            self.shot_image,
            color
        )


    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        dt,
        keys
    ):

        direction = (
            pygame.Vector2()
        )


        if (
            keys[
                pygame.K_LEFT
            ]
            or
            keys[
                pygame.K_a
            ]
        ):

            direction.x -= 1


        if (
            keys[
                pygame.K_RIGHT
            ]
            or
            keys[
                pygame.K_d
            ]
        ):

            direction.x += 1


        if (
            keys[
                pygame.K_UP
            ]
            or
            keys[
                pygame.K_w
            ]
        ):

            direction.y -= 1


        if (
            keys[
                pygame.K_DOWN
            ]
            or
            keys[
                pygame.K_s
            ]
        ):

            direction.y += 1


        if (
            direction.length_squared()
            > 0
        ):

            direction = (
                direction.normalize()
            )


        self.position += (

            direction

            * self.speed

            * dt
        )


        half_w = (
            self.rect.width / 2
        )


        half_h = (
            self.rect.height / 2
        )


        self.position.x = max(

            half_w,

            min(
                SCREEN_WIDTH
                - half_w,

                self.position.x
            )
        )


        self.position.y = max(

            half_h,

            min(
                PLAY_AREA_BOTTOM
                - half_h,

                self.position.y
            )
        )


        self.rect.center = (

            round(
                self.position.x
            ),

            round(
                self.position.y
            )
        )


        # =================================================
        # TIMERS
        # =================================================

        self.primary_timer = max(
            0,
            self.primary_timer - dt
        )


        self.secondary_timer = max(
            0,
            self.secondary_timer - dt
        )


        self.invulnerable_timer = max(
            0,
            self.invulnerable_timer - dt
        )


        self.overheat_timer = max(
            0,
            self.overheat_timer - dt
        )


        self.reactive_timer = max(
            0,
            self.reactive_timer - dt
        )


        # =================================================
        # SHIELD RECHARGE
        # =================================================

        if (
            self.shield_capacity > 0

            and self.shield_points
            < self.shield_capacity
        ):

            self.shield_recharge_timer += (
                dt
            )


            recharge_time = (

                self.defense[
                    "recharge_time"
                ]

                * self.ship_config[
                    "shield_recharge_modifier"
                ]
            )


            if (
                self.shield_recharge_timer
                >= recharge_time
            ):

                self.shield_points += 1

                self.shield_recharge_timer = 0


    # =====================================================
    # PRIMARY FIRE
    # =====================================================

    def shoot(self):

        if (
            self.primary_timer > 0
        ):

            return []


        if (
            self.overheat_timer > 0
        ):

            return []


        cooldown = (

            self.primary[
                "cooldown"
            ]

            * self.ship_config[
                "primary_cooldown_modifier"
            ]
        )


        self.primary_timer = (
            cooldown
        )


        # =================================================
        # ANCIENT GREY OVERHEAT
        # =================================================

        if (
            "overheat_after"
            in self.primary
        ):

            self.overheat_shots += 1


            if (
                self.overheat_shots
                >= self.primary[
                    "overheat_after"
                ]
            ):

                self.overheat_shots = 0


                self.overheat_timer = (
                    self.primary[
                        "overheat_time"
                    ]
                )


        projectiles = []


        pattern = (
            self.primary[
                "pattern"
            ]
        )


        if (
            pattern
            == "single"
        ):

            projectiles.append(

                self.create_primary_projectile(
                    0,
                    0
                )
            )


        elif (
            pattern
            == "twin"
        ):

            projectiles.append(

                self.create_primary_projectile(
                    -11,
                    0
                )
            )


            projectiles.append(

                self.create_primary_projectile(
                    11,
                    0
                )
            )


        elif (
            pattern
            == "spread"
        ):

            projectiles.append(

                self.create_primary_projectile(
                    0,
                    -12
                )
            )


            projectiles.append(

                self.create_primary_projectile(
                    0,
                    0
                )
            )


            projectiles.append(

                self.create_primary_projectile(
                    0,
                    12
                )
            )


        return projectiles


    # =====================================================
    # PRIMARY PROJECTILE
    # =====================================================

    def create_primary_projectile(
        self,
        offset_x,
        angle_degrees
    ):

        angle = math.radians(
            angle_degrees
        )


        speed = (
            self.primary[
                "speed"
            ]
        )


        velocity = pygame.Vector2(

            math.sin(
                angle
            )
            * speed,

            -math.cos(
                angle
            )
            * speed
        )


        return Projectile(

            image=
            self.get_primary_shot_image(),

            center=(
                self.rect.centerx
                + offset_x,

                self.rect.top
            ),

            velocity=
            velocity,

            damage=
            self.primary[
                "damage"
            ],

            owner=
            "player",

            kind=
            "primary",

            max_hits=
            self.primary[
                "max_hits"
            ]
        )


    # =====================================================
    # SECONDARY
    # =====================================================

    def can_use_secondary(self):

        return (

            self.secondary_id
            != 0

            and self.secondary_timer
            <= 0
        )


    def consume_secondary_cooldown(
        self
    ):

        self.secondary_timer = (

            self.secondary[
                "cooldown"
            ]

            * self.ship_config[
                "secondary_cooldown_modifier"
            ]
        )


    # =====================================================
    # DEFENSE BURST
    # =====================================================

    def activate_defense_burst(
        self
    ):

        self.invulnerable_timer = max(

            self.invulnerable_timer,

            self.secondary[
                "duration"
            ]
        )


    # =====================================================
    # DAMAGE
    # =====================================================

    def take_damage(
        self,
        damage
    ):

        if (
            self.invulnerable_timer
            > 0
        ):

            return False


        # =================================================
        # PHASE SHIELD
        # =================================================

        if (
            self.defense[
                "kind"
            ]
            == "phase"

            and random.random()
            < self.defense[
                "phase_chance"
            ]
        ):

            self.invulnerable_timer = (
                0.20
            )

            return False


        # =================================================
        # SHIELD
        # =================================================

        if (
            self.defense[
                "kind"
            ]
            == "shield"

            and self.shield_points > 0
        ):

            self.shield_points -= 1

            self.shield_recharge_timer = 0

            self.invulnerable_timer = (
                0.20
            )

            return False


        # =================================================
        # REACTIVE ARMOR
        # =================================================

        if (
            self.defense[
                "kind"
            ]
            == "reactive"

            and self.reactive_timer
            <= 0
        ):

            self.reactive_timer = (
                self.defense[
                    "cooldown"
                ]
            )

            self.invulnerable_timer = (
                0.20
            )

            return False


        # =================================================
        # HULL DAMAGE
        # =================================================

        self.hp -= (
            damage
        )


        self.hp = max(
            0,
            self.hp
        )


        self.invulnerable_timer = (
            PLAYER_INVULNERABILITY
        )


        # =================================================
        # EMERGENCY REPAIR
        # =================================================

        if (
            self.defense[
                "kind"
            ]
            == "repair"

            and not self.emergency_repair_used

            and self.hp <= 1

            and self.hp > 0
        ):

            self.hp = min(
                self.max_hp,
                self.hp + 1
            )


            self.emergency_repair_used = (
                True
            )


        return True


    # =====================================================
    # HEAL
    # =====================================================

    def heal(
        self,
        amount
    ):

        self.hp = min(

            self.max_hp,

            self.hp
            + amount
        )


    # =====================================================
    # DEAD
    # =====================================================

    def is_dead(self):

        return (
            self.hp <= 0
        )