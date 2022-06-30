def time_left(days, seconds):
    result = ''
    hours = seconds // 3600
    if days < 0:
        result += '<span class="text-danger">Не согласован в срок</span>'
    else:
        result += 'Осталось: '
        if days > 0:
            result += str(days)
            if days % 10 == 1 and days != 11:
                result += ' день'
            elif 2 <= days % 10 <= 4:
                result += ' дня'
            else:
                result += ' дней'
            if hours >= 1:
                result += ' и '
        if hours >= 1:
            result += str(hours)
            if hours % 10 == 1 and hours != 11:
                result += ' час'
            elif 2 <= hours % 10 <= 4:
                result += ' часа'
            else:
                result += ' часов'
        if days == 0 and hours < 0:
            result += 'меньше часа'
    return result
