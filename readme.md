# Propositional Logic Parser

A Propositional Logic Parser processes logical expressions by breaking them into tokens, checking their syntax, building a parse tree, and enabling further analysis or evaluation.

## How to use

```
python propositional_logic_parser.py <InputFile>
```

Existing test files:

```powershell
# Valid Expressions
python propositional_logic_parser.py ".\Input\valid_expressions.txt"

# Invalid Expressions
python propositional_logic_parser.py ".\Input\invalid_expressions.txt"

# Both valid and invalid expressions
python propositional_logic_parser.py ".\Input\mixed_expressions.txt"
```