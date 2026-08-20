import os

bind = "0.0.0.0:" + os.environ.get("PORT", "7860")
workers = 1
threads = 2
timeout = 120
preload_app = True
