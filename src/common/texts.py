
def format_number(number: float) -> str:
    number = round(number, 1)
    if not isinstance(number, int):
        if number.is_integer():
            number = int(number)

    return f'{number:_}'.replace('_', ' ')


def plural_form(number: int, titles: tuple[str, ...] | list[str], include_number: bool = True, do_format_number: bool = True):
    """
    :param include_number:
    :param number:
    :param titles: 1 Минута, 2 минуты, 0 минут
    :return:
    """

    cases = [2, 0, 1, 1, 1, 2]

    if 4 < number % 100 < 20:
        idx = 2
    elif number % 10 < 5:
        idx = cases[number % 10]
    else:
        idx = cases[5]

    title = titles[idx]
    if include_number:
        return f'{format_number(number)} {title}'
    return title
