#!/usr/bin/env bash
set -euo pipefail

# Reproducible CPU-only whisper.cpp install for the AWS demo origin.
# Override with WHISPER_CPP_REF=<tag-or-commit> when intentionally testing another version.
WHISPER_CPP_REF="${WHISPER_CPP_REF:-v1.9.4}"
PREFIX="/opt/sinapuml/whisper"
BUILD_ROOT="$(mktemp -d /tmp/sinapuml-whisper.XXXXXX)"
trap 'rm -rf "$BUILD_ROOT"' EXIT

if [[ ${EUID} -ne 0 ]]; then
  echo "Run with sudo: sudo bash ./install-whisper.sh" >&2
  exit 1
fi

apt-get update
apt-get install -y --no-install-recommends \
  build-essential \
  ca-certificates \
  cmake \
  curl \
  git

if ! id sinapuml >/dev/null 2>&1; then
  useradd --system --home /opt/sinapuml --shell /usr/sbin/nologin sinapuml
fi

install -d -o sinapuml -g sinapuml "$PREFIX" "$PREFIX/models"

git clone --depth 1 --branch "$WHISPER_CPP_REF" \
  https://github.com/ggml-org/whisper.cpp.git \
  "$BUILD_ROOT/whisper.cpp"

cmake -S "$BUILD_ROOT/whisper.cpp" -B "$BUILD_ROOT/whisper.cpp/build" \
  -DCMAKE_BUILD_TYPE=Release \
  -DWHISPER_BUILD_EXAMPLES=ON
cmake --build "$BUILD_ROOT/whisper.cpp/build" \
  --config Release \
  --target whisper-server \
  --parallel 2

SERVER="$BUILD_ROOT/whisper.cpp/build/bin/whisper-server"
if [[ ! -x "$SERVER" ]]; then
  echo "whisper-server was not produced at the expected path: $SERVER" >&2
  exit 1
fi
install -o sinapuml -g sinapuml -m 0755 "$SERVER" "$PREFIX/whisper-server"

(
  cd "$BUILD_ROOT/whisper.cpp"
  bash ./models/download-ggml-model.sh base
)
MODEL="$BUILD_ROOT/whisper.cpp/models/ggml-base.bin"
if [[ ! -s "$MODEL" ]]; then
  echo "ggml-base.bin was not downloaded." >&2
  exit 1
fi
install -o sinapuml -g sinapuml -m 0644 "$MODEL" "$PREFIX/models/ggml-base.bin"

if systemctl list-unit-files sinapuml-whisper.service >/dev/null 2>&1; then
  systemctl restart sinapuml-whisper.service || true
fi

cat <<MSG
whisper.cpp installed for SinapUML.
Version/ref: $WHISPER_CPP_REF
Binary:      $PREFIX/whisper-server
Model:       $PREFIX/models/ggml-base.bin
MSG
