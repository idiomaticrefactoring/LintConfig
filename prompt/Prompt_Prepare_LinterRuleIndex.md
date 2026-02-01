### Task: Prepare Linter Configuration Documentation

You are responsible for generating a linter rule index in JSON format.

#### Instructions

1. **Check for Existing Index**
   - If `<LinterNameIndex>.json` exists, read the file and return its content directly.
   - Do not regenerate or modify the file if it already exists.

2. **Generate Index When Missing**
   - If `<LinterNameIndex>.json` does not exist:
   - Write Python code to fetch and parse rule information from `LinterNameUrl`.
   - Extract each linter rule’s name, description, and documentation URL.
   - Save the parsed result as `<LinterNameIndex>.json`.

#### Output Requirements

The generated JSON file must follow this structure:

```json
{
  "linter_rule_name": {
    "description": "Brief explanation of the rule",
    "ruleurl": "URL to the official rule documentation"
  }
}
```

#### Notes

- Ensure all rule names are unique and accurately captured.
- The final output should be valid JSON and suitable for documentation or automation use.
