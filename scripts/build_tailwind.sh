#!/usr/bin/env bash
# scripts/build_tailwind.sh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

# Minimal package.json and tailwind build if not present
if [ ! -f package.json ]; then
  cat > package.json <<'JSON'
{
  "name": "mega-tool-frontend",
  "version": "0.0.1",
  "private": true,
  "devDependencies": {
    "tailwindcss": "^4.0.0",
    "postcss": "^8.0.0",
    "autoprefixer": "^10.0.0"
  },
  "scripts": {
    "build:css": "tailwindcss -i ./frontend/tailwind.input.css -o ./static/css/tailwind.css --minify"
  }
}
JSON
  echo "Created package.json for Tailwind build"
fi

mkdir -p frontend
# Create a tiny tailwind input if not present
if [ ! -f frontend/tailwind.input.css ]; then
  cat > frontend/tailwind.input.css <<'CSS'
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Add project-specific styles here */
CSS
  echo "Created frontend/tailwind.input.css"
fi

echo "Now run:"
echo "  npm install"
echo "  npm run build:css"
echo
echo "(If you prefer not to use npm, keep the placeholder static/css/tailwind.css file.)"
