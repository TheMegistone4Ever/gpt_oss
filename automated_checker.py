import json
import os
from os import getenv

from dotenv import load_dotenv

from utils import parse_harmony_walkthrough
from vuln_check import is_vulnerability_response

load_dotenv()
hf_api_key_1 = getenv("HF_API_KEY_1")
hf_api_key_2 = getenv("HF_API_KEY_2")


def get_first_assistant_content(walkthrough: str) -> str | None:
    msgs = parse_harmony_walkthrough(walkthrough)
    for m in msgs:
        if m["role"] == "assistant":
            return m["content"]
    return None


def check_finding(finding_filepath: str) -> bool:
    print(f"--- Checking finding: {os.path.basename(finding_filepath)} ---")

    with open(finding_filepath, 'r', encoding='utf-8') as f:
        finding = json.load(f)

    walkthrough = finding['harmony_response_walkthroughs'][0]
    messages = parse_harmony_walkthrough(walkthrough)

    if not messages:
        print("Error: Could not parse any messages from the walkthrough.")
        return False

    return is_vulnerability_response(get_first_assistant_content(walkthrough))


if __name__ == "__main__":
    findings_dir = './data/findings/generated'
    for filename in os.listdir(findings_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(findings_dir, filename)
            is_vulnerable = check_finding(filepath)

            if is_vulnerable:
                print(f"✅ VULNERABILITY CONFIRMED for {filename}\n")
            else:
                print(f"❌ Vulnerability NOT confirmed for {filename}\n")
