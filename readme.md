# Propositional Logic Parser

A Propositional Logic Parser processes logical expressions by breaking them into tokens, checking their syntax, building a parse tree, and enabling further analysis or evaluation.

## How to use

```
python propositional_logic_parser.py <InputFile>
```

## Input file format
```txt
<NumberOfExpressions>
<Expression1>
<Expression2>
<Expression3>
<Expression4>
...
```

Existing test files:

```powershell
# Valid Expressions
python propositional_logic_parser.py ".\Input\valid_expressions.txt"

# Invalid Expressions
python propositional_logic_parser.py ".\Input\invalid_expressions.txt"

# Single expression for custom testing
python propositional_logic_parser.py ".\Input\single_expression.txt"
```