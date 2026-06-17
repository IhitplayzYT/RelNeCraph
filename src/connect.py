from typing import Optional
import requests
from consts import DEFAULT_ENDPOINT,DEFAULT_MODEL,DEFAULT_TIMEOUT

class ModelSocket:
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        host: str = DEFAULT_ENDPOINT,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self.model = model
        self.host = host.rstrip("/")
        self.timeout = timeout

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature,
            },
        }

        if system is not None:
            payload["system"] = system

        response = requests.post(
            f"{self.host}/api/generate",
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        return data["response"]

    def stream(self, prompt: str):
        response = requests.post(
            f"{self.host}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": True,
            },
            stream=True,
        )

        response.raise_for_status()

        for line in response.iter_lines():
            if not line:
                continue

            chunk = json.loads(line)

            yield chunk["response"]

            if chunk.get("done", False):
                break

# Manual index into ["content"] returned value for getting response text
    def chat(
        self,
        messages: list[dict],
        temperature: float = 0.7,
    ) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }

        response = requests.post(
            f"{self.host}/api/chat",
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        return data["message"] 