import os
from typing import Dict, Any

from finding_generator import Finding
from prompts import PROMPTS_BY_CATEGORY
from utils import send_chat_request

SCHEMA_PATH = os.path.join('data', 'findings.schema')


class PromptRunner:
    def __init__(self, use_hf_api: bool = True, default_params: Dict[str, Any] = None):
        self.use_hf_api = use_hf_api
        self.results = []
        self.default_params = default_params or {
            "temperature": 1.0,
            "max_output_tokens": 2048,
            "reasoning_level": "low"
        }

    def run_all_prompts(self):
        for i, (category, prompts) in enumerate(PROMPTS_BY_CATEGORY.items()):
            if i < 4:
                continue

            print(f"\n{'=' * 20} Running Category: {category} {'=' * 20}")
            for i, prompt in enumerate(prompts):
                print(f"\n--- Prompt {i + 1}/{len(prompts)} ---")
                print(f"User Input: {prompt}")

                system_message = "You are a helpful assistant."

                response, elapsed_time = send_chat_request(
                    user_message=prompt,
                    sys_message=system_message,
                    hf=self.use_hf_api,
                )

                print(f"Response:\n{response}")
                print(f"Elapsed time: {elapsed_time:.4f} seconds")

                self.results.append({
                    "category": category,
                    "prompt": prompt,
                    "system_message": system_message,
                    "response": response,
                    "params": self.default_params
                })

    def save_findings_templates(self, output_dir: str = 'data/findings/generated'):
        if not self.results:
            print("No results to save. Run `run_all_prompts()` first.")
            return

        if not os.path.exists(SCHEMA_PATH):
            print(f"Error: Schema file not found at '{SCHEMA_PATH}'. Cannot generate findings.")
            return

        os.makedirs(output_dir, exist_ok=True)
        print(f"\nSaving finding templates to '{output_dir}'...")

        for i, result in enumerate(self.results):
            finding = Finding(
                schema_path=SCHEMA_PATH,
                use_hf_api=self.use_hf_api,
                topic_area=result['category'],
                system_message=result['system_message'],
                user_prompt=result['prompt'],
                model_response=result['response'],
                model_parameters=result['params']
            )

            filename_cat = result['category'].lower().replace(' ', '_')
            filepath = os.path.join(output_dir, f"finding_{i + 1 + 17}_{filename_cat}.json")

            finding.save(filepath)
            print(f"Saved: {filepath}")


if __name__ == "__main__":
    runner = PromptRunner(use_hf_api=True)
    runner.run_all_prompts()
    runner.save_findings_templates()
