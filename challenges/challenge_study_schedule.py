def study_schedule(permanence_period, target_time):
    try:
        dictPeriods = 0
        for period in permanence_period:
            if period[0] <= target_time <= period[1]:
                dictPeriods += 1
    except (IndexError, TypeError):
        return None
    return dictPeriods
