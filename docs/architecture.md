# Architecture

`weav-ai-providers` is the provider facade in the WeavInt AI package split. It gives runtime packages a stable place to build provider clients and list provider capabilities without importing server code.

## Design Goals

- Keep provider construction separate from tenant and server infrastructure.
- Expose a small stable API for downstream runtime assembly.
- Delegate provider-specific implementation details to `weav_provider_router`.
- Keep imports lightweight by loading provider-router modules lazily.

## Dependency Direction

The intended dependency direction is:

```text
weav-ai-core
  -> weav-ai-providers
    -> weav-ai-runtime
      -> weav-server-ai-adapter
```

`weav-ai-providers` may depend on `weav-ai-core`, but it should not import downstream runtime or server packages.

Do not add dependencies on:

- tenant credential stores
- SQLModel or database sessions
- server model tables
- usage accounting services
- product-specific model selection policy

Those responsibilities belong above this package.

## Runtime Boundary

This package answers provider-level questions:

- How do I build a provider client for a provider name?
- How do I ask a provider for available model names?
- How do I build image provider clients and configs?
- Which image provider names are installed?

It does not answer product-level questions:

- Which tenant is making the request?
- Which API key should be used?
- Which model should be selected by default?
- How should usage be recorded?
- How should failures be reported to end users?

## Lazy Import Strategy

Factory functions import `weav_provider_router` inside each function instead of at module import time. This has two benefits:

- importing `weav_ai_providers` does not require every provider backend to be installed
- tests can mock provider-router modules and validate facade behavior quickly

The tradeoff is that missing provider-router dependencies fail when a factory function is called. Callers should treat provider construction as an operation that can fail and surface useful diagnostics.

## Error Handling Guidance

This package intentionally does not catch broad provider construction errors. Provider failures often contain useful configuration or dependency information and should be handled by the runtime or application layer that knows the tenant and request context.

Recommended downstream pattern:

```python
try:
    provider = build_provider(provider_name, **credentials)
except Exception as exc:
    # Log with provider name and request context in the runtime layer.
    raise
```

## Testing Strategy

The tests mock `weav_provider_router` modules and validate that:

- `build_provider()` delegates provider name and keyword arguments
- `list_models()` filters empty and non-string values
- image provider helpers delegate correctly

Future integration tests can be added in a higher-level package that installs real provider backends and credentials.

## Release Considerations

This package currently depends on `weav-ai-core` through a direct Git reference. Hatchling requires `tool.hatch.metadata.allow-direct-references = true` for this.

Before a stable release, prefer pinning `weav-ai-core` to a tag or published package version so builds are reproducible.
