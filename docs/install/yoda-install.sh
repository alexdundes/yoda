#!/bin/sh
set -eu
if (set -o pipefail) 2>/dev/null; then
  set -o pipefail
fi

BASE_URL="https://alexdundes.github.io/yoda"
LATEST_URL="$BASE_URL/install/latest.json"

ROOT="."
VERSION=""
SOURCE=""
DEV=""
DRY_RUN=0

usage() {
  cat <<'USAGE'
Usage: yoda-install.sh [--version <semver+build>] [--root <path>] [--source <url|path>] [--dev <slug>] [--dry-run]

Options:
  --version   Expected version (defaults to latest.json version+build).
  --root      Project root to install into (default: current directory).
  --source    Override package_url with a URL or local tar.gz path.
  --dev       Developer slug to run init after install.
  --dry-run   Show planned actions without writing to the project root.
USAGE
}

log() {
  printf '%s\n' "$*"
}

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

require_arg() {
  if [ -z "${2-}" ]; then
    fail "Missing value for $1"
  fi
}

have_cmd() {
  command -v "$1" >/dev/null 2>&1
}

fetch_url() {
  url="$1"
  out="$2"
  if have_cmd curl; then
    curl -fsSL "$url" -o "$out"
  elif have_cmd wget; then
    wget -qO "$out" "$url"
  else
    fail "curl or wget is required to download $url"
  fi
}

normalize_sha() {
  printf '%s' "$1" | tr 'A-F' 'a-f'
}

calc_sha256() {
  file="$1"
  if have_cmd sha256sum; then
    sha256sum "$file" | awk '{print $1}'
  elif have_cmd shasum; then
    shasum -a 256 "$file" | awk '{print $1}'
  else
    fail "sha256sum or shasum is required to verify checksums"
  fi
}

is_url() {
  case "$1" in
    http://*|https://*|file://*)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

while [ $# -gt 0 ]; do
  case "$1" in
    --version)
      require_arg "$1" "${2-}"
      VERSION="$2"
      shift 2
      ;;
    --root)
      require_arg "$1" "${2-}"
      ROOT="$2"
      shift 2
      ;;
    --source)
      require_arg "$1" "${2-}"
      SOURCE="$2"
      shift 2
      ;;
    --dev)
      require_arg "$1" "${2-}"
      DEV="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    *)
      fail "Unknown option: $1"
      ;;
  esac
done

if [ ! -d "$ROOT" ]; then
  fail "Root directory not found: $ROOT"
fi

ROOT=$(cd "$ROOT" && pwd)

if ! have_cmd python3; then
  fail "python3 is required to parse latest.json and run init"
fi

if ! have_cmd tar; then
  fail "tar is required to extract the package"
fi

log "WARNING: This installer executes a remote script. Prefer the manual flow for production."
log "INFO: Using metadata from $LATEST_URL"

TMP_DIR=$(mktemp -d 2>/dev/null || mktemp -d -t yoda-install)

cleanup() {
  if [ -n "${TMP_DIR-}" ] && [ -d "$TMP_DIR" ]; then
    rm -rf "$TMP_DIR"
  fi
}
trap cleanup EXIT INT TERM

LATEST_JSON="$TMP_DIR/latest.json"
fetch_url "$LATEST_URL" "$LATEST_JSON"

LATEST_VERSION=$(python3 - "$LATEST_JSON" <<'PY'
import json,sys
with open(sys.argv[1]) as f:
    data=json.load(f)
print(data.get("version", ""))
PY
)
LATEST_BUILD=$(python3 - "$LATEST_JSON" <<'PY'
import json,sys
with open(sys.argv[1]) as f:
    data=json.load(f)
print(data.get("build", ""))
PY
)
LATEST_PACKAGE_URL=$(python3 - "$LATEST_JSON" <<'PY'
import json,sys
with open(sys.argv[1]) as f:
    data=json.load(f)
print(data.get("package_url", ""))
PY
)
LATEST_SHA256=$(python3 - "$LATEST_JSON" <<'PY'
import json,sys
with open(sys.argv[1]) as f:
    data=json.load(f)
print(data.get("sha256", ""))
PY
)

