---
name: LintConfig-CodingStandard-Parse-CheckstyleURLVisit
description: A skill for configuring static analysis and linting tools based on given coding standards or style guidelines. 
It generates or adapts linter configurations (e.g., rule selection and option settings) to check whether code complies with specified coding standards. 
---

## Main Capabilities

* Generate executable linter configurations for coding standards or style guidelines (including popular standards, user-specified rules, and project-specific rules).


## Steps

### Step 1: Extract key information from user request: 


- **Coding Standard**: Google Java Style Guide, e-commerce, portfolio, dashboard, landing page, etc.
- **Linter Name**: Checktyle, ESLint, Pylint, Ruff, Flake8, etc.
- **Programming Language**: Java, Python, JavaScript, etc.
- **Linter Format**: Json, XML, YAML, etc.


### Step 2: Formalize Coding Standards into Coding Rules;
1. For each sentence in the coding standard, determine the number of atomic coding rules it contains (0, 1, 2, ...).
2. Parse all coding rules using given grammar by understanding its semantics. 

Formalize into the following format:

RuleSet: 1. Rule₁ ; 
         2. Rule₂ ; 
            ... ; 
         n. Ruleₙ ;

Rule ::= [Must | Optional] /  RuleUnit |

	 [Must | Optional] / If RuleUnit Then RuleUnit

RuleUnit ::= RuleEntitySet₁ (if needed) / [Not (if needed)] **RuleConstraintType (Value if needed)** /  RuleEntitySetₙ;

RuleEntitySet ::= [ Entity₁, ... , Entityₖ ] 

Entity ::= ProgrammingTerm₁(Value if needed) (of/at/within/...  ProgrammingTermₖ if needed) 

For example, one RuleSet is likes follows: 
Rule₁: Must / [FileName] / **is** /[ClassName]
Rule₂: Optional / **Not Exist** / [ImportStatement, PackageStatement, IfStatement]
...
Ruleₙ: Optional / [LineBreak at NonAssignmentOperator] **Before** / [NonAssignmentOperator]

### Step 3: Configure Linter Configuration for All Coding Rules;