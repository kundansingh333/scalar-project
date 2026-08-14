# gunicorn.conf.py
# Applied automatically when gunicorn is started without an explicit config flag.
# On Render's free tier (512 MB RAM) a single worker keeps the spaCy model
# loaded in memory exactly once.  The 120-second timeout gives the redaction
# pipeline enough headroom to process a large DOCX without Render killing the
# worker mid-request.

workers = 1
timeout = 120
bind = "0.0.0.0:8000"
