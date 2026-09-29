import math

from settings import (
    SCREEN_WIDTH
)


# =========================================================
# HELPERS
# =========================================================

def clamp_x(enemy):

    margin = (
        enemy.rect.width / 2
        + 8
    )

    enemy.position.x = max(
        margin,
        min(
            SCREEN_WIDTH - margin,
            enemy.position.x
        )
    )


# =========================================================
# HORIZONTAL
# =========================================================
#
# Movimento simples.
#
# Desce lentamente enquanto se move
# lateralmente e rebate nas bordas.
#
# =========================================================

def horizontal(
    enemy,
    dt
):

    enemy.position.y += (
        enemy.vertical_speed
        * dt
    )

    enemy.position.x += (
        enemy.horizontal_direction
        * enemy.horizontal_speed
        * dt
    )


    margin = (
        enemy.rect.width / 2
        + 10
    )


    if (
        enemy.position.x <= margin
    ):

        enemy.position.x = margin

        enemy.horizontal_direction = 1


    elif (
        enemy.position.x
        >= SCREEN_WIDTH - margin
    ):

        enemy.position.x = (
            SCREEN_WIDTH - margin
        )

        enemy.horizontal_direction = -1


# =========================================================
# ZIGZAG
# =========================================================
#
# Inimigo frágil e rápido.
#
# Desce normalmente, mas oscila em X.
#
# =========================================================

def zigzag(
    enemy,
    dt
):

    enemy.position.y += (
        enemy.vertical_speed
        * dt
    )


    amplitude = (
        enemy.config.get(
            "zigzag_amplitude",
            80
        )
    )


    frequency = (
        enemy.config.get(
            "zigzag_frequency",
            3.0
        )
    )


    enemy.position.x = (

        enemy.base_x

        + math.sin(
            enemy.movement_time
            * frequency
            + enemy.movement_phase
        )

        * amplitude
    )


    clamp_x(
        enemy
    )


# =========================================================
# STRAFE
# =========================================================
#
# Entra na tela, segura determinada altitude
# e começa a fazer ataques laterais.
#
# Depois de alguns segundos volta a descer.
#
# =========================================================

def strafe(
    enemy,
    dt
):

    hold_y = (
        enemy.config.get(
            "strafe_y",
            145
        )
    )


    hold_time = (
        enemy.config.get(
            "strafe_duration",
            4.0
        )
    )


    amplitude = (
        enemy.config.get(
            "strafe_amplitude",
            150
        )
    )


    frequency = (
        enemy.config.get(
            "strafe_frequency",
            2.3
        )
    )


    # Ainda entrando.
    if (
        enemy.position.y < hold_y
    ):

        enemy.position.y += (
            enemy.vertical_speed
            * dt
        )

        return


    # Começa a contar o tempo
    # estacionado na região de combate.
    enemy.strafe_timer += (
        dt
    )


    if (
        enemy.strafe_timer
        <= hold_time
    ):

        enemy.position.y = (
            hold_y
        )


        enemy.position.x = (

            enemy.base_x

            + math.sin(
                enemy.strafe_timer
                * frequency
                + enemy.movement_phase
            )

            * amplitude
        )


        clamp_x(
            enemy
        )


    else:

        # Depois do ataque,
        # finalmente abandona a tela.
        enemy.position.y += (
            enemy.vertical_speed
            * 1.25
            * dt
        )


# =========================================================
# DIVE
# =========================================================
#
# Entra normalmente.
#
# Quando chega à região superior da tela,
# trava a posição atual do jogador e mergulha.
#
# O alvo NÃO é atualizado durante o mergulho.
#
# Isso permite ao jogador esquivar.
#
# =========================================================

def dive(
    enemy,
    dt
):

    if (
        not enemy.dive_started
    ):

        enemy.position.y += (
            enemy.vertical_speed
            * 0.70
            * dt
        )


        enemy.position.x += (

            math.sin(
                enemy.movement_time
                * 2.0
                + enemy.movement_phase
            )

            * 18

            * dt
        )


        trigger_y = (
            enemy.config.get(
                "dive_trigger_y",
                105
            )
        )


        if (
            enemy.position.y
            >= trigger_y

            and enemy.player_ref
            is not None
        ):

            target = (
                pygame_vector(
                    enemy.player_ref
                    .rect.center
                )
            )


            direction = (
                target
                - enemy.position
            )


            if (
                direction.length_squared()
                > 0
            ):

                dive_speed = (
                    enemy.config.get(
                        "dive_speed",
                        330
                    )
                )


                enemy.dive_velocity = (

                    direction.normalize()

                    * dive_speed
                )


                enemy.dive_started = (
                    True
                )


    else:

        enemy.position += (
            enemy.dive_velocity
            * dt
        )


# =========================================================
# PURSUIT
# =========================================================
#
# Persegue a coordenada X do jogador.
#
# Não aponta diretamente para ele em Y,
# então continua sendo um shooter vertical
# e não uma nave "teleguiada".
#
# =========================================================

def pursuit(
    enemy,
    dt
):

    enemy.position.y += (

        enemy.vertical_speed
        * 0.65
        * dt
    )


    if (
        enemy.player_ref
        is None
    ):

        return


    target_x = (
        enemy.player_ref
        .rect.centerx
    )


    pursuit_speed = (
        enemy.config.get(
            "pursuit_speed",
            130
        )
    )


    difference = (
        target_x
        - enemy.position.x
    )


    max_step = (
        pursuit_speed
        * dt
    )


    if abs(
        difference
    ) <= max_step:

        enemy.position.x = (
            target_x
        )

    else:

        enemy.position.x += (

            max_step

            if difference > 0

            else -max_step
        )


    clamp_x(
        enemy
    )


# =========================================================
# FORMATION
# =========================================================
#
# Todos os membros de uma formação recebem:
#
# - posições iniciais diferentes
# - a mesma fase de oscilação
#
# Assim permanecem organizados
# enquanto atravessam a tela.
#
# =========================================================

def formation(
    enemy,
    dt
):

    enemy.position.y += (

        enemy.vertical_speed
        * 0.85
        * dt
    )


    amplitude = (
        enemy.config.get(
            "formation_amplitude",
            25
        )
    )


    frequency = (
        enemy.config.get(
            "formation_frequency",
            1.8
        )
    )


    enemy.position.x = (

        enemy.base_x

        + math.sin(
            enemy.movement_time
            * frequency
            + enemy.movement_phase
        )

        * amplitude
    )


    clamp_x(
        enemy
    )


# =========================================================
# SMALL VECTOR HELPER
# =========================================================
#
# Import local para deixar este arquivo
# independente da inicialização do display.
#
# =========================================================

def pygame_vector(
    value
):

    from pygame import Vector2

    return Vector2(
        value
    )


# =========================================================
# REGISTRY
# =========================================================

MOVEMENT_PATTERNS = {

    "horizontal":
        horizontal,

    "zigzag":
        zigzag,

    "strafe":
        strafe,

    "dive":
        dive,

    "pursuit":
        pursuit,

    "formation":
        formation
}