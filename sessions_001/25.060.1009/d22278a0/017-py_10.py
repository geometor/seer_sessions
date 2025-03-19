# --- Conceptual Code Execution ---
# For each training example (input, expected_output):
#   1.  predicted_output = transform(input)
#   2.  diff_grid = (predicted_output != expected_output).astype(int)
#   3.  Report:
#       - Input grid dimensions and seed pixel locations/colors
#       - Output grid dimensions
#       - Number of differing pixels: np.sum(diff_grid)
#       - Location of differing pixels: np.argwhere(diff_grid)
#       - For a sample of differing pixels:
#           - Expected color vs. Predicted color
#           - Surrounding pixel colors in input and output

# Example Report (Illustrative - based on provided images, not actual execution)

reports = []

example_data = [
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ],
        "output": [
            [0, 0, 0, 2, 0, 2, 0, 2],
            [0, 0, 0, 2, 0, 2, 0, 2],
            [0, 0, 0, 2, 0, 2, 0, 2],
            [0, 0, 0, 2, 0, 2, 0, 2],
            [0, 0, 0, 2, 0, 2, 0, 2],
            [0, 0, 0, 2, 0, 2, 0, 2],
            [0, 0, 0, 2, 0, 2, 0, 2]
        ]
    },
     {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        "output": [
            [0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 0, 0]
        ]
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        "output": [
            [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0]
        ]
    }
]

for i, example in enumerate(example_data):
    input_grid = np.array(example['input'])
    expected_output = np.array(example['output'])
    predicted_output = transform(input_grid)  # Assuming 'transform' is defined
    diff_grid = (predicted_output != expected_output).astype(int)

    report = {
        "example": i + 1,
        "input_dims": input_grid.shape,
        "output_dims": expected_output.shape,
        "seed_pixels": get_seed_pixels(input_grid),  # Assuming 'get_seed_pixels'
        "diff_count": np.sum(diff_grid),
        "diff_locations": np.argwhere(diff_grid).tolist(),  # Convert to list
        "sample_diffs": []
    }

    # Sample up to 3 differing pixels for detailed analysis
    sample_indices = np.random.choice(len(report["diff_locations"]),
                                        min(3, len(report["diff_locations"])),
                                        replace=False)
    for sample_idx in sample_indices:
        r, c = report["diff_locations"][sample_idx]
        sample_info = {
            "location": [int(r), int(c)],
            "expected": int(expected_output[r, c]),
            "predicted": int(predicted_output[r, c]),
            "input_neighbors": [],
            "output_neighbors": []
        }

        # Get 3x3 neighborhood around the differing pixel
        for i in range(max(0, r - 1), min(input_grid.shape[0], r + 2)):
            for j in range(max(0, c - 1), min(input_grid.shape[1], c + 2)):
                sample_info["input_neighbors"].append(
                    {"location": [i, j], "value": int(input_grid[i, j])})
                sample_info["output_neighbors"].append(
                    {"location": [i, j], "value": int(expected_output[i, j])})
        report["sample_diffs"].append(sample_info)

    reports.append(report)

for report in reports:
    print(report)
