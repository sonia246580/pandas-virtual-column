# Pandas Virtual Column

A Python solution for a recruitment task that adds calculated (virtual) columns to a pandas DataFrame using arithmetic expressions.

## Features

- Supports addition (`+`), subtraction (`-`), and multiplication (`*`)
- Validates DataFrame column names
- Validates the new column name
- Rejects unsupported expressions and operators
- Returns an empty DataFrame when validation or calculation fails
- Does not modify the original DataFrame
- Uses Python AST instead of `eval()`

## Example

```python
import pandas as pd
from solution import add_virtual_column

df = pd.DataFrame(
    [[2, 3, 4]],
    columns=["label_one", "label_two", "label_three"],
)

result = add_virtual_column(
    df,
    "label_one + label_two * label_three",
    "result_column",
)

print(result)
```

Output:

```text
   label_one  label_two  label_three  result_column
0          2          3            4             14
```

## Requirements

- Python 3.10+
- pandas
- pytest

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running tests

```bash
pytest -q
```

The project includes:

- the original recruitment test cases,
- additional unit tests covering:
  - invalid DataFrame column names,
  - operator precedence,
  - complex arithmetic expressions,
  - unsupported operators,
  - preserving the original DataFrame.