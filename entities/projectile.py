import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)


class Projectile(
    pygame.sprite.Sprite
):

    def __init__(
        self,
        image,
        x,
        y,
        velocity_x,
        velocity_y,
        damage,
        owner
    ):

        super().__init__()


        self.image = image


        self.rect = (
            self.image.get_rect(
                center=(x, y)
            )
        )


        self.position = (
            pygame.Vector2(
                x,
                y
            )
        )


        self.velocity = (
            pygame.Vector2(
                velocity_x,
                velocity_y
            )
        )


        self.damage = damage

        self.owner = owner


    def update(
        self,
        dt
    ):

        self.position += (
            self.velocity
            * dt
        )


        self.rect.center = (
            round(self.position.x),
            round(self.position.y)
        )


        margin = 100


        if (
            self.rect.bottom
            < -margin

            or self.rect.top
            > SCREEN_HEIGHT + margin

            or self.rect.right
            < -margin

            or self.rect.left
            > SCREEN_WIDTH + margin
        ):

            self.kill()