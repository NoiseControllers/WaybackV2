import random


def filter_per_year(snapshots: list, per_year: int) -> list:
    years = []
    temp = []
    results = []
    for snapshot in snapshots:
        time_stamp, status_code = snapshot
        year = time_stamp[0:4]
        if year not in years:
            years.append(year)

    for year in years:
        for snapshot in snapshots:
            time_stamp, status_code = snapshot
            if year == time_stamp[0:4]:
                temp.append(snapshot)

        for c in range(per_year):
            try:
                choice = random.choice(temp)
                results.append(choice)
                temp.remove(choice)
            except IndexError:
                continue
        temp.clear()

    return results
