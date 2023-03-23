import os

required_env_vars = {
    "OPENAI_API_KEY": None,
    "GCLOUD_KEY_PATH": None,
    "VOICEVOX_API_URL": None,
}

for var_name in required_env_vars:
    value = os.environ.get(var_name)
    if value is None:
        raise ValueError(f"{var_name} environment variable is not set.")
    else:
        required_env_vars[var_name] = value

OPENAI_API_KEY = required_env_vars["OPENAI_API_KEY"]
GCLOUD_KEY_PATH = required_env_vars["GCLOUD_KEY_PATH"]
VOICEVOX_API_URL = required_env_vars["VOICEVOX_API_URL"]

SPEAKER_ID = int(os.environ.get("SPEAKER_ID", "0"))

