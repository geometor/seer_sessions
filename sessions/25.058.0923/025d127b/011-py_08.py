import numpy as np

def describe_grid(grid):
    """Provides a description of the grid, focusing on azure pixels."""
    azure_pixels = np.argwhere(grid == 8)
    if azure_pixels.size > 0:
        min_x = np.min(azure_pixels[:, 1])
        max_x = np.max(azure_pixels[:, 1])
        min_y = np.min(azure_pixels[:, 0])
        max_y = np.max(azure_pixels[:, 0])
        return {
            "azure_pixels": azure_pixels.tolist(),
            "min_x": int(min_x),
            "max_x": int(max_x),
            "min_y": int(min_y),
            "max_y": int(max_y)
        }
    else:
        return {"azure_pixels": [], "min_x": None, "max_x": None, "min_y": None, "max_y": None}

# Example Data (Replace with actual data from the task)
examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 8, 0, 0],
                           [0, 0, 0, 8, 0, 0],
                           [0, 0, 0, 8, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 8, 8, 0, 0],
                           [0, 0, 8, 8, 0, 0],
                           [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 8, 8, 0, 0],
                           [0, 0, 8, 8, 0, 0],
                           [0, 0, 0, 0, 0, 0]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 8, 0, 8, 0, 8, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 8, 0, 8, 0, 8, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 8, 0, 8, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 8, 0, 8, 0]])
    },
     {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 8, 0, 0, 0, 0],
                           [0, 0, 0, 8, 8, 8, 0, 0],
                           [0, 0, 0, 8, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 8, 8, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]])
    }

]

for i, example in enumerate(examples):
    print(f"Example {i+1}:")
    print("Input:")
    input_desc = describe_grid(example["input"])
    print(input_desc)
    print("Output:")
    output_desc = describe_grid(example["output"])
    print(output_desc)
    print("-" * 20)