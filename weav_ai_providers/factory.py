from __future__ import annotations

from typing import Any


def build_provider(provider: str, **kwargs: Any) -> Any:
    """Build a chat provider by name using the installed provider-router."""
    from weav_provider_router.providers import build_provider as _build_provider

    return _build_provider(provider, **kwargs)


def list_models(provider: str, **kwargs: Any) -> list[str]:
    """List model names for a provider using the installed provider-router."""
    from weav_provider_router.api import list_models as _list_models

    models = _list_models(provider, **kwargs)
    return [str(model) for model in models if isinstance(model, str) and model.strip()]


def build_image_provider(provider: str, **kwargs: Any) -> Any:
    """Build an image provider by name using the installed provider-router."""
    from weav_provider_router import build_image_provider as _build_image_provider

    return _build_image_provider(provider=provider, **kwargs)


def make_image_config(**kwargs: Any) -> Any:
    """Create an ImageConfig using the installed provider-router."""
    from weav_provider_router import ImageConfig

    return ImageConfig(**kwargs)


def list_image_providers() -> list[str]:
    """List installed image provider names."""
    from weav_provider_router import IMAGE_PROVIDER_CLASSES

    return list(IMAGE_PROVIDER_CLASSES.keys())
