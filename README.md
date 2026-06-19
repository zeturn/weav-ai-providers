# weav-ai-providers

Provider adapter package for WeavInt AI.

`weav-ai-providers` centralizes provider construction, model listing, and image provider access behind a small facade. It delegates to the installed `weav_provider_router` package at call time.

## When to Use This Package

Use `weav-ai-providers` when you need to construct provider clients or list provider models without importing product-specific runtime or server code.

This package is responsible for:

- building chat providers by provider name
- listing model names from a provider
- building image providers
- creating image provider configuration objects
- listing installed image provider implementations

It is not responsible for tenant lookup, API key storage, model selection policy, usage recording, or database access. Those responsibilities belong in `weav-ai-runtime` and server adapters.

## Package Relationship

The AI packages are intended to be consumed in this order:

1. `weav-ai-core` provides shared primitives and compatibility imports.
2. `weav-ai-providers` exposes provider construction and model discovery.
3. `weav-ai-runtime` assembles credentials, model catalog, routing, and usage contracts.
4. `weav-server-ai-adapter` connects the reusable runtime to `weav_server` infrastructure.

`weav-ai-providers` depends on `weav-ai-core`, but it should not depend on `weav-ai-runtime` or `weav_server`.

## Public API Overview

```python
from weav_ai_providers import (
    build_provider,
    list_models,
    build_image_provider,
    make_image_config,
    list_image_providers,
)
```

The functions lazily import `weav_provider_router` when called. This keeps module import lightweight and lets tests validate the facade without provider backends installed.

See [docs/api-reference.md](docs/api-reference.md) for function-level details and examples.

## Architecture

This package is a facade over provider-router behavior. It provides a stable package name and small API surface for downstream runtime assembly while the provider implementation can continue to evolve behind the boundary.

See [docs/architecture.md](docs/architecture.md) for boundaries, dependency direction, and operational notes.

## Installation

Install from the current main branch:

```bash
python -m pip install git+https://github.com/zeturn/weav-ai-providers.git@main
```

For local development:

```bash
python -m pip install -e ".[dev]"
```

For package-shell validation without installing migration-time upstream dependencies:

```bash
python -m pip install -e . --no-deps
```

`weav_provider_router` is imported lazily by the factory functions. Install the provider-router package and any provider-specific dependencies in environments that call the factory functions for real provider clients.

## Quick Start

```python
from weav_ai_providers import build_provider, list_models

provider = build_provider("openai", api_key="...")
models = list_models("openai", api_key="...")
```

Image provider usage:

```python
from weav_ai_providers import build_image_provider, make_image_config

config = make_image_config(size="1024x1024")
image_provider = build_image_provider("dalle", api_key="...")
```

## Development

Run the local quality checks:

```bash
python -m pytest
python -m build --wheel
```

The test suite mocks `weav_provider_router` so the facade can be validated without real provider packages or external credentials.

## Release Notes

This package is currently in migration bootstrap status. Before cutting a production release, pin `weav-ai-core` to a tag or published package version instead of tracking `main`.

Recommended release order:

1. release `weav-ai-core`
2. update this package to depend on the released core version
3. release `weav-ai-providers`
4. update downstream runtime packages to consume the released provider package

## Governance

- Security reporting: see [SECURITY.md](SECURITY.md)
- Contribution workflow: see [CONTRIBUTING.md](CONTRIBUTING.md)
- License: Apache-2.0, see [LICENSE](LICENSE)
