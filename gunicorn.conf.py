import os
import sys

# Python 3.12+ no longer guarantees '' (cwd) is in sys.path.
# Explicitly add the directory that contains this file (= project root)
# so that 'app' and 'redact_pii' are always importable.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Render sets PORT dynamically; default to 10000 (Render's standard web port)
bind = "0.0.0.0:{}".format(os.environ.get("PORT", "10000"))

# Single worker: spaCy model is loaded once at startup.
# Multiple workers would each load a copy → OOM on 512 MB free tier.
workers = 1

# 2-minute request timeout. Large documents can take 60–90 s to redact.
timeout = 120

keepalive = 5
