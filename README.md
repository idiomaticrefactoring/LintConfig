# LintConfig

An AI skill that automatically interprets coding standards, configures static analysis and linting tools, executes lint checks, and assists with code quality improvement. The skill supports both configuration-only workflows (e.g., "generate a linter config for a coding standard") and end-to-end quality enforcement workflows (e.g., "check this code against our coding standard and suggest fixes").

## Features

- **Automatic Coding Standard Parsing**: Converts natural language coding standards into formalized coding rules using a structured grammar. 
- **Intelligent Linter Configuration**: Automatically maps coding rules to appropriate linter rules and generates validated configuration files.
- **Multi-Linter Support**: Currently supports Checkstyle (Java) with extensible architecture for additional linters.
- **Coverage Analysis**: Classifies configuration coverage (Exact Match, Over-Approximation, Under-Approximation) to help you understand how well the linter configuration aligns with your coding standards
- **End-to-End Workflow**: From coding standard → rules → configuration → linting → violation repair suggestions.
- **Rule Knowledge Base**: Pre-built index and complete information for Linter Rules.

## Installation

### Using Claude Marketplace (Claude Code)

Install directly in Claude Code with two commands:

```
/plugin marketplace add <your-username>/LintConfig
/plugin install LintConfig@<your-username>/LintConfig
```

### Manual Installation

1. Clone or download this repository
2. Copy the skill to the appropriate skills directory for your platform:

| Platform | Skills Directory | Activation |
|----------|-----------------|------------|
| Claude Code | `~/.claude/skills/` | Auto-activate |
| Cursor | `~/.cursor/skills/` | Auto-activate |
| Windsurf | `~/.windsurf/skills/` | Auto-activate |
| GitHub Copilot | `~/.copilot/skills/` | Use `/lintconfig` command |
| OpenCode | `~/.opencode/skills/` | Auto-activate |
| Codex | `~/.codex/skills/` | Use `/lintconfig` command |
| Gemini | `~/.gemini/skills/` | Auto-activate |

**Example:**
```bash
# For Claude Code
cp -r LintConfig ~/.claude/skills/

# For Cursor
cp -r LintConfig ~/.cursor/skills/
```

### Prerequisites

- Python 3.x (for rule data preparation scripts, if needed)
- Access to one of the supported AI coding assistants

## Usage

### Skill Mode (Auto-activate)

**Supported:** Claude Code, Cursor, Windsurf, OpenCode, Gemini

The skill activates automatically when you request linter configuration or code quality tasks. Just chat naturally:

```
Generate Checkstyle configuration for "Package declaration
The package declaration is not line-wrapped. The column limit (Section 4.4, Column limit: 100) does not apply to package declarations."
```

```
Configure Checkstyle for Google Java Style Guide
```

```
Check this code at LintConfig/code/ArrayCombination.java against our coding standard at LintConfig/test/test_cs/package_declaration.txt and suggest fixes
```

### Workflow Mode (Slash Command)

**Supported:** GitHub Copilot, Codex

Use the slash command to invoke the skill:

```
/lintconfig Generate a linter configuration that enforces:
Package declaration
The package declaration is not line-wrapped. The column limit (Section 4.4, Column limit: 100) does not apply to package declarations.
```

```
/lintconfig Configure Checkstyle for Google Java Style Guide
```

### Workflow Modes

#### 1. Configuration-Only Mode

Generate linter configuration files without executing lint checks:

```
Generate a Checkstyle configuration for the following coding standard:
[Your coding standard here]
```

#### 2. End-to-End Quality Enforcement Mode

Full workflow from standard → configuration → linting → repair:

```
Parse this coding standard, configure Checkstyle, lint my code, and suggest fixes:
[Your coding standard or file path or url]
[Your lintername]
[Your code or file path]
```

### Supported Platforms

| Platform | Installation | Activation | Status |
|----------|-------------|------------|--------|
| Claude Code | Marketplace / Manual | Auto-activate | ✅ Supported |
| Cursor | Manual | Auto-activate | ✅ Supported |
| Windsurf | Manual | Auto-activate | ✅ Supported |
| GitHub Copilot | Manual | Slash command `/lintconfig` | ✅ Supported |
| OpenCode | Manual | Auto-activate | ✅ Supported |
| Codex | Manual | Slash command `/lintconfig` | ✅ Supported |
| Gemini | Manual | Auto-activate | ✅ Supported |

## How It Works

The skill follows a structured 5-step process:

### Step 1: Extract Key Information
- Identifies coding standard (from text, file, or URL)
- Determines target linter (Checkstyle, ESLint, Ruff, etc.)
- Extracts programming language and code context
- Prepares linter rule knowledge base if needed

### Step 2: Formalize Coding Standards
- Parses natural language coding standards into atomic coding rules
- Uses structured grammar to represent rules formally
- Handles edge cases and clarifications as separate rules
- Outputs a complete rule set for configuration mapping

