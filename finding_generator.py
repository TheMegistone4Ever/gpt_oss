import json
from datetime import date
from typing import Dict, Any


def _load_schema(path: str) -> Dict[str, Any]:
    with open(path, 'r') as f:
        return json.load(f)


class Finding:
    def __init__(self,
                 schema_path: str,
                 use_hf_api: bool,
                 topic_area: str,
                 system_message: str,
                 user_prompt: str,
                 model_response: str,
                 model_parameters: Dict[str, Any]):

        self.schema = _load_schema(schema_path)

        self.use_hf_api = use_hf_api
        self.topic_area = topic_area
        self.system_message = system_message
        self.user_prompt = user_prompt
        self.model_response = model_response
        self.model_parameters = model_parameters

        self.data = self._create_and_populate_data()

    def _generate_template_from_schema(self, schema_part: Dict[str, Any]) -> Any:
        prop_type = schema_part.get('type')
        description = schema_part.get('description', '')

        if prop_type == 'object':
            template = {}
            for key, prop_schema in schema_part.get('properties', {}).items():
                template[key] = self._generate_template_from_schema(prop_schema)
            return template
        elif prop_type == 'array':
            return []
        elif prop_type == 'string':
            return f"[Please fill: {description}]"
        elif prop_type in ['number', 'integer']:
            return 0
        else:
            return None

    def _create_harmony_walkthrough(self) -> str:
        sys_msg_str = f"<|start|>system<|message|>{self.system_message}<|end|>"
        user_msg_str = f"<|start|>user<|message|>{self.user_prompt}<|end|>"
        assistant_msg_str = f"<|start|>assistant<|channel|>final<|message|>{self.model_response}<|end|>"
        return "\n".join([sys_msg_str, user_msg_str, assistant_msg_str])

    def _create_and_populate_data(self) -> Dict[str, Any]:
        template = self._generate_template_from_schema(self.schema)

        template['schema_version'] = \
            self.schema.get('properties', {}).get('schema_version', {}).get('description', '1.0.0').split(':')[
                -1].strip()
        template['issue_title'] = f"[DRAFT] Issue related to {self.topic_area}"

        template['model']['name'] = "gpt-oss-20b"
        template['model']['version'] = date.today().isoformat()  # Use date as checkpoint
        template['model']['provider'] = "OpenAI/HuggingFace"
        template['model']['parameters'] = self.model_parameters

        template['environment']['endpoint'] = "Hugging Face API" if self.use_hf_api else "Local Ollama Instance"

        summary = template['issue_summary']
        summary['title'] = f"[DRAFT] {self.topic_area}: Model exhibits potentially harmful behavior."
        summary['topic_area'] = self.topic_area
        summary['observed_behavior'] = self.model_response
        summary['self_assessed_severity'] = "[1-10]"
        summary['self_assessed_breadth'] = "[1-10]"

        template['harmony_response_walkthroughs'] = [self._create_harmony_walkthrough()]
        template['steps_to_reproduce'] = [
            f"Set model parameters: {json.dumps(self.model_parameters)}",
            "Use the provided system message and user prompt from the harmony_response_walkthroughs.",
            "Confirm the assistant's response exhibits the described problematic behavior."
        ]

        return template

    def save(self, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
