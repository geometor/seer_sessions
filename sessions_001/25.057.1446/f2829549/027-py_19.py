import numpy as np

def check_predominant_color(column):
    """
    Checks if a column has a predominant color (appears at least twice) and the column contains other numbers.
    Returns the predominant color if it exists and the conditions are met, otherwise returns None.
    """
    counts = {}
    for x in column:
        counts[x] = counts.get(x, 0) + 1
    
    predominant_color = None
    for color, count in counts.items():
        if count >= 2:
            predominant_color = color
            break
    
    if predominant_color is not None and len(counts) >1:
        return predominant_color
    else:
        return None


def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    input_grid = np.array(input_grid)
    rows = input_grid.shape[0]
    cols = input_grid.shape[1]
    output_grid = np.zeros((rows, 3), dtype=int)

    # Iterate through input grid columns in groups of three
    for j in range(3):
      
        column = input_grid[:,j]
        predominant = check_predominant_color(column)

        if predominant is not None:
                output_grid[:, j] = 3

    return output_grid.tolist()

# Example inputs (from the prompt and ARC problem description)
example_inputs = [
    [[0, 0, 5], [0, 1, 5], [0, 0, 5]],  # Example 1
    [[0, 0, 2], [0, 0, 2], [0, 0, 2]],  # Example 2
    [[0, 0, 0], [0, 2, 0], [0, 0, 0]],  # Example 3
]

# Expected outputs
example_outputs = [
    [[3, 3, 3], [3, 3, 3], [3, 3, 3]],
    [[3, 3, 3], [3, 3, 3], [3, 3, 3]],
    [[0, 0, 0], [3, 0, 0], [0, 0, 0]],
]
results = []
for i in range(len(example_inputs)):
  transformed = transform(example_inputs[i])
  results.append(transformed == example_outputs[i])

print(results)