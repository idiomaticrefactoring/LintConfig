---
name: LintConfig
description: A skill for configuring static analysis and linting tools based on given coding standards or style guidelines. It generates or adapts linter configurations (e.g., rule selection and option settings) to check whether code complies with specified coding standards. 
---

## Strictly Follow Steps:   

### Step 1: Extract key information from user request: 


- **CodingStandard**: "XXX".
- **CodingStandardURL** (if possible): "XXX". Visit the url to get coding standard. 
- **CodingStandardFilePath** (if possible): "XXX". Read the file to get coding standard.

- **LinterName**: Checktyle, ESLint, Ruff, etc. If user' request not specifiy the Linter, recommend a Linter to user.
- **LinterFormat**: Json, XML, YAML, etc.
- **LinterRuleURL** (if possible): "XXX".
- **LinterRuleFilePath** (if possible): "XXX".

- **ProgrammingLanguage**: Java, Python, JavaScript, etc.


- **Code** (if possible): "XXX".
- **CodeFilePath** (if possible): "XXX". 


Invoke prompt at `skills/LintConfig/prompt/Prompt_Prepare_LinterRuleIndex.md` to generate `<LinterName>Index.json` at `skills/LintConfig/data/<LinterName>/`

Invoke prompt at `skills/LintConfig/prompt/Prompt_Prepare_LinterRuleCompleteInformation.md` to generate `<LinterRuleNameCompleteInformation>.json` at `skills/LintConfig/data/<LinterName>/Rules/`


### Step 2: Formalize Coding Standards into Coding Rules: 

After completing Step 1, then you must **Must initiate a separate LLM call**, **strictly and exclusively follows the dedicated prompt** at `skills/LintConfig/prompt/Prompt_Parse_CodingStandard.md`. This isolated step has the single purpose of parsing the given coding standard. You must not combine it with any configuration generation or other tasks from the broader process. 

Show coding rules to users. 


### Step 3: Configure Linter Configuration for All Coding Rules in Linter Format; 
After completing Step 2, then you must **Must initiate a separate LLM call**, **strictly follows the dedicated prompt** at `skills/LintConfig/prompt/Prompt_Configure_Linter.md`.  This isolated step has the single purpose of configure linter for the given coding rules. After finish it, tell the user of the exact file path where the configuration has been saved.

Show configuration to users.