import inspect


class ConstantGroup:
    def __iter__(self):
        for name, cls in vars(self.__class__).items():
            if inspect.isclass(cls):
                for const_name, const_value in vars(cls).items():
                    if not const_name.startswith("__") and not callable(const_value):
                        yield const_value

            elif not name.startswith("__"):
                yield vars(self.__class__).get(name)


class EmbeddingModels(ConstantGroup):
    class OpenAI(ConstantGroup):
        TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"

    class VoyageAI(ConstantGroup):
        VOYAGE_LARGE_2_INSTRUCT = "voyage-large-2-instruct"


class LargeLanguageModels(ConstantGroup):
    class OpenAI(ConstantGroup):
        GPT_4O = "gpt-4o"
        GPT_35_TURBO = "gpt-3.5-turbo-0125"

    class MetaAI(ConstantGroup):
        LLAMA_3_70B = "llama3:70b"
