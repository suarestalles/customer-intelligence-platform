from datetime import date, datetime


def format_number(value: int | float) -> str:
    return f"{value:,.0f}".replace(",", ".")


def format_decimal(value: int | float, decimals: int = 2) -> str:
    formatted = f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return formatted


def format_currency(value: int | float) -> str:
    return f"R$ {format_decimal(value)}"


def format_compact_currency(value: int | float) -> str:
    if abs(value) > 1_000_000:
        return f"R$ {value / 1_000_000:.2f} mi"
    if abs(value) >= 1_000:
        return f"R$ {value / 1_000:.2f} mil"

    return format_currency(value)


def format_date(value: date | datetime | str | None) -> str:
    if value is None:
        return "-"
    if isinstance(value, datetime | date):
        return value.strftime("%d/%m/%Y")
    if isinstance(value, str):
        try:
            parsed_value = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return parsed_value.strftime("%d/%m/%Y")
        except ValueError:
            return value
    return str(value)


def format_datetime(value: datetime | str | None) -> str:
    if value is None:
        return "-"
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y %H:%M")
    if isinstance(value, str):
        try:
            parsed_value = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return parsed_value.strftime("%d/%m/%Y %H:%M")
        except ValueError:
            return value
    return str(value)
