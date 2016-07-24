import logging

_logger = None


def _log(level, message, *args, **kwargs):
    """Log into the internal pete logger."""
    global _logger
    if _logger is None:
        _logger = logging.getLogger('pete')
        # Only set up a default log handler if the
        # end-user application didn't set anything up.
        if not logging.root.handlers and _logger.level == logging.NOTSET:
            _logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(name)s - %(levelname)s - %(asctime)s - %(message)s")
            handler.setFormatter(formatter)
            _logger.addHandler(handler)
    _logger.log(logging.getLevelName(level.upper()), message, *args, **kwargs)
