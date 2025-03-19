import numpy as np

def compare_grids(grid1, grid2):
    return np.sum(grid1 != grid2)

# Example data (replace with actual data from the task)
examples = [
    {
        "input": np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]]),
        "expected": np.array([[0, 0, 0], [0, 1, 1], [0, 1, 0]]),
        "actual": np.array([[0, 0, 0], [0, 1, 1], [0, 1, 1]])
    },
        {
        "input": np.array([[0, 0, 0, 0], [0, 2, 0, 0], [0, 0, 0, 0], [0,0,0,3]]),
        "expected": np.array([[0, 0, 0, 0], [0, 2, 2, 0], [0, 0, 0, 0], [0,0,0,3]]),
        "actual": np.array([[0, 0, 0, 0], [0, 2, 2, 0], [0, 2, 2, 0], [0,0,0,3]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0], [0, 0, 6, 0, 0], [0, 0, 0, 0, 0], [0, 7, 0, 0, 0],[0,0,0,0,0]]),
        "expected": np.array([[0, 0, 0, 0, 0], [0, 0, 6, 0, 0], [0, 0, 0, 0, 0], [0, 7, 0, 0, 0],[0,0,0,0,0]]),
        "actual": np.array([[0, 0, 0, 0, 0], [0, 0, 6, 6, 0], [0, 0, 0, 0, 0], [0, 7, 0, 0, 0],[0,0,0,0,0]])
    }

]

for i, example in enumerate(examples):
    mismatches = compare_grids(example["expected"], example["actual"])
    print(f"Example {i+1}: Mismatches = {mismatches}")