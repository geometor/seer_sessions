import numpy as np

def describe_grid(grid):
    """Provides a textual description of a grid."""
    rows, cols = grid.shape
    description = f"Grid Size: {rows}x{cols}\n"
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            description += f"({r},{c}): {color} "
        description += "\n"
    return description

def analyze_results(task_data):
   """Analyzes the results of applying the transform function."""
   reports = []
   for example in task_data['train']:
      input_grid = np.array(example['input'])
      output_grid = np.array(example['output'])
      predicted_grid = transform(input_grid)  # Apply the transform function
      
      report = {
          'input': describe_grid(input_grid),
          'expected_output': describe_grid(output_grid),
          'predicted_output': describe_grid(predicted_grid),
          'comparison': (output_grid == predicted_grid).all()
      }
      reports.append(report)
   return reports
   

# This is placeholder task data.  In a real scenario, this would be loaded.
task_data = {
    'train': [
       {'input': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
        'output': [[0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]},
       {'input': [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
        'output': [[0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]},
       {'input': [[0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
        'output': [[0, 0, 3, 0, 0, 0], [0, 0, 3, 0, 0, 0], [0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0]]},
    ]
}

reports = analyze_results(task_data)
for i, report in enumerate(reports):
  print(f"Example {i+1}:")
  print(f"  Comparison (Correct Output == Predicted): {report['comparison']}")
  print(f"Input:\n{report['input']}")
  print(f"Expected Output:\n{report['expected_output']}")
  print(f"Predicted Output:\n{report['predicted_output']}")
