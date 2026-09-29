import math
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
        center,
        velocity,
        damage=1,
        owner="player",
        kind="normal",
        max_hits=1,
        blast_radius=0,
        target=None
    ):

        super().__init__()


        self.image = (
            image.copy()
        )


        self.position = (
            pygame.Vector2(
                center
            )
        )


        self.velocity = (
            pygame.Vector2(
                velocity
            )
        )


        self.damage = (
            damage
        )


        self.owner = (
            owner
        )


        self.kind = (
            kind
        )


        self.max_hits = max(
            1,
            max_hits
        )


        self.hit_count = 0

        self.hit_ids = set()


        self.blast_radius = (
            blast_radius
        )


        self.target = (
            target
        )


        self.rect = (
            self.image.get_rect(
                center=center
            )
        )


    # =====================================================
    # COLLISION
    # =====================================================

    def can_hit(
        self,
        sprite
    ):

        return (
            id(sprite)
            not in self.hit_ids
        )


    def register_hit(
        self,
        sprite
    ):

        self.hit_ids.add(
            id(sprite)
        )


        self.hit_count += 1


        if (
            self.hit_count
            >= self.max_hits
        ):

            self.kill()


    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        dt
    ):

        # Missile homing.
        if (
            self.kind == "missile"

            and self.target is not None

            and self.target.alive()
        ):

            target_vector = (

                pygame.Vector2(
                    self.target.rect.center
                )

                - self.position
            )


            if (
                target_vector.length_squared()
                > 0
            ):

                speed = (
                    self.velocity.length()
                )


                desired = (
                    target_vector.normalize()
                    * speed
                )


                # Steering suave.
                self.velocity = (
                    self.velocity.lerp(
                        desired,
                        min(
                            1.0,
                            dt * 4.0
                        )
                    )
                )


        self.position += (
            self.velocity
            * dt
        )


        self.rect.center = (

            round(
                self.position.x
            ),

            round(
                self.position.y
            )
        )


        margin = 100


        if (
            self.rect.bottom < -margin

            or self.rect.top
            > SCREEN_HEIGHT + margin

            or self.rect.right < -margin

            or self.rect.left
            > SCREEN_WIDTH + margin
        ):

            self.kill()