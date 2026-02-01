## Formalize the Coding Standard into Coding Rules;

### Notes for Coding Rules:

1. One sentence may contain **0, 1, or multiple rules**.  
2. Multiple sentencesOne rule may a rule.
3. **Edge case clarification**, such as constraint introduced by "even when", "except", or "unless",  must be extracted as **individual atomic rules**.

### Strictly Follow the Steps: 
1. Treat **edge case clarifications** as individual atomic coding rules.
2. Remove sentences that contain **no coding rules**.
3. If a sentence contains **multiple coding rules**, split it into separate atomic rules.
4. If multiple sentences together form a single coding rule, treat them as **one atomic rule**.
5. Complete and clarify each atomic rule so that it is explicit and self-contained.
6. Split the coding standard into atomic coding rules. 
7. Count the total number of atomic coding rules (0, 1, 2, 3, ...).
8. Parse all coding rules using given grammar by understanding its semantics. 

Note: **Edge case clarification**, such as constraint introduced by even when, except, or unless,  must be extracted as **individual atomic rules**.


### RuleSet Grammar is as follows:

```
RuleSet: 1. Rule₁ ; 
         2. Rule₂ ; 
            ... ; 
         n. Ruleₙ ;

Rule ::= [Must | Optional] /  RuleUnit | [Must | Optional] / If RuleUnit, RuleUnit

RuleUnit ::= RuleEntitySet₁ (if needed) / [Not (if needed)] **ConstraintOperator (Value if needed)** /  RuleEntitySetₙ;

RuleEntitySet ::= [ Entity₁, ... , Entityₖ ] 

Entity ::= PLTerm₁(Value if needed) (of/at/within/is/... PLTermₖ constrain PLTerm₁ if needed) 

Note: In the ObligationLevel position of each rule, you **must only use Must or Optional.**

```

### Example RuleSet is as follows::


Rule₁: Must / [PLTerm] / **ConstraintOperator** / [PLTerm];

Rule₂: Must / **Not ConstraintOperator** / [WildcardImport, StaticImport];

...

Ruleₙ: Optional / [PLTerm of/at/within/is/ PLTerm] / **Before** / [NonAssignmentOperator]