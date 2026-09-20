#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [ -d "$ROOT/android" ] || [ -d "$ROOT/ios" ]; then
  echo "Native projects already exist; refusing to overwrite them."
  exit 1
fi
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
cd "$TMP"
npx @react-native-community/cli@latest init CodeReadyTutors --version 0.81.0 --skip-install
cp -R "$TMP/CodeReadyTutors/android" "$ROOT/android"
cp -R "$TMP/CodeReadyTutors/ios" "$ROOT/ios"
echo "Native React Native 0.81 projects generated. Run npm install, then npm run android."

# Generated native projects remain JavaScript-first; no TypeScript app code is introduced.
