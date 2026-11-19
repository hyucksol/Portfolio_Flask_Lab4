def to_uppercase(text):
    """Gawing UPPERCASE ang text."""
    return (text or "").upper()


def handle(form):
    return {'uppercase_result': to_uppercase(form.get('text_input'))}