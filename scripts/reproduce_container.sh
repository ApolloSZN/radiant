#!/usr/bin/env bash
set -euo pipefail
# Clean-container reproduction. A passing receipt is written only after the
# image builds and the full Radiant reproduction succeeds inside that image.
IMAGE="radiant-reproduce:${RADIANT_IMAGE_TAG:-local}"
mkdir -p artifacts
docker build --pull -t "$IMAGE" .
# Run as the host user so files written into the mounted artifacts/ directory stay
# writable by later host-side CI steps (root-owned receipts caused EACCES).
docker run --rm --user "$(id -u):$(id -g)" \
  -e HOME=/tmp -e PYTHONDONTWRITEBYTECODE=1 -e PYTEST_ADDOPTS="-p no:cacheprovider" \
  -v "$PWD/artifacts:/app/artifacts" "$IMAGE"
python - <<'PY'
import json
from pathlib import Path
from radiant.source_fingerprint import fingerprint
Path('artifacts/container_reproduction_report.json').write_text(json.dumps({
  'schema':'radiant.container_reproduction.v1',
  'passed':True,
  'source_fingerprint':fingerprint('.'),
  'builder':'docker',
  'command':'docker build --pull ... && docker run --rm ...',
  'inner_receipt':'artifacts/reproduction_report.json'
},indent=2)+'\n')
PY
