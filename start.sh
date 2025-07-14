# #!/bin/bash

# uvicorn main:app --host 0.0.0.0 --port 10000

#!/bin/bash
# Download Hindi Stanza model before starting the app
python3 -c "import stanza; stanza.download('hi')"

# Start FastAPI app using Uvicorn
uvicorn main:app --host 0.0.0.0 --port 10000


