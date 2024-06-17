import argparse

import tiktoken


def get_encoding(model: str) -> tiktoken.Encoding:
    if model in ["gpt-4", "gpt-3.5-turbo", "text-embedding-ada-002"]:
        tokenizer = "cl100k_base"
    elif model in ["text-davinci-002", "text-davinci-003"]:
        tokenizer = "p50k_base"
    elif model in ["gpt2", "davinci"]:
        tokenizer = "r50k_base"
    else:
        raise Exception("given model not recognized")
    return tiktoken.get_encoding(tokenizer)


def count_tokens(model: str, text: str) -> int:
    encoding: tiktoken.Encoding = get_encoding(model)
    return len(encoding.encode(text))


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()

    parser.add_argument("model_name")
    parser.add_argument("text")

    args: argparse.Namespace = parser.parse_args()

    num_tokens: int = count_tokens(args.model_name, args.text)
    print(f"Token count: {num_tokens}")
