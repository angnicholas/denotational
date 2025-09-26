import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class ChatGPTClient:
    def __init__(self):
        """Initialize the ChatGPT client with API key from environment."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def upload_file(self, file_path: str, purpose: str = "assistants") -> Optional[str]:
        """
        Upload a file to OpenAI and return the file ID.

        Args:
            file_path: Path to the file to upload
            purpose: Purpose of the file (default: "assistants")

        Returns:
            File ID if successful, None otherwise
        """
        try:
            url = f"{self.base_url}/files"

            with open(file_path, "rb") as file:
                files = {"file": (os.path.basename(file_path), file), "purpose": (None, purpose)}

                headers = {"Authorization": f"Bearer {self.api_key}"}

                response = requests.post(url, files=files, headers=headers)
                response.raise_for_status()

                result = response.json()
                print(f"File uploaded successfully. File ID: {result['id']}")
                return result["id"]

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error uploading file: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def create_completion(
        self, messages: list, model: str = "gpt-4", file_ids: Optional[list] = None, **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Create a chat completion with optional file attachments.

        Args:
            messages: List of message objects
            model: Model to use (default: "gpt-4")
            file_ids: List of file IDs to attach
            **kwargs: Additional parameters for the API call

        Returns:
            API response if successful, None otherwise
        """
        try:
            url = f"{self.base_url}/chat/completions"

            # Prepare messages with file attachments if provided
            if file_ids:
                for message in messages:
                    if message.get("role") == "user" and "content" in message:
                        # Add file references to the message content
                        file_references = []
                        for file_id in file_ids:
                            file_references.append({"type": "file", "file_id": file_id})

                        if isinstance(message["content"], str):
                            message["content"] = [
                                {"type": "text", "text": message["content"]},
                                *file_references,
                            ]
                        elif isinstance(message["content"], list):
                            message["content"].extend(file_references)

            payload = {"model": model, "messages": messages, **kwargs}

            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error creating completion: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def simple_chat(
        self, user_message: str, file_path: Optional[str] = None, model: str = "gpt-4"
    ) -> Optional[str]:
        """
        Simple chat interface with optional file upload.

        Args:
            user_message: The user's message
            file_path: Optional path to a file to upload and analyze
            model: Model to use

        Returns:
            Assistant's response if successful, None otherwise
        """
        file_ids = []

        # Upload file if provided
        if file_path:
            file_id = self.upload_file(file_path)
            if file_id:
                file_ids.append(file_id)
            else:
                print("Failed to upload file, continuing without it...")

        # Prepare messages
        messages = [{"role": "user", "content": user_message}]

        # Create completion
        response = self.create_completion(messages, model=model, file_ids=file_ids)

        if response and "choices" in response:
            return response["choices"][0]["message"]["content"]
        else:
            print("Failed to get response from ChatGPT")
            return None


def main():
    """Example usage of the ChatGPTClient."""
    try:
        # Initialize the client
        client = ChatGPTClient()

        # Example 1: Simple chat without file
        print("=== Simple Chat ===")
        response = client.simple_chat("Hello! Can you explain what machine learning is?")
        if response:
            print(f"ChatGPT: {response}")

        print("\n" + "=" * 50 + "\n")

        # Example 2: Chat with file upload
        print("=== Chat with File Upload ===")
        # Replace with an actual file path you want to analyze
        file_path = "example.txt"  # Change this to your file path

        if os.path.exists(file_path):
            response = client.simple_chat(
                "Please analyze this file and summarize its contents:", file_path=file_path
            )
            if response:
                print(f"ChatGPT: {response}")
        else:
            print(f"File '{file_path}' not found. Please provide a valid file path.")

        # Example 3: Advanced usage with custom parameters
        print("\n=== Advanced Usage ===")
        messages = [
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": "Write a Python function to calculate fibonacci numbers."},
        ]

        response = client.create_completion(
            messages=messages, model="gpt-4", temperature=0.7, max_tokens=500
        )

        if response and "choices" in response:
            print(f"ChatGPT: {response['choices'][0]['message']['content']}")

    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please make sure you have a .env file with OPENAI_API_KEY set")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
