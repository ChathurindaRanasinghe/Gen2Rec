from prompts import RECOMMENDATION_ENGINE_PROMPT_FOOTER


class RecommendationEnginePrompt:

    def __init__(
        self,
        role,
        item,
        task=None,
        user_profile=False,
        explanation=False,
        explanation_examples=None,
        output_parameters=None,
    ) -> None:
        self.role = role
        self.item = item
        self.user_profile = user_profile
        self.task = task
        self.explanation = explanation
        self.explanation_examples = explanation_examples
        self.output_parameters = output_parameters
        self.prompt = ""

    def _role_injection(self):
        role_description = f"Assume you are a {self.role}."
        self.prompt += role_description

    def _task_description(self):
        if self.task is None:
            task_description = f"Your task is to help the user to find the best {self.item} for his needs. Recommend him the most suitable {self.item} from the given items."
        self.prompt += task_description

    def _task_boundary(self):
        if self.explanation:
            task_boundary = f"\nProvide a clear explanation why you recommended that {self.item}."
        else:
            task_boundary = "ONLY provide "
            for parameter in self.output_parameters:
                task_boundary += f"{parameter}, "
            task_boundary += "\nEXAMPLES:\n"
            for idx, example in enumerate(self.explanation_examples, start=1):
                task_boundary += f"{idx}. {example}\n"
            task_boundary += "END OF EXAMPLES\n"

        self.prompt += task_boundary

    def get_prompt(self):
        self._role_injection()
        self._task_description()
        self._task_boundary()
        self.prompt += "\n"
        self.prompt += RECOMMENDATION_ENGINE_PROMPT_FOOTER
        return self.prompt


template = RecommendationEnginePrompt(role="laptop reviewer", item="laptop", explanation=True)
print(template.get_prompt())
