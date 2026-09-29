import pygame

from settings import (
    SCREEN_WIDTH,
    PLAY_AREA_BOTTOM,
    PLAYER_FIRE_COOLDOWN,
    PLAYER_INVULNERABILITY,
    PLAYER_SHOT_SPEED,
    PLAYER_SHOT_DAMAGE
)

from entities.projectile import (
    Projectile
)


class Player(
    pygame.sprite.Sprite
):

    def __init__(
        self,
        image,
        shot_image,
        ship_config,
        max_hp,
        money=0
    ):

        super().__init__()


        self.image = image

        self.rect = (
            self.image.get_rect()
        )


        self.position = (
            pygame.Vector2(
                SCREEN_WIDTH / 2,
                PLAY_AREA_BOTTOM - 60
            )
        )


        self.rect.center = (
            self.position
        )


        self.ship_config = (
            ship_config
        )


        self.ship_id = (
            ship_config["id"]
        )


        self.ship_name = (
            ship_config["name"]
        )


        self.speed = (
            ship_config["speed"]
        )


        self.max_hp = (
            max_hp
        )


        self.hp = (
            max_hp
        )


        self.money = (
            money
        )


        self.weapon_name = (
            "PULSE"
        )


        self.shot_image = (
            shot_image
        )


        self.fire_timer = 0

        self.invulnerable_timer = 0


    @property
    def hitbox(
        self
    ):

        width = int(
            self.rect.width * 0.45
        )


        height = int(
            self.rect.height * 0.60
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


    def update(
        self,
        dt,
        keys
    ):

        direction = pygame.Vector2(
            0,
            0
        )


        if (
            keys[pygame.K_LEFT]
            or keys[pygame.K_a]
        ):

            direction.x -= 1


        if (
            keys[pygame.K_RIGHT]
            or keys[pygame.K_d]
        ):

            direction.x += 1


        if (
            keys[pygame.K_UP]
            or keys[pygame.K_w]
        ):

            direction.y -= 1


        if (
            keys[pygame.K_DOWN]
            or keys[pygame.K_s]
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


        half_width = (
            self.rect.width / 2
        )


        half_height = (
            self.rect.height / 2
        )


        self.position.x = max(
            half_width,
            min(
                SCREEN_WIDTH
                - half_width,
                self.position.x
            )
        )


        # Mantém o player fora do painel inferior.
        self.position.y = max(
            half_height + 55,
            min(
                PLAY_AREA_BOTTOM
                - half_height,
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


        if self.fire_timer > 0:

            self.fire_timer -= dt


        if (
            self.invulnerable_timer
            > 0
        ):

            self.invulnerable_timer -= dt


    def shoot(
        self
    ):

        if self.fire_timer > 0:

            return None


        self.fire_timer = (
            PLAYER_FIRE_COOLDOWN
        )


        return Projectile(

            image=
            self.shot_image,

            x=
            self.rect.centerx,

            y=
            self.rect.top,

            velocity_x=0,

            velocity_y=
            -PLAYER_SHOT_SPEED,

            damage=
            PLAYER_SHOT_DAMAGE,

            owner="player"
        )


    def take_damage(
        self,
        damage
    ):

        if (
            self.invulnerable_timer
            > 0
        ):

            return False


        self.hp -= damage


        self.invulnerable_timer = (
            PLAYER_INVULNERABILITY
        )


        return True


    def is_dead(
        self
    ):

        return (
            self.hp <= 0
        )