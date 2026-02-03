### Task: Prepare Linter Configuration Documentation

You are responsible for generating a linter rule index in JSON format.

#### Core Principle (Mandatory)

All user-provided names and paths (including linter names, directory names, and file paths)
MUST be resolved in a **case-insensitive** manner.

If a matching path exists on disk with different letter casing, it MUST be treated as valid,
and the system MUST use the **actual path as stored on disk** for all subsequent operations.

Example:
- User input path: `skills/lintconfig/data/checkstyle`
- Actual path on disk: `skills/LintConfig/data/Checkstyle`
- Result: The path MUST be resolved to `skills/LintConfig/data/Checkstyle`


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
    "url": "URL to the official rule documentation"
  },
  ...
}
```

#### Notes

- Ensure all rule names are unique and accurately captured.
- The final output should be valid JSON and suitable for documentation or automation use.
