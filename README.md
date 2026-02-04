# YODA Framework Package

## What this package is
This package embeds the YODA Framework inside a host project. It includes the agent manual, scripts, templates, and metadata you need to run YODA in that repo.

## How to use
### Quick install (one-liner)
This is the fastest path, but it executes a remote script directly. Use it only if you trust the source.

<!-- TODO: define base URL for installer script and metadata hosting (yoda-install.sh, latest.json). -->
```bash
curl -fsSL <url>/yoda-install.sh | sh -s -- --version <semver+build> --root .
```

Safety tips:
- Pin an explicit `--version`.
- Review the script if you are in a regulated environment.
- The installer must verify the tarball checksum from `latest.json`.

### Manual install (recommended)
1) Download `yoda-framework-<semver+build>.tar.gz` and `latest.json`.
2) Verify the `sha256` from `latest.json` matches the tarball.
3) Extract the package:
```bash
tar -xzf yoda-framework-<semver+build>.tar.gz -C <target>
```
4) Copy the `yoda/` subtree into the project root (preserve `yoda/todos/`, `yoda/logs/`, `yoda/project/issues/`).
5) Run init:
```bash
python yoda/scripts/init.py --dev <slug> --root .
```

## What's inside
- `yoda/yoda.md` (agent manual)
- `yoda/scripts/` (CLI tools)
- `yoda/templates/` (issue templates)
- `yoda/PACKAGE_MANIFEST.yaml` (build metadata)
- `yoda/CHANGELOG.yaml` (release history)
- `yoda/LICENSE` (embedded license)

## Version/build info
Check `yoda/PACKAGE_MANIFEST.yaml` for the exact version/build and `yoda/CHANGELOG.yaml` for release notes.

## Where to read more
- `yoda/yoda.md` for the embedded manual
- `yoda/scripts/README.md` for script usage
