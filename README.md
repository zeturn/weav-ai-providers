# weav-ai-providers

Provider adapter package for WeavInt AI.

`weav-ai-providers` centralizes provider construction, model listing, and image provider access behind a small facade. It delegates to the installed `weav_provider_router` package at call time.

## Scope

This package exposes:

- `build_provider()` for chat provider construction
- `list_models()` for provider model discovery
- `build_image_provider()` and `make_image_config()` for image provider integration
- `list_image_providers()` for installed image provider names

## Package Relationship

The AI packages are intended to be consumed in this order:

1. `weav-ai-core` provides shared primitives and compatibility imports.
2. `weav-ai-providers` exposes provider construction and model discovery.
3. `weav-ai-runtime` assembles credentials, model catalog, routing, and usage contracts.
4. `weav-server-ai-adapter` connects the reusable runtime to `weav_server` infrastructure.

## Installation

```bash
python -m pip install git+https://github.com/zeturn/weav-ai-providers.git@main
```

For local development:

```bash
python -m pip install -e ".[dev]" --no-deps
```

`weav_provider_router` is imported lazily by the factory functions, so tests can validate the facade without installing provider backends.

## Usage

```python
from weav_ai_providers import build_provider, list_models

provider = build_provider("openai", api_key="...")
models = list_models("openai", api_key="...")
```

## Development

Run the local quality checks:

```bash
python -m pytest
python -m build --wheel
```

## Release Notes

This package is currently in migration bootstrap status. Before cutting a production release, pin `weav-ai-core` to a tag or published package version instead of tracking `main`.