if [ -z "$LATEST_VERSION" ] || [ -z "$LATEST_PACKAGE_URL" ] || [ -z "$LATEST_SHA256" ]; then
  fail "latest.json is missing required fields"
fi

if [ -n "$LATEST_BUILD" ]; then
  LATEST_FULL="$LATEST_VERSION+$LATEST_BUILD"
else
  LATEST_FULL="$LATEST_VERSION"
fi

if [ -z "$VERSION" ]; then
  VERSION="$LATEST_FULL"
elif [ "$VERSION" != "$LATEST_FULL" ]; then
  fail "Requested version '$VERSION' does not match latest.json '$LATEST_FULL'"
fi

if [ -n "$SOURCE" ]; then
  PACKAGE_SOURCE="$SOURCE"
else
  PACKAGE_SOURCE="$LATEST_PACKAGE_URL"
fi

if [ "$DRY_RUN" -eq 1 ]; then
  log "DRY RUN: Would download package from $PACKAGE_SOURCE"
  log "DRY RUN: Would verify sha256 $LATEST_SHA256"
  log "DRY RUN: Would extract and install into $ROOT"
  log "DRY RUN: Would preserve yoda/todos, yoda/logs, yoda/project/issues"
  if [ -n "$DEV" ]; then
    log "DRY RUN: Would run init: python3 yoda/scripts/init.py --dev $DEV --root $ROOT"
  else
    log "DRY RUN: Skipping init (no --dev provided)"
  fi
  exit 0
fi

TARBALL="$TMP_DIR/yoda-framework.tar.gz"

if [ -f "$PACKAGE_SOURCE" ]; then
  cp "$PACKAGE_SOURCE" "$TARBALL"
elif is_url "$PACKAGE_SOURCE"; then
  fetch_url "$PACKAGE_SOURCE" "$TARBALL"
else
  fail "--source is not a file or URL: $PACKAGE_SOURCE"
fi

EXPECTED_SHA256=$(normalize_sha "$LATEST_SHA256")
ACTUAL_SHA256=$(calc_sha256 "$TARBALL")

if [ "$EXPECTED_SHA256" != "$ACTUAL_SHA256" ]; then
  fail "Checksum mismatch. Expected $EXPECTED_SHA256, got $ACTUAL_SHA256"
fi

EXTRACT_DIR="$TMP_DIR/extract"
mkdir -p "$EXTRACT_DIR"

tar -xzf "$TARBALL" -C "$EXTRACT_DIR"

SRC_YODA="$EXTRACT_DIR/yoda"
DEST_YODA="$ROOT/yoda"

if [ ! -d "$SRC_YODA" ]; then
  fail "Package does not contain a yoda/ directory"
fi

mkdir -p "$DEST_YODA"

copy_entry() {
  src="$1"
  dest="$2"
  rm -rf "$dest"
  if [ -d "$src" ]; then
    cp -R "$src" "$dest"
  else
    cp "$src" "$dest"
  fi
}

copy_project() {
  src_project="$1"
  dest_project="$DEST_YODA/project"
  mkdir -p "$dest_project"
  for sub in "$src_project"/*; do
    [ -e "$sub" ] || continue
    sub_name=$(basename "$sub")
    if [ "$sub_name" = "issues" ]; then
      continue
    fi
    copy_entry "$sub" "$dest_project/$sub_name"
  done
}

for entry in "$SRC_YODA"/*; do
  [ -e "$entry" ] || continue
  name=$(basename "$entry")
  case "$name" in
    todos|logs)
      continue
      ;;
    project)
      copy_project "$entry"
      ;;
    *)
      copy_entry "$entry" "$DEST_YODA/$name"
      ;;
  esac
done

log "INFO: Installed YODA framework files under $DEST_YODA"
log "INFO: Preserved yoda/todos, yoda/logs, yoda/project/issues"

if [ -n "$DEV" ]; then
  python3 "$DEST_YODA/scripts/init.py" --dev "$DEV" --root "$ROOT"
else
  log "INFO: Skipping init (no --dev provided)"
fi

log "Install complete: YODA $VERSION installed at $ROOT"
