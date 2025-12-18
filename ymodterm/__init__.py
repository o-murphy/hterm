from importlib.metadata import metadata

try:
    __version__ = metadata("ymodterm")["Version"]
except Exception:
    __version__ = "unknown"
