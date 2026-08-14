import os

# Render sets the PORT environment variable. Default to 10000 (Render's
# standard port for web services) if not set (e.g. local dev).
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"

# Single worker: the spaCy model is loaded once into one process.
# Multiple workers would each load a copy, immediately exhausting the
# 512 MB RAM available on Render's free tier.
workers = 1

# 2-minute timeout: large DOCX files can take 30-90 seconds to redact.
timeout = 120
