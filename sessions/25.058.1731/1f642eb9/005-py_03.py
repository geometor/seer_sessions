import numpy as np

def report(grid, label):
    # Find and report positions of key colors
    colors = {
      9: "maroon",
      8: "azure",
      6: "magenta",
      4: "yellow"
    }
    
    print(f"Report on {label}:")
    print(grid)

    for color_val, color_name in colors.items():
        coords = np.argwhere(grid == color_val)
        if len(coords) > 0:
            #find bounding box
            min_row, min_col = np.min(coords, axis=0)
            max_row, max_col = np.max(coords, axis=0)
            height = max_row - min_row + 1
            width = max_col - min_col + 1
            print(f"  {color_name} ({color_val}):")
            print(f"    Top-left: ({min_row}, {min_col})")
            print(f"    Bottom-right: ({max_row}, {max_col})")
            print(f"    Height x Width: {height} x {width}")
        else:
            print(f"  {color_name} ({color_val}): Not found")

# Load the training data
train_data = [
    # Example 1
    {
      "input": np.array([[9, 8, 8, 8, 4],
                        [0, 8, 8, 8, 0],
                        [0, 8, 8, 8, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 6, 0]]),
      "output": np.array([[9, 8, 8, 8, 4],
                         [9, 8, 8, 8, 0],
                         [0, 8, 8, 8, 0],
                         [6, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0]])
    },
    # Example 2
    {
      "input": np.array([[9, 8, 8, 0, 0],
                        [0, 8, 8, 0, 0],
                        [0, 8, 8, 0, 6],
                        [0, 8, 8, 0, 0],
                        [0, 8, 8, 0, 0],
                        [4, 0, 0, 0, 0]]),
      "output": np.array([[9, 8, 8, 0, 0],
                        [9, 8, 8, 0, 0],
                        [0, 8, 8, 0, 0],
                        [0, 8, 8, 0, 0],
                        [4, 8, 8, 6, 0],
                        [0, 0, 0, 0, 0]])
    },
    # Example 3
      {
        "input": np.array([[9, 0, 0, 0, 0, 0],
                          [8, 8, 6, 0, 4, 0],
                          [8, 8, 0, 0, 0, 0]]),
        "output": np.array([[9, 0, 0, 0, 0, 0],
                          [9, 8, 0, 0, 4, 0],
                          [8, 8, 6, 0, 0, 0]])
      },
]

# Example usage with train and test data

for i,task in enumerate(train_data):
  report(task['input'],f'training example {i+1} input')
  report(task['output'],f'training example {i+1} output')
