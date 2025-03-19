import numpy as np

def get_horizontal_stripes(input_grid):
    """
    Identifies and returns horizontal stripes of specified colors.
    """
    rows, cols = input_grid.shape
    target_colors = [3, 7, 8, 1]
    stripes = []

    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] in target_colors:
                stripes.append((r, input_grid[r,c]))
                break # only the first occurence on a line
    return stripes
                

def transform(input_grid):
    """
    Transforms the input grid by replicating identified horizontal stripes of specific colors (3, 7, 8, and 1)
    across the entire output grid.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Get horizontal stripes
    stripes = get_horizontal_stripes(input_grid)
    
    # reconstruct based on stripes
    stripe_index = 0
    
    for r in range(rows):
        if stripe_index < len(stripes):
            output_grid[r,:] = stripes[stripe_index][1]
            stripe_index += 1
        else:
            # handle no more stripes
            pass
    return output_grid

# Example Data (replace with actual data from the task)
examples = [
    {
        "input": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                           [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7]]),
    },
    {
        "input": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]]),
    },
    {
        "input": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]),
    },
]

for i, example in enumerate(examples):
    input_grid = example["input"]
    expected_output = example["output"]
    predicted_output = transform(input_grid)
    
    match = np.array_equal(predicted_output, expected_output)

    print(f"Example {i+1}:")
    print(f"  Input shape: {input_grid.shape}")
    print(f"  Output shape: {expected_output.shape}")
    print(f"  Predicted Output shape: {predicted_output.shape}")
    print(f"  Match: {match}")
    print(f"  Stripes Identified: {get_horizontal_stripes(input_grid)}")
    print("-" * 20)