### Step 3: Configure Linter
- Maps each coding rule to candidate linter rules
- Retrieves complete rule documentation and options
- Binds option values within valid ranges
- Classifies coverage relationship (Exact Match, Over/Under-Approximation)
- Filters invalid configurations
- Generates validated configuration file

### Step 4: Execute Linter
- Runs the generated linter configuration against your code
- Captures and saves linting results
- Reports violations with context

### Step 5: Suggest Repairs
- Analyzes linting violations
- Provides fix suggestions aligned with coding rules
- Helps improve code quality systematically

## Supported Linters

| Linter | Language | Status | Rules Available |
|--------|----------|--------|-----------------|
| Checkstyle | Java | ✅ Active | 184+ rules |
| ESLint | JavaScript/TypeScript | 🚧 Planned | - |
| Ruff | Python | 🚧 Planned | - |
| Pylint | Python | 🚧 Planned | - |
| RuboCop | Ruby | 🚧 Planned | - |

## Project Structure

```
LintConfig/
├── data/                          # Linter rule knowledge base
│   └── Checkstyle/
│       ├── CheckstyleIndex.json   # Rule index (184 rules)
│       ├── CheckstyleConfig.xml   # Example configuration
│       └── rules/                 # Complete rule documentation
│           └── [184 JSON files]   # Individual rule details
├── prompt/                        # Prompt templates
│   ├── Prompt_Parse_CodingStandard.md
│   ├── Prompt_Configure_Linter.md
│   ├── Prompt_Prepare_LinterRuleIndex.md
│   └── Prompt_Prepare_LinterRuleCompleteInformation.md
├── output/                        # Generated configurations
│   ├── CheckstyleConfig.xml
│   ├── CONFIGURATION_SUMMARY.txt
│   └── RULE_MAPPING_TABLE.txt
├── test/                          # Test cases
│   ├── test_cs/                   # Checkstyle test files
│   └── test_task_prompt/          # Prompt examples
├── SKILL.md                       # Skill definition
└── README.md                      # This file
```

## Example Output

### Configuration Summary

```
CHECKSTYLE CONFIGURATION SUMMARY
================================================================================

PROJECT: Google Java Style Guide - Checkstyle Configuration
Total Coding Rules Analyzed: 47
Checkstyle Rules Configured: 23

COVERAGE CLASSIFICATION
- Exact Match:           32 rules (68%)
- Over-Approximation:    5 rules (11%)
- Under-Approximation:   3 rules (6%)
- Not Covered:           7 rules (15%)

Rules Successfully Mapped: 40 out of 47 (85%)
```

### Generated Configuration

The skill generates validated XML/JSON/YAML configuration files ready to use:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<module name="Checker">
  <module name="LineLength">
    <property name="max" value="100"/>
    <property name="ignorePattern" value="^(package|import) .*"/>
  </module>
  <module name="TreeWalker">
    <module name="NoLineWrap">
      <property name="tokens" value="PACKAGE_DEF"/>
    </module>
  </module>
</module>
```

## Coverage Classification

The skill classifies how well each linter configuration aligns with your coding rules:

- **Exact Match**: The linter configuration checks exactly the same violations as the coding rule
- **Over-Approximation**: The linter flags more issues than the coding rule requires
- **Under-Approximation**: The linter flags fewer issues than the coding rule requires
- **Mismatches**: Non-aligned cases (filtered out)

This helps you understand the limitations and make informed decisions about your linting setup.

## Contributing

We welcome contributions! Areas where help is needed:

1. **Additional Linter Support**: Add support for ESLint, Ruff, Pylint, RuboCop, etc.
2. **Rule Knowledge Base**: Expand rule documentation for existing and new linters
3. **Language Support**: Add support for more programming languages
4. **Testing**: Add test cases for various coding standards and edge cases
5. **Documentation**: Improve prompts and examples

### Development Setup

1. Clone the repository
2. Review the existing structure in `data/Checkstyle/` as a template
3. For new linters:
   - Create `data/<LinterName>/` directory
   - Generate `<LinterName>Index.json` with rule index
   - Create `rules/` directory with each rule complete documentation
4. Test with various coding standards and code samples

## Roadmap

- [x] Multi-platform deployment (Claude Code, Cursor, Windsurf, GitHub Copilot, OpenCode, Codex, Gemini)
- [ ] Support for 5+ major programming languages
- [ ] Support for 3-5 popular linters per language
- [ ] Enhanced prompt compatibility testing
- [ ] Automated rule knowledge base generation
- [ ] Integration with CI/CD pipelines
- [ ] CLI installer for easy multi-platform setup

## Acknowledgments

Inspired by the need for automated linting configuration in AI-assisted coding workflows. Built to bridge the gap between natural language coding standards and formal linter configurations.
