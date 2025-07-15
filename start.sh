#!/bin/bash

# Optional: Download Stanza model if not already present
if [ ! -d "stanza_models" ]; then
  echo "Downloading Stanza Hindi model..."
  python3 -c "import stanza; stanza.download('hi', dir='stanza_models')"
fi

# Start the FastAPI server on Cloud Run's expected port for deployment
exec uvicorn main:app --host 0.0.0.0 --port=${PORT:-8080}
