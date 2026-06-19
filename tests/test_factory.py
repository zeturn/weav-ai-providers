import sys
import types

from weav_ai_providers import (
    build_image_provider,
    build_provider,
    list_image_providers,
    list_models,
    make_image_config,
)


def install_provider_router_stubs(monkeypatch):
    root = types.ModuleType("weav_provider_router")
    root.__path__ = []

    class ImageConfig:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    root.ImageConfig = ImageConfig
    root.IMAGE_PROVIDER_CLASSES = {"dalle": object, "stability": object}
    root.build_image_provider = lambda **kwargs: {"image_provider": kwargs}

    providers = types.ModuleType("weav_provider_router.providers")
    providers.build_provider = lambda provider, **kwargs: {"provider": provider, "kwargs": kwargs}

    api = types.ModuleType("weav_provider_router.api")
    api.list_models = lambda provider, **kwargs: ["gpt-4o", "", None, "claude-3-5"]

    monkeypatch.setitem(sys.modules, "weav_provider_router", root)
    monkeypatch.setitem(sys.modules, "weav_provider_router.providers", providers)
    monkeypatch.setitem(sys.modules, "weav_provider_router.api", api)


def test_build_provider_delegates_to_router(monkeypatch):
    install_provider_router_stubs(monkeypatch)

    provider = build_provider("openai", api_key="test-key")

    assert provider == {"provider": "openai", "kwargs": {"api_key": "test-key"}}


def test_list_models_returns_non_empty_string_models(monkeypatch):
    install_provider_router_stubs(monkeypatch)

    assert list_models("openai") == ["gpt-4o", "claude-3-5"]


def test_image_provider_facade(monkeypatch):
    install_provider_router_stubs(monkeypatch)

    config = make_image_config(size="1024x1024")
    provider = build_image_provider("dalle", api_key="test-key")

    assert config.kwargs == {"size": "1024x1024"}
    assert provider == {"image_provider": {"provider": "dalle", "api_key": "test-key"}}
    assert list_image_providers() == ["dalle", "stability"]
