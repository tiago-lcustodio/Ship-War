from settings import (
    PLAY_AREA_BOTTOM
)


def horizontal(
    enemy,
    dt
):

    enemy.position.x += (
        enemy.direction
        * enemy.speed
        * dt
    )


    enemy.position.y += (
        enemy.vertical_speed
        * dt
    )


    enemy.rect.center = (
        round(
            enemy.position.x
        ),
        round(
            enemy.position.y
        )
    )


    top_limit = 70

    bottom_limit = (
        PLAY_AREA_BOTTOM - 40
    )


    if (
        enemy.rect.top
        < top_limit
    ):

        enemy.rect.top = (
            top_limit
        )


        enemy.position.y = (
            enemy.rect.centery
        )


        enemy.vertical_speed *= -1


    if (
        enemy.rect.bottom
        > bottom_limit
    ):

        enemy.rect.bottom = (
            bottom_limit
        )


        enemy.position.y = (
            enemy.rect.centery
        )


        enemy.vertical_speed *= -1


MOVEMENT_PATTERNS = {

    "horizontal":
    horizontal
}