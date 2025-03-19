import numpy as np

def describe_grid(grid):
    """Provides a concise description of a grid."""
    rows, cols = grid.shape
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    description = f"Grid: {rows}x{cols} - Colors: {color_counts}"
    return description

def analyze_results(examples):
    analysis = []
    for i, (input_grid, output_grid) in enumerate(examples):
        input_desc = describe_grid(input_grid)
        output_desc = describe_grid(output_grid)

        # Execute the transform function
        transformed_grid = transform(input_grid.copy())  # Use a copy to avoid modifying the original
        transformed_desc = describe_grid(transformed_grid)

        # Compare the transformed output with the expected output
        comparison = np.array_equal(transformed_grid, output_grid)

        analysis.append(
            {
                "example_index": i,
                "input": input_desc,
                "expected_output": output_desc,
                "transformed_output": transformed_desc,
                "match": comparison
            }
        )
    return analysis

# provided example data:
examples = [
    (np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,1,1,1,0,0,0],[0,0,0,1,0,1,0,0,0],[0,0,0,1,2,1,0,0,0],[0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]),
     np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,1,1,1,0,0,0],[0,0,0,1,2,1,0,0,0],[0,0,0,1,2,1,0,0,0],[0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]])),

    (np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,1,1,1,1,1,1,0,0],[0,0,1,0,0,0,0,1,0,0],[0,0,1,0,0,2,0,1,0,0],[0,0,1,0,0,0,0,1,0,0],[0,0,1,1,1,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]),
     np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,1,1,1,1,1,1,0,0],[0,0,1,2,2,2,2,1,0,0],[0,0,1,2,2,2,2,1,0,0],[0,0,1,2,2,2,2,1,0,0],[0,0,1,1,1,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]])),

    (np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,1,1,1,0,0,0],[0,0,0,1,0,1,0,0,0],[0,0,0,1,2,1,0,0,0],[0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]),
     np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,1,1,1,0,0,0],[0,0,0,1,2,1,0,0,0],[0,0,0,1,2,1,0,0,0],[0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]])),
    
    (np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,1,0,0,0,0,0],[0,0,0,1,0,1,0,0,0,0],[0,0,0,1,0,1,0,0,0,0],[0,0,0,1,0,1,0,0,0,0],[0,0,2,1,0,1,0,0,0,0],[0,0,0,1,1,1,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]),
    np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,1,0,0,0,0,0],[0,0,0,1,0,1,0,0,0,0],[0,0,0,1,0,1,0,0,0,0],[0,0,0,1,0,1,0,0,0,0],[0,0,2,1,2,1,0,0,0,0],[0,0,0,1,1,1,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]])
     )
]

analysis = analyze_results(examples)
for item in analysis:
    print(item)