import numpy as np

def describe_grid(grid):
    """Provides a basic description of the grid: dimensions and unique colors."""
    return {
        "shape": grid.shape,
        "unique_colors": np.unique(grid).tolist()
    }

def compare_grids(grid1, grid2):
    """Compares two grids and returns a diff-like representation."""
    if grid1.shape != grid2.shape:
        return "Shapes are different: {} vs {}".format(grid1.shape, grid2.shape)
    else:
        diff = grid1 != grid2
        if np.any(diff):
          coords = np.argwhere(diff)
          diff_report = []
          for r,c in coords:
            diff_report.append(f"diff at ({r},{c}) expected {grid2[r,c]} but got {grid1[r,c]}")
          return diff_report
        else:
          return "Grids are identical"

# Example data (replace with actual data from the task)
example_data = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 3, 0, 0, 8, 0],
                           [0, 0, 0, 0, 0, 0, 0]]),
        "expected_output": np.array([[0, 0, 0, 0, 0, 0, 0],
                                    [0, 3, 3, 3, 5, 8, 8],
                                    [0, 0, 3, 0, 5, 8, 0]]),
        "actual_output": np.array([[0, 0, 0, 0, 0, 0, 0],
                                  [0, 3, 3, 3, 5, 8, 8],
                                  [0, 0, 3, 0, 5, 8, 0]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 3, 0, 0, 8, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0]]),
        "expected_output": np.array([[0, 3, 3, 5, 8, 8, 0],
                                  [0, 3, 3, 5, 8, 8, 0],
                                    [0, 3, 0, 5, 8, 0, 0]]),
        "actual_output": np.array([[0, 3, 3, 5, 8, 8, 0],
                                    [0, 3, 3, 5, 8, 8, 0],
                                    [0, 0, 3, 0, 8, 0, 0]])

    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 8, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 3, 0, 0, 0, 0, 0, 0]]),
        "expected_output": np.array([[0, 0, 0, 8, 0, 0, 0, 0],
                                     [0, 3, 3, 8, 8, 8, 0, 0],
                                     [0, 3, 3, 5, 5, 8, 0, 0],
                                     [0, 3, 0, 0, 0, 0, 0, 0]]),
        "actual_output": np.array([[0, 0, 0, 8, 8, 8, 0, 0],
                                  [0, 3, 3, 3, 5, 8, 8, 8],
                                  [0, 0, 3, 0, 5, 8, 8, 8],
                                  [0, 0, 0, 0, 0, 0, 0, 0]])

    },
    {
        "input": np.array([[3, 0, 0, 0, 8, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 3],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 8, 0, 0, 0, 0, 0, 0]]),
        "expected_output": np.array([[3, 3, 3, 5, 8, 8, 8, 0, 0],
                                     [3, 0, 0, 5, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 5, 0, 0, 0, 3, 3],
                                     [0, 0, 0, 5, 0, 0, 0, 3, 0],
                                     [8, 8, 8, 5, 0, 0, 0, 0, 0]]),
        "actual_output": np.array([[3, 3, 3, 5, 8, 8, 8, 0, 0],
                                     [0, 0, 3, 0, 8, 8, 8, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 3, 3],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 3],
                                     [8, 8, 8, 0, 0, 0, 0, 0, 0]])

    },
    {
         "input":  np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0]]),
        "expected_output": np.array([[0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 3, 0],
                                     [0, 0, 0, 8, 5, 8, 8, 0, 0, 0, 3, 0],
                                     [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 3, 3],
                                     [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 3, 0],
                                     [8, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0],
                                     [8, 8, 8, 0, 5, 3, 3, 0, 0, 0, 0, 0],
                                     [8, 5, 0, 0, 5, 3, 0, 0, 0, 0, 0, 0],
                                     [0, 5, 0, 0, 5, 3, 3, 3, 0, 0, 0, 0]]),
        "actual_output": np.array([[0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 3, 3],
                                    [0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 3],
                                    [0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 3, 3],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [8, 8, 8, 0, 0, 0, 3, 3, 3, 0, 0, 0],
                                    [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0]])

    }

]

for i, example in enumerate(example_data):
    print(f"Example {i+1}:")
    print("  Input:", describe_grid(example["input"]))
    print("  Expected Output:", describe_grid(example["expected_output"]))
    print("  Actual Output:", describe_grid(example["actual_output"]))
    diff_report = compare_grids(example["actual_output"], example["expected_output"])
    print("  Differences:")
    if isinstance(diff_report, list):
        for line in diff_report:
          print("   ", line)
    else:
        print("   ", diff_report)
    print("-" * 40)
