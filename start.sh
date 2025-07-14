#!/bin/bash

# Optional: download model if not exists
if [ ! -d "stanza_models" ]; then
  echo "Downloading Stanza Hindi model..."
  python3 -c "import stanza; stanza.download('hi', dir='stanza_models')"
fi

exec uvicorn main:app --host 0.0.0.0 --port=${PORT:-8080}
