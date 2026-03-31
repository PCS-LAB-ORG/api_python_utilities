import os
import yaml
from dotenv import load_dotenv


class CortexAuthManager:
    def __init__(self, config_file="cortex.env"):
        """
        Handles credentials and authentication headers for Cortex Cloud.
        Attempts to load from a .env file using dotenv, falling back to .yaml.
        """
        # 1. Load environment variables using python-dotenv
        if config_file.endswith(".env") or "env" in config_file:
            if os.path.exists(config_file):
                load_dotenv(dotenv_path=config_file)

        # 2. Extract credentials
        self.base_url = os.environ.get("CORTEX_API_BASE_URL")
        self.api_key_id = os.environ.get("CORTEX_API_KEY_ID")
        self.api_key = os.environ.get("CORTEX_API_KEY")

        # 3. Fallback to YAML if credentials aren't in the environment
        if not all(
            [self.base_url, self.api_key_id, self.api_key]
        ) and config_file.endswith((".yaml", ".yml")):
            self._load_credentials_from_yaml(config_file)

        # Final Validation
        if not all([self.base_url, self.api_key_id, self.api_key]):
            raise ValueError(
                "Credentials missing. Ensure CORTEX_API_BASE_URL, CORTEX_API_KEY_ID, and CORTEX_API_KEY are set."
            )

        # Ensure proper URL formatting
        if not self.base_url.startswith("http"):
            self.base_url = f"https://{self.base_url}"

    def _load_credentials_from_yaml(self, config_file: str):
        """Extract credentials from a .yaml configuration file."""
        if os.path.exists(config_file):
            with open(config_file) as f:
                config = yaml.safe_load(f) or {}
                self.base_url = self.base_url or config.get("CORTEX_API_BASE_URL")
                self.api_key_id = self.api_key_id or str(
                    config.get("CORTEX_API_KEY_ID", "")
                )
                self.api_key = self.api_key or config.get("CORTEX_API_KEY")

    def get_auth_headers(self):
        """Construct the required Advanced or Standard authentication headers."""
        return {
            "x-xdr-auth-id": self.api_key_id,
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }
