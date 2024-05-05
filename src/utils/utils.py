def string_from_numbers(text:str, )->list[int]:
    numbers = [int(s) for s in text.split() if s.isdigit()]
    return numbers