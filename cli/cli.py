import os
import argparse
import sys
from pathlib import Path
from anthropic import Anthropic

def main():
    parser = argparse.ArgumentParser(description="Anthropic API Command Line Tool")
    parser.add_argument("-g", "--message", action="append", nargs=2, metavar=("role", "content"), help="Add a message with the specified role and content")
    parser.add_argument("-i", "--image", type=str, help="Path to the image file")
    parser.add_argument("-m", "--model", type=str, default="claude-3-opus-20240229", help="Anthropic model to use (default: claude-3-opus-20240229)")
    parser.add_argument("-s", "--system", type=str, help="System message")
    parser.add_argument("-t", "--temperature", type=float, help="Temperature for the model")
    parser.add_argument("-k", "--top_k", type=int, help="Top-k sampling")
    parser.add_argument("-p", "--top_p", type=float, help="Top-p sampling")
    parser.add_argument("-x", "--max_tokens", type=int, default=1024, help="Maximum number of tokens in the response (default: 1024)")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY environment variable is not set.")
        sys.exit(0)

    client = Anthropic(api_key=api_key)

    messages = []
    if args.message:
        for role, content in args.message:
            message = {"role": role, "content": content}
            messages.append(message)

    if args.image:
        image_path = Path(args.image)
        if not image_path.is_file():
            print(f"Image file not found: {args.image}")
            return

        image_message = {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": image_path,
            },
        }

        if messages:
            last_message = messages[-1]
            if isinstance(last_message["content"], list):
                last_message["content"].append(image_message)
            else:
                last_message["content"] = [{"type": "text", "text": last_message["content"]}, image_message]
        else:
            messages.append({"role": "user", "content": [{"type": "text", "text": ""}, image_message]})

    create_kwargs = {
        "max_tokens": args.max_tokens,
        "messages": messages,
        "model": args.model,
    }

    if args.system is not None:
        create_kwargs["system"] = args.system
    if args.temperature is not None:
        create_kwargs["temperature"] = args.temperature
    if args.top_k is not None:
        create_kwargs["top_k"] = args.top_k
    if args.top_p is not None:
        create_kwargs["top_p"] = args.top_p

    response = client.messages.create(**create_kwargs)

    for content in response.content:
        if isinstance(content, dict) and content.get("type") == "text":
            print(content["text"])
        elif hasattr(content, "text"):
            print(content.text)

if __name__ == "__main__":
    main()