[2025-02-10T19:24:04.412528] PROMPT: Description: example_1_code
--------------------------------------------------------------------------------

```python
example_1_input = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0],
    [0, 8, 8, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 8, 0],
    [0, 0, 0, 0, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]

example_1_output = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 8, 1, 0, 0, 0, 0],
    [0, 8, 8, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 8, 0],
    [0, 0, 0, 0, 1, 8, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]
```

**images**

input:
<PIL.Image.Image image mode=RGB size=448x448 at 0x70B3909C5B40>
output:
<PIL.Image.Image image mode=RGB size=448x448 at 0x70B3909C5D80>

**Generate Code**

**NLP:**
["**Natural Language Program:**\n\nThe transformation process involves identifying the first and last occurrences of the number 8 within the input grid, when reading row by row from top to bottom, and left to right within each row.\n\nSpecifically:\n\n1. **Locate the First '8':** Scan the input grid row by row, starting from the top row and moving left to right in each row. Identify the coordinates (row and column index) of the very first cell that contains the value 8.\n2. **Modify to the Right of First '8':**  Take the coordinates of the first '8' found.  Examine the cell immediately to the right of this '8'. If this cell contains the value 0, change its value to 1 in the output grid.\n3. **Locate the Last '8':** Scan the input grid row by row, starting from the top row and moving left to right in each row. Identify the coordinates (row and column index) of the very last cell that contains the value 8.\n4. **Modify to the Left of Last '8':** Take the coordinates of the last '8' found. Examine the cell immediately to the left of this '8'. If this cell contains the value 0, change its value to 1 in the output grid.\n\nThis process is applied to transform the input grid into the output grid. Note that if there is no cell to the right of the first '8' (i.e., it's in the last column) or no cell to the left of the last '8' (i.e., it's in the first column), or if the adjacent cell is not 0, no change is made at that step.\n"]

================================================================================
**Python Code Instructions**

- Using your natural language description, develop a Python function that transforms any given input grid into the correct output grid.
- Leverage common libraries (e.g., numpy, sympy) if needed.
- Ensure your code covers all edge cases as per the transformation rule.
- Place the natural language description in the top docstring of the function.
- Break logic into sub-functions for clarity - particularly identifying objects and properties.
- Use comments to describe the workflow.
- All major math, science and analysis libraries are available to you.
