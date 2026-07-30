import ast
import re 
import pandas as pd

column_name_pattern = re.compile(r"^[A-Za-z_]+$")

def _is_valid_column_name(column_name: object) -> bool: 
    return(
        isinstance(column_name, str)
        and column_name_pattern.fullmatch(column_name) is not None 
    )

def _has_valid_column_names(df: pd.DataFrame) -> bool:
    return all(_is_valid_column_name(column) for column in df.columns)

def _empty_dataframe() -> pd.DataFrame:
    return pd.DataFrame()

def _evaluate_expression(node: ast.AST, df: pd.DataFrame):
    if isinstance(node, ast.Name):
        if node.id not in df.columns:
            raise ValueError("Column does not exist")

        return df[node.id]

    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _evaluate_expression(node.left, df)
        right = _evaluate_expression(node.right, df)
        return left + right

    
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Sub):
        left = _evaluate_expression(node.left, df)
        right = _evaluate_expression(node.right, df)
        return left - right

    
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
        left = _evaluate_expression(node.left, df)
        right = _evaluate_expression(node.right, df)
        return left * right
    
    raise ValueError("Unsupported expression")

def add_virtual_column(
        df: pd.DataFrame,
        role: str,
        new_column: str,
) -> pd.DataFrame:
    """
    Return a copy of the DataFrame with and additional calculated column.

    If validation or calculation fails, ]an empty DataFrame is returned.
    """
    if not isinstance(df, pd.DataFrame):
        return _empty_dataframe()

    if not isinstance(role, str):
        return _empty_dataframe()

    if not isinstance(new_column, str):
        return _empty_dataframe()

    if not _has_valid_column_names(df):
        return _empty_dataframe()

    if not _is_valid_column_name(new_column):
        return _empty_dataframe()

    role = role.strip()

    if not role: 
        return _empty_dataframe()

    try: 
        expression = ast.parse(role, mode="eval")
    except SyntaxError:
        return _empty_dataframe()

    try: 
        result = _evaluate_expression(expression.body, df)
        result_df = df.copy()
        result_df[new_column] = result
        return result_df
    except (ValueError, TypeError, KeyError):
        return _empty_dataframe()