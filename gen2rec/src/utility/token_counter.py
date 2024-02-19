import sys

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
    num_tokens = count_tokens(sys.argv[1], sys.argv[2])
    print(f"Token count: {num_tokens}")
