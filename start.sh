# # #!/bin/bash

# # uvicorn main:app --host 0.0.0.0 --port 10000

# #!/bin/bash
# # Download Hindi Stanza model before starting the app
# python3 -c "import stanza; stanza.download('hi')"

# # Start FastAPI app using Uvicorn
# uvicorn main:app --host 0.0.0.0 --port 10000

#!/bin/bash

# Optional: Download Stanza model if not already present
if [ ! -d "stanza_models" ]; then
  echo "Downloading Stanza Hindi model..."
  python3 -c "import stanza; stanza.download('hi', dir='stanza_models')"
fi

# Start the FastAPI server on Cloud Run's expected port
exec uvicorn main:app --host 0.0.0.0 --port=${PORT:-8080}

