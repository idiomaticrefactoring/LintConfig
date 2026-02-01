### Task: Prepare Complete Linter Documentation for all Linter Rules

You are responsible for generating a complete linter rule documentation file in JSON format.

#### Prerequisite
- Load `<LinterNameIndex>.json`, which contains the list of linter rules and their documentation URLs.

#### Instructions

1. **Check for Existing Complete Documentation**
   - If `<LinterNameCompleteInformation>.json` exists, Finish! 
   - Otherwise, do the step 2!

2. **Generate Complete Documentation When Missing**
   - If `<LinterNameCompleteInformation>.json` does not exist:
     - For each `LinterRuleUrl`, fetch and parse the official documentation page.
     - Extract the following information for each linter rule:
       - Rule description
       - Configuration options (if any)
     - Save each LinterRule'result as `<LinterRuleNameCompleteInformation>.json` at `skills/LintConfig/data/<LinterName>/rules/`.
     - Write Python code to aggregate all `<LinterRuleNameCompleteInformation>.json` into one json file `<LinterNameCompleteInformation>.json`

#### Output Format

The generated JSON file must follow this structure:

```json
{
  "linter_rule_name": {
    "description": "Rule description",
    "option": {
      "option_name": {
        "option_description": "Description of the option",
        "option_data_type": "Data type (e.g. boolean, string, number, array)",
        "default_value": "Default value",
        "option_values": {
          "valuelist": [
            "value1",
            "value2"
          ],
          "value1": "Explanation of value1",
          "value2": "Explanation of value2"
        }
      }
    }
  }
}
```

#### Option Value Rules

- If the number of valid option values is **50 or fewer**, list all values explicitly in `valuelist`.
- If the number of valid option values exceeds **50**, use a single descriptive sentence in `valuelist` to summarize the allowed values.
- If all option values are explicitly listed, provide a concise explanation for each value.
- If values are summarized instead of listed, provide one sentence explaining the overall meaning or constraint.

#### Notes

- Ensure rule names and option names are accurate and unique.
- Keep descriptions concise, precise, and derived from official documentation.
- The final output must be valid, well-formatted JSON suitable for long-term documentation use.
