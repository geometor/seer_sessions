def code_execution(input_grid):
    import numpy as np
    
    def classify_row(row):
      if all(pixel == 6 for pixel in row):
          return 6  # Magenta
      elif all(pixel == 3 for pixel in row):
          return 3  # Green
      else:
          return 0  # White
    
    rows, _ = input_grid.shape
    row_classifications = [classify_row(input_grid[r]) for r in range(rows)]
    has_green = 3 in row_classifications
    has_magenta = 6 in row_classifications
    magenta_positions = [i for i, x in enumerate(row_classifications) if x == 6]
    green_positions = [i for i, x in enumerate(row_classifications) if x == 3]
    
    print(f"  Row Classifications: {row_classifications}")
    print(f"  Has Green: {has_green}, Has Magenta: {has_magenta}")
    print(f"  Magenta Positions: {magenta_positions}, Green Positions: {green_positions}")

task_data = [
    {
        "input": [
            [6, 6, 6, 6, 6, 6, 6],
            [3, 3, 3, 3, 3, 3, 3]
        ],
        "output": [
            [3, 3, 3],
            [6, 6, 6],
            [0, 0, 0]
        ]
    },
    {
        "input": [
            [6, 6, 6, 6, 6],
            [0, 0, 0, 0, 0],
            [3, 3, 3, 3, 3]
        ],
        "output": [
            [3, 3, 3],
            [6, 6, 6],
            [3, 3, 3]
        ]
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0],
            [6, 6, 6, 6, 6, 6],
            [0, 0, 0, 0, 0, 0],
            [3, 3, 3, 3, 3, 3]
        ],
        "output": [
            [3, 3, 3],
            [6, 6, 6],
            [3, 3, 3]
        ]
    },
    {
      "input":[
        [3, 3, 3, 3],
        [3, 3, 3, 3],
        [3, 3, 3, 3],
        [6, 6, 6, 6]
      ],
      "output":[
        [3, 3, 3],
        [6, 6, 6],
        [0, 0, 0]
      ]
    },
    {
      "input": [
        [6, 6, 6],
        [6, 6, 6]
      ],
      "output": [
        [6, 6, 6],
        [0, 0, 0],
        [0, 0, 0]
      ]
    }
]

for i, example in enumerate(task_data):
    print(f"Example {i+1}:")
    code_execution(np.array(example["input"]))