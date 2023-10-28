import tiktoken

# cl100k_base	gpt-4, gpt-3.5-turbo, text-embedding-ada-002
# p50k_base	Codex models, text-davinci-002, text-davinci-003
# r50k_base (or gpt2)	GPT-3 models like davinci
encoding = tiktoken.get_encoding("cl100k_base")
num_tokens = len(encoding.encode("string"))

print(f"Token count: {num_tokens}")
