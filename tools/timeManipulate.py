FORMAT_DATA = "%Y-%m-%d"


def weekday_sun_first(date):
    weekday = date.weekday()

    match weekday:
        case 6:
            return 1

        case _:
            return weekday + 2
