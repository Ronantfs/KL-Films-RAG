from datetime import date, timedelta
import calendar


def _early_next_month(today: date) -> list[str]:
    year: int = today.year + (today.month == 12)
    month: int = 1 if today.month == 12 else today.month + 1
    days: list[str] = [date(year, month, d).isoformat() for d in range(1, 6)]
    return days


def _second_tuesday_next_month(today: date) -> list[str]:
    year: int = today.year + (today.month == 12)
    month: int = 1 if today.month == 12 else today.month + 1
    cal: list[list[int]] = calendar.monthcalendar(year, month)
    tuesdays: list[int] = [
        week[calendar.TUESDAY] for week in cal if week[calendar.TUESDAY] != 0
    ]
    result: list[str] = [date(year, month, tuesdays[1]).isoformat()]
    return result


def _around_end_of_next_month(today: date) -> list[str]:
    year: int = today.year + (today.month == 12)
    month: int = 1 if today.month == 12 else today.month + 1
    last_day: int = calendar.monthrange(year, month)[1]
    candidate_days: list[int] = [last_day - 1, last_day, last_day + 1]

    dates: list[str] = [
        date(year, month, d).isoformat() for d in candidate_days if 1 <= d <= last_day
    ]
    return dates


def _specific_month_day(today: date, month: int, day: int) -> list[str]:
    year: int = today.year
    candidate: date = date(year, month, day)

    if candidate < today:
        candidate = date(year + 1, month, day)

    result: list[str] = [candidate.isoformat()]
    return result


def _jan_28_or_next_monday(today: date) -> list[str]:
    dates: set[str] = set(_specific_month_day(today, 1, 28))

    weekday: int = today.weekday()
    next_monday: date = today + timedelta(days=(7 - weekday))
    dates.add(next_monday.isoformat())

    result: list[str] = sorted(dates)
    return result


def _last_friday_of_february(today: date) -> list[str]:
    year: int = today.year
    feb_first: date = date(year, 2, 1)

    if today > feb_first:
        year += 1

    cal: list[list[int]] = calendar.monthcalendar(year, 2)
    fridays: list[int] = [
        week[calendar.FRIDAY] for week in cal if week[calendar.FRIDAY] != 0
    ]

    result: list[str] = [date(year, 2, fridays[-1]).isoformat()]
    return result


def _next_week_and_a_half(today: date) -> list[str]:
    start: date = today + timedelta(days=1)
    dates: list[str] = [(start + timedelta(days=i)).isoformat() for i in range(10)]
    return dates


def _between_10th_and_15th_next_month(today: date) -> list[str]:
    year: int = today.year + (today.month == 12)
    month: int = 1 if today.month == 12 else today.month + 1
    dates: list[str] = [date(year, month, d).isoformat() for d in range(10, 16)]
    return dates


def _third_weekend_next_month(today: date) -> list[str]:
    year: int = today.year + (today.month == 12)
    month: int = 1 if today.month == 12 else today.month + 1

    cal: list[list[int]] = calendar.monthcalendar(year, month)
    weekends: list[tuple[int, int, int]] = [
        (
            week[calendar.FRIDAY],
            week[calendar.SATURDAY],
            week[calendar.SUNDAY],
        )
        for week in cal
        if week[calendar.FRIDAY] and week[calendar.SATURDAY] and week[calendar.SUNDAY]
    ]

    friday: int
    saturday: int
    sunday: int
    friday, saturday, sunday = weekends[2]

    result: list[str] = [
        date(year, month, friday).isoformat(),
        date(year, month, saturday).isoformat(),
        date(year, month, sunday).isoformat(),
    ]
    return result


def _next_monday_tuesday_or_friday(today: date) -> list[str]:
    targets: set[int] = {
        calendar.MONDAY,
        calendar.TUESDAY,
        calendar.FRIDAY,
    }

    results: list[str] = []
    for offset in range(1, 8):
        candidate: date = today + timedelta(days=offset)
        if candidate.weekday() in targets:
            results.append(candidate.isoformat())

    return results


def _this_weekend_example(today: date) -> list[str]:
    weekday: int = today.weekday()  # Monday=0
    friday: date = today + timedelta(days=(4 - weekday) % 7)
    saturday: date = friday + timedelta(days=1)
    sunday: date = friday + timedelta(days=2)

    result: list[str] = [
        friday.isoformat(),
        saturday.isoformat(),
        sunday.isoformat(),
    ]
    return result


def _next_week_example(ref: date) -> list[str]:
    weekday: int = ref.weekday()
    next_monday: date = ref + timedelta(days=(7 - weekday))
    dates: list[str] = [(next_monday + timedelta(days=i)).isoformat() for i in range(7)]
    return dates


def build_system_prompt(today: date) -> str:
    examples = [
        ("today", [today.isoformat()]),
        ("this weekend", _this_weekend_example(today)),
        ("next week", _next_week_example(today)),
        ("early next month", _early_next_month(today)),
        ("the second Tuesday of next month", _second_tuesday_next_month(today)),
        ("around the end of next month", _around_end_of_next_month(today)),
        ("March 3rd", _specific_month_day(today, 3, 3)),
        ("Jan 28th or next monday", _jan_28_or_next_monday(today)),
        ("the last Friday of February", _last_friday_of_february(today)),
        ("over the next week and a half", _next_week_and_a_half(today)),
        (
            "between the 10th and the 15th of next month",
            _between_10th_and_15th_next_month(today),
        ),
        ("the third weekend of next month", _third_weekend_next_month(today)),
        ("next monday, tuesday or friday", _next_monday_tuesday_or_friday(today)),
    ]

    example_blocks: list[str] = []
    for nat_lang_date_text, dates_list in examples:
        example_blocks.append(
            f"""User: "{nat_lang_date_text}"
                Output:
                {{"dates": {dates_list}}}"""
        )

    system_prompt: str = (
        f"""
        For a given users date natural language date expression,
        You must return JSON with exactly one key:
        "dates": a list of ISO-8601 dates (YYYY-MM-DD)

        Rules:
        - Include every date implied by the expression.
        - If the expression refers to a range, enumerate all dates in the range.
        - Do not include dates outside the implied range.
        - NOTE: references to the weekend should include friday, saturday and sunday.

        Some Guiding examples for what list of dates you would form from some natural language date expressions:

        {chr(10).join(example_blocks)}
        """.strip()
    )

    return system_prompt


def validate_dates(data: dict):
    # --- deterministic validation ---
    assert isinstance(data, dict)
    assert set(data.keys()) == {"dates"}
    assert isinstance(data["dates"], list)
    assert len(data["dates"]) > 0

    for d in data["dates"]:
        assert isinstance(d, str)
        assert len(d) == 10  # YYYY-MM-DD
        assert d[0:4].isdigit()
        assert d[5:7].isdigit()
        assert d[8:10].isdigit()
        assert d[4] == "-" and d[7] == "-"
