def format_timestamp(value, fmt="%b %d, %Y - %H:%M"):
    """Custom template filter tool processing clean datestamps inside system layout contexts."""
    if not value:
        return ""
    return value.strftime(fmt)

def register_utils(app):
    app.jinja_env.filters['datetime_format'] = format_timestamp
