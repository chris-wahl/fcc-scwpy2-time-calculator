_dow_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
             'Saturday', 'Sunday']
_dow_order = {day: index for index, day in enumerate(_dow_list)}
_minutes_per_day = 1440

def add_time(start: str, duration: str, dow: str = None) -> str:
    # Decompose start time into hours/minutes on a 24 hour clock
    start_hours, start_minutes = start.split(':')

    if start_hours == '12' and 'AM' in start_minutes:
        start_hours = 0
    else:
        start_hours = int(start_hours) + (12 if 'PM' in start_minutes else 0)
    # Turn the entire start time into minutes from midnight.
    start_minutes = int(start_minutes[:2]) + start_hours * 60

    # Decompose the duration into hours and minutes
    duration_hours, duration_minutes = (int(x) for x in duration.split(':'))
    # and transform entirely into minutes.
    duration_minutes += duration_hours * 60

    # Get the new finish time
    finish_minutes = start_minutes + duration_minutes

    # Prepare add'l info strings.
    next_str = ''
    days_elapsed = int(finish_minutes / _minutes_per_day)
    if days_elapsed == 1:
        next_str = ' (next day)'
    elif days_elapsed > 1:
        next_str = f' ({days_elapsed} days later)'

    # If provided a start day-of-week, determine the finish day of the week
    # based on days_elapsed
    if dow is not None:
        dow = dow.title()
        idx = (_dow_order[dow] + days_elapsed) % 7
        new_dow = _dow_list[idx]
        next_str = f', {new_dow}{next_str}'

    # Transform the finsh minutes back into a clock-time
    finish_hours = int((finish_minutes % _minutes_per_day) / 60)
    finish_minutes = (finish_minutes % _minutes_per_day) - finish_hours * 60

    # Handle the edge-cast of 00:XX AM -> 12:XX AM
    output = '12' if finish_hours % 12 == 0 else finish_hours % 12
    output = f"{output}:{str(finish_minutes).rjust(2, '0')} "
    output += 'PM' if finish_hours >= 12 else 'AM'
    return (output + next_str) if next_str else output
