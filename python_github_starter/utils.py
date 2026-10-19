"""Small reusable validation helpers."""


def validate_title(title: str) -> str:
    if not isinstance(title, str):
        raise ValueError("Task title must be text.")
    clean_title = title.strip()
    if not clean_title:
        raise ValueError("Task title cannot be empty.")
    if len(clean_title) > 120:
        raise ValueError("Task title must be 120 characters or fewer.")
    return clean_title
