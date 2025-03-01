# Conceptual Code - for analysis, not execution
import numpy as np

def analyze_example(input_grid, output_grid):
    input_columns = []
    output_columns = []

    for i in range(input_grid.shape[1]):
        input_columns.append({
            'color': input_grid[0, i] if len(set(input_grid[:, i])) == 1 else -1,
            'index': i
        })

    for i in range(output_grid.shape[1]):
        output_columns.append({
            'color': output_grid[0,i] if len(set(output_grid[:, i])) == 1 else -1,
            'index': i
        })

    return input_columns, output_columns

#Example Usage and Expected output for each example

task_examples = [
    (train_input_0, train_output_0),  # Assuming these are defined elsewhere
    (train_input_1, train_output_1),
    (train_input_2, train_output_2),
    (train_input_3, train_output_3),
    (train_input_4, train_output_4)
]

for i, (inp, outp) in enumerate(task_examples):
  in_cols, out_cols = analyze_example(inp, outp)
  print(f"Example {i}:")
  print(f"  Input Columns: {in_cols}")
  print(f"  Output Columns: {out_cols}")
