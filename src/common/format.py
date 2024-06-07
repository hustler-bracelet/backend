
def format_number(number: float) -> str:
    number = round(number, 1)
    if not isinstance(number, int):
        if number.is_integer():
            number = int(number)

    return f'{number:_}'.replace('_', ' ') 
