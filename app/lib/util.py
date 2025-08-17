from urllib.parse import urlparse, unquote

def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))


def get_path(url: str | None) -> str:
    if (url is None) or (url == ""):
        return url
    # Handle scheme-less hosts without breaking absolute paths
    needs_host_hint = not (url.startswith('/') or '://' in url or url.startswith('//'))
    to_parse = f"//{url}" if needs_host_hint else url
    path = urlparse(to_parse).path
    return unquote(path or '/')