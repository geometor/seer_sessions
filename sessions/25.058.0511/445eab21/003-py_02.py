import numpy as np

def analyze_example(example_num, input_grid, output_grid, transform_func):
    """Analyzes a single example and gathers relevant metrics."""

    # 1. Input Grid Properties
    input_shape = input_grid.shape
    input_colors = np.unique(input_grid)

    # 2. Identified Objects (all colors)
    objects = find_objects(input_grid)  # Uses the provided find_objects function
    object_colors = [input_grid[obj[0]] for obj in objects]

    # 3. Output Grid Properties
    output_shape = output_grid.shape
    output_colors = np.unique(output_grid)

    # 4. 2x2 Azure Subgrid Existence
    azure_objects = [obj for obj in objects if input_grid[obj[0]] == 8]
    has_2x2_azure = False
    for azure_obj in azure_objects:
        if extract_subgrid(input_grid, azure_obj) is not None:
            has_2x2_azure = True
            break

    # 5. Code Output vs. Expected Output
    predicted_output = transform_func(input_grid)
    match = np.array_equal(predicted_output, output_grid)
    
    print(f"--- Example {example_num} ---")
    print(f"Input Shape: {input_shape}")
    print(f"Input Colors: {input_colors}")
    print(f"Number of Objects: {len(objects)}")
    print(f"Object Colors: {object_colors}")
    print(f"Output Shape: {output_shape}")
    print(f"Output Colors: {output_colors}")
    print(f"Has 2x2 Azure Subgrid: {has_2x2_azure}")
    print(f"Predicted Output Matches Expected: {match}")
    print("\n")
    
    return {
      'example_num': example_num,
      'input_shape': input_shape,
      'input_colors': input_colors,
      'num_objects': len(objects),
        'object_colors': object_colors,
        'output_shape': output_shape,
        'output_colors': output_colors,
        'has_2x2_azure': has_2x2_azure,
        'match': match,
    }


# Example data (replace with actual data from the task)
examples = [
    {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8]]),
        "output": np.array([[8, 8], [8, 8]])
    },
        {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[8, 8], [8, 8]])
    },
    {
        "input": np.array([[8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8], [8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8], [8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8], [8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8], [8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8], [8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8], [8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8], [8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8]]),
        "output": np.array([[8, 8], [8, 8]])
    },
    {
        "input": np.array([[5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5], [5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5], [5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5], [5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5], [5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5]]),
        "output": np.array([[8, 8], [8, 8]])
    },
    {
        "input": np.array([[8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8]]),
        "output": np.array([[8, 8], [8, 8]])
    }
]

results = []
for i, example in enumerate(examples):
    results.append(analyze_example(i + 1, example["input"], example["output"], transform))