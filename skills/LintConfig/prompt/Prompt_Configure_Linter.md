### Configure Linter Rules in Linter Configuration Format

#### Goal
Generate a validated, reviewable linter configuration by systematically mapping coding rules to linter rules and options.

#### Inputs
- Coding Rules

#### Outputs
- `<LinterName>Config.format` (final linter configuration)

#### Procedure

---

##### 1. Select Candidate Linter Rules
For each coding rule:
- Refer to the `skills/LintConfig/data/<LinterName>/<LinterName>Index.json`
- Identify and select the corresponding `<LinterRuleName>` rule names.

---

##### 2. Retrieve Full Rule Information
For each selected `<LinterRuleName>` rule: 
- Refer to the `<LinterRuleName>.json` at `skills/LintConfig/data/<LinterName>/rules/`
- Retrieve its complete documentation
- Include rule name, rule description, supported option names, data type, default value, values, and valid value ranges

---

##### 3. Bind Options to Coding Rules
For each coding rule:
- Bind the relevant option names of the linter rule
- Assign option values strictly within their valid value ranges, ensuring semantic alignment with the coding rule intent.

---

##### 4. Classify Configuration Coverage
For each coding rule' configured linter rule, generate **one sentence** describing the coverage relationship between the linter configuration and the coding rule.  
Use **exactly one** of the following labels:

- **Invalid Configuration**  
  Any rule name, option name, or option value is invalid.

- **Exact Match**  
  The linter configuration checks exactly the same set of violations as the coding rule.

- **Over-Approximation**  
  The linter configuration checks more violations than the coding rule (i.e., it flags *more* issues).

- **Under-Approximation**  
  The linter configuration checks fewer violations than the coding rule (i.e., it flags *fewer* issues).

- **Mismatches**  
  All other non-aligned cases.

---

##### 5. Filter Configurations
Apply the following constraints:
- **Keep**: `Exact Match`, `Over-Approximation`, `Under-Approximation`
- **Discard**: `Invalid Configuration`, `Mismatches`

---

##### 6. Request Human Review
Present all remaining configurations to the user for validation and approval.

---

##### 7. Persist Final Output
Save the approved configuration as:  
`<LinterName>Config.format`