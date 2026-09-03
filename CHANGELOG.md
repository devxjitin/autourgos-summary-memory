# Changelog

## [2.0.5] - 2026-09-03

- Added `features.md` documenting the module's feature set and a competitor comparison. No code changes.


## [2.0.4] - 2026-09-01

- Metadata: added `maintainers` (Sonia, Vishwanil Suman) to `pyproject.toml`,
  and linked the README's existing Sonia contributor badge to her GitHub
  profile (https://github.com/dahiyasonia). No code changes.

## [2.0.3] - 2026-09-01

- Fixed: `_update_summary()` used to bake the literal string `"None"` into
  `moving_summary` permanently if `llm.invoke()` returned `None` (or an
  empty string) — `str(None) == "None"`. Now falls back to raw
  concatenation on a `None`/empty response, same as any other
  unusable/failed response.

## [2.0.1] - 2026-07-27

- Docs: fixed the undefined my_llm placeholder in the Quick Start example.

All notable changes to `autourgos-summary-memory` are documented here.

---

## [2.0.0] - 2026-07-27

### Changed
- BREAKING: this package now depends on `autourgos-memory>=1.0.1` (previously zero-dependency). `BaseMemory`/`BaseRetriever`/`Document`/`MemoryMessage` are now re-exported from `autourgos-memory` instead of duplicated locally. No public API/behavior change for typical usage.

## [1.0.1] - 2026-07-27

### Fixed
- `__version__` fallback in `__init__.py` now matches `pyproject.toml` (was incorrectly `1.0.2`, now `1.0.0`).
- Wording correction: CHANGELOG previously referenced a non-existent `autourgos-core` package; now correctly states there is no dependency on `autourgos-memory` or any other Autourgos package.

## [1.0.0] - 2026-06-17

### Added
- Initial release.
- LLM-compressed rolling summary memory.
- Self-contained package — no dependency on `autourgos-memory` or any other Autourgos package.
- All base interfaces (`BaseMemory`, `BaseRetriever`, `MemoryMessage`, `Document`) inlined.
- Thread-safe implementation using `threading.RLock`.
- Full type annotations and `py.typed` marker.

