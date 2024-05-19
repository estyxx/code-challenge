from .base import *  # noqa: F403

# SECRET_KEY is required by Django to start.
SECRET_KEY = "fake_secret_key_to_run_tests"  # pragma: allowlist secret

# Allow all hosts in tests.
ALLOWED_HOSTS = ["*"]
