# Utility

## Token Counter

To use token counter, use following methods.

1. Use command `python utility/token_counter.py gpt-3.5-turbo "This is the text you want to analyze."`
2. Use `from utility.token_counter import count_tokens` to import method and
   use `count_tokens(model, text)` method.

Following are the encoding models that are supported.

| Encoding name           | OpenAI models                                        |
|-------------------------|------------------------------------------------------|
| `cl100k_base`           | `gpt-4`, `gpt-3.5-turbo`, `text-embedding-ada-002`   |
| `p50k_base`             | Codex models, `text-davinci-002`, `text-davinci-003` |
| `r50k_base` (or `gpt2`) | GPT-3 models like `davinci`                          |
