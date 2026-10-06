__version__ = "0.3.0"


def __getattr__(name):
    if name in ("PresentationBuilder", "build_from_spec"):
        from .builder import PresentationBuilder, build_from_spec
        return {"PresentationBuilder": PresentationBuilder,
                "build_from_spec": build_from_spec}[name]
    if name in ("Theme", "DEFAULT_THEME", "ZH_THEME", "make_zh_theme"):
        from . import theme
        return getattr(theme, name)
    raise AttributeError(name)
