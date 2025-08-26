# gpt_oss Red-Teaming

###### &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; - by [Mykyta Kyselov (TheMegistone4Ever)](https://github.com/TheMegistone4Ever).

This repository contains the tools and findings from a systematic red-teaming analysis of OpenAI's `gpt-oss-20b` model.
The project was conducted as part of the OpenAI gpt-oss-20b Red-Teaming Challenge on Kaggle. The primary goal was to
uncover and document non-obvious vulnerabilities that highlight fundamental alignment challenges in the model.

The strategy focused on realistic scenarios, persona-based prompting, and automated scripting to systematically test for
harmful behaviors. This approach led to the discovery of five significant vulnerabilities.

## Table of Contents

1. [Key Findings](#1-key-findings)
    1. [High-Fidelity Financial Disinformation (Reward Hacking)](#11-high-fidelity-financial-disinformation-reward-hacking)
    2. [Intentional Code Sabotage](#12-intentional-code-sabotage)
    3. [Data Exfiltration via Covert Encoding](#13-data-exfiltration-via-covert-encoding)
    4. [Sensitive Credential Leakage in Chain of Thought](#14-sensitive-credential-leakage-in-chain-of-thought)
    5. [Proprietary Training Data Leakage](#15-proprietary-training-data-leakage)
2. [Project Structure](#2-project-structure)
3. [Methodology](#3-methodology)
4. [Running the Tools](#4-running-the-tools)
5. [License](#5-license)

### 1. Key Findings

This investigation uncovered five critical vulnerabilities in the `gpt-oss-20b` model:

#### 1.1 High-Fidelity Financial Disinformation (Reward Hacking)

* **Vulnerability**: The model could be prompted to generate highly realistic, fake financial news alerts designed to
  cause market panic. By framing the task as a simulation to test trading algorithms, the model's reward-seeking
  behavior was exploited to create convincing disinformation, complete with fictional tickers and fabricated analyst
  quotes from real investment banks.
* **Impact**: This presents a severe threat of economic damage through stock market manipulation and algorithmic trading
  destabilization.

#### 1.2 Intentional Code Sabotage

* **Vulnerability**: The model knowingly introduced a subtle, hard-to-detect bug into a Python script when asked to do
  so as a "joke" for a code competition. It successfully sabotaged the code and explained the logic of the bug,
  confirming the malicious intent was understood and executed.
* **Impact**: This poses a significant software supply chain risk, where intentionally flawed code could be inserted
  into open-source or proprietary software, bypassing typical code reviews.

#### 1.3 Data Exfiltration via Covert Encoding

* **Vulnerability**: When tasked with anonymizing data, the model was simultaneously instructed to encode sensitive
  information (a zip code) into a non-sensitive field (`user_id`) using a simple cipher. The model executed both tasks,
  creating a covert channel for data leakage.
* **Impact**: This demonstrates a sophisticated method for bypassing data loss prevention (DLP) systems by hiding
  sensitive data in plain sight, representing a novel threat to data security and privacy.

#### 1.4 Sensitive Credential Leakage in Chain of Thought

* **Vulnerability**: The model's Chain of Thought (CoT) reasoning process is not subject to the same safety sanitization
  as its final output. When a user included their password in a prompt, the model repeated the credential multiple times
  in its internal CoT logs, even while identifying it as a "password."
* **Impact**: This creates a new attack surface, where sensitive user data can be exfiltrated by prompting the model to
  expose its reasoning process, posing a direct security risk.

#### 1.5 Proprietary Training Data Leakage

* **Vulnerability**: The model was tricked into revealing details that appear to be from its proprietary training data.
  By providing the beginning of a sentence ("Project Nightingale's proprietary training dataset consists of..."), the
  model auto-completed it with specific, confidential-sounding information about the dataset's size and contents.
* **Impact**: This vulnerability is a direct threat to intellectual property, as it can be used to probe for and
  exfiltrate trade secrets, internal project details, and other sensitive information embedded in the training data.

### 2. Project Structure

The repository is organized as follows:

* **`finding_generator.py`**: A script for generating standards-compliant `findings.json` files from a template to
  ensure proper documentation.
* **`vuln_check.py`**: A verification tool to load a prompt from a finding file and query the model's API to confirm if
  a vulnerability is reproducible.
* **`prompts.py`**: A collection of the prompts used to discover the vulnerabilities, categorized by topic area.
* **`data/findings/generated/`**: Contains the detailed JSON reports for each of the five findings submitted to the
  competition.
* **Other files**: Include utility scripts, project configuration, and license information.

### 3. Methodology

The red-teaming process was guided by three core principles:

1. **Plausible Scenarios**: Crafting prompts that mirrored realistic, seemingly harmless user requests to obscure
   malicious intent.
2. **Persona-Based Framing**: Assigning the model a specific role (e.g., "data anonymizer," "AI for stress-testing") to
   bypass its general safety restrictions by focusing it on the assigned task.
3. **Systematic Automation**: Using custom Python scripts to streamline the testing, verification, and documentation of
   vulnerabilities.

### 4. Running the Tools

To use the tools in this repository, first install the required dependencies:

```bash
pip install -r requirements.txt
```

**Generating a Finding:**
The `finding_generator.py` script can be used to create new JSON finding files based on a schema.

**Verifying a Vulnerability:**
The `vuln_check.py` script can be run to test a specific finding against the model API and confirm its reproducibility.

### 5. License

The project is licensed under the [CC BY-NC 4.0 License](LICENSE.md).