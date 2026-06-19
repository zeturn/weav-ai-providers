# API Reference

This document describes the public API exposed by `weav-ai-providers`.

```python
from weav_ai_providers import (
    build_provider,
    list_models,
    build_image_provider,
    make_image_config,
    list_image_providers,
)
```

All factory functions delegate to the installed `weav_provider_router` package.

## `build_provider(provider: str, **kwargs) -> Any`

Build a chat provider by name.

```python
from weav_ai_providers import build_provider

provider = build_provider("openai", api_key="sk-...")
```

Arguments:

| Name | Description |
| --- | --- |
| `provider` | Provider name understood by `weav_provider_router`. |
| `**kwargs` | Provider-specific construction options, such as `api_key` or `base_url`. |

Behavior:

- imports `weav_provider_router.providers.build_provider` lazily
- passes the provider name and keyword arguments through unchanged
- returns whatever provider-router returns
- lets provider-router errors propagate to the caller

## `list_models(provider: str, **kwargs) -> list[str]`

List model names for a provider.

```python
from weav_ai_providers import list_models

models = list_models("openai", api_key="sk-...")
```

Behavior:

- imports `weav_provider_router.api.list_models` lazily
- passes provider name and keyword arguments through to provider-router
- returns only non-empty string model names
- drops empty strings and non-string values from the provider-router result

This filtering makes downstream model catalogs easier to consume.

## `build_image_provider(provider: str, **kwargs) -> Any`

Build an image provider by name.

```python
from weav_ai_providers import build_image_provider

image_provider = build_image_provider("dalle", api_key="sk-...")
```

Behavior:

- imports `weav_provider_router.build_image_provider` lazily
- calls it with `provider=provider` plus keyword arguments
- returns whatever provider-router returns

## `make_image_config(**kwargs) -> Any`

Create an image configuration object from provider-router.

```python
from weav_ai_providers import make_image_config

config = make_image_config(size="1024x1024", quality="standard")
```

Behavior:

- imports `weav_provider_router.ImageConfig` lazily
- constructs and returns an `ImageConfig` instance
- passes keyword arguments through unchanged

## `list_image_providers() -> list[str]`

Return installed image provider names.

```python
from weav_ai_providers import list_image_providers

names = list_image_providers()
```

Behavior:

- imports `weav_provider_router.IMAGE_PROVIDER_CLASSES` lazily
- returns the dictionary keys as a list

## Error Handling

Provider-router import and construction failures are not swallowed by this package. Downstream runtime code should catch and log errors with request context when appropriate.

Example:

```python
from weav_ai_providers import build_provider

try:
    provider = build_provider("openai", api_key="sk-...")
except ImportError as exc:
    raise RuntimeError("Provider router is not installed") from exc
```

## Public API Rules

- New public functions must be added to `weav_ai_providers.__all__`.
- New public functions must be documented here.
- New public functions should have tests that mock provider-router delegation.
- Keep provider credentials and tenant policy out of this package.
