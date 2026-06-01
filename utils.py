def is_valid_hex(text):
    text = text.strip()
    if not text:
        return False
    return all(c in "0123456789abcdefABCDEF" for c in text) and len(text) % 2 == 0


def truncate_display(text, max_len=200):
    if len(text) <= max_len:
        return text
    return text[:max_len] + f"... [{len(text) - max_len} more chars]"


def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def validate_text_input(text):
    if not text or not text.strip():
        return False, "Input text cannot be empty."
    return True, ""
