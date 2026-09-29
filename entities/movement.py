import math

from settings import (
    SCREEN_WIDTH
)


def horizontal(
    enemy,
    dt
):

    enemy.position.x += (
        enemy.horizontal_direction
        * enemy.horizontal_speed
        * dt
    )


    margin = 30


    if (
        enemy.position.x < margin
    ):

        enemy.position.x = margin

        enemy.horizontal_direction = 1


    elif (
        enemy.position.x
        > SCREEN_WIDTH - margin
    ):

        enemy.position.x = (
            SCREEN_WIDTH - margin
        )

        enemy.horizontal_direction = -1


def zigzag(
    enemy,
    dt
):

    enemy.movement_time += (
        dt
    )


    enemy.position.x = (

        enemy.base_x

        + math.sin(
            enemy.movement_time
            * 3.2
        )

        * enemy.horizontal_speed
        * 0.55
    )


    enemy.position.x = max(

        30,

        min(
            SCREEN_WIDTH - 30,
            enemy.position.x
        )
    )


MOVEMENT_PATTERNS = {

    "horizontal": horizontal,

    "zigzag": zigzag
}