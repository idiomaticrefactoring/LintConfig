---
name: LintConfig
description: A comprehensive skill for interpreting coding standards, configuring linting tools, executing lint checks, and assisting with code quality improvement. The skill is designed to support both configuration-only workflows (e.g., "generate a linter config") and end-to-end quality enforcement workflows (e.g., "check this code against our coding standard and suggest fixes").
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

Invoke prompt at `skills/LintConfig/prompt/Prompt_Prepare_LinterRuleCompleteInformation.md` to generate `<LinterRuleNameCompleteInformation>.json` at `skills/LintConfig/data/<LinterName>/rules/`


### Step 2: Formalize Coding Standards into Coding Rules: 

After completing Step 1, then you must **Must initiate a separate LLM call**, **strictly and exclusively follows the dedicated prompt** at `skills/LintConfig/prompt/Prompt_Parse_CodingStandard.md`. This isolated step has the single purpose of parsing the given coding standard. You must not combine it with any configuration generation or other tasks from the broader process. 

Show coding rules to users. 


### Step 3: Configure Linter Configuration for All Coding Rules in Linter Format; 
After completing Step 2, then you must **Must initiate a separate LLM call**, **strictly follows the dedicated prompt** at `skills/LintConfig/prompt/Prompt_Configure_Linter.md`. This isolated step has the single purpose of configure linter for the given coding rules. You must not combine it with any configuration generation or other tasks from the broader process. 

Show configuration to users and exact file path where the configuration has been saved. 


### Step 4: Invoke the Generated Linter Configuration to Lint the Code
After completing Step3, you can proceed the Step4. 
1. If **Code** is provided, execute the generated linter configuration to lint the current code string.
2. If a **CodeFilePath** is provided, execute the generated linter configuration to lint the code from the specified file.
3. If neither **Code** nor **CodeFilePath** is provided, ask the user if they would like to invoke the generated linter configuration to lint the code.  
   - If the user agrees, request the **Code** or **CodeFilePath** and proceed with linting.

Generate and Run command to lint code, and save the linting results "<LinterName>LintResult" if needed.

---

### Step 5: Repair Coding Violations Based on Coding Rules

After completing Step 5 that obtains the linting results, provide suggestions for fixing any coding violations. 



## Failure Handling

- Missing coding standards → request clarification
- Unsupported language or linter → explain limitations and suggest alternatives
- Lint execution failure → surface command output and diagnostics
