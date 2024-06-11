

def distribute_funds(fund: int, places: int, distribution_ratio: float = 0.8):
    # Подсчёт суммы геометрической прогрессии
    progression_sum = (1 - distribution_ratio ** places) / (1 - distribution_ratio)

    # Подсчёт первого члена прогрессии
    first_prize = fund / progression_sum

    # Генерация результатов
    for i in range(places):
        yield first_prize * (distribution_ratio ** i)
