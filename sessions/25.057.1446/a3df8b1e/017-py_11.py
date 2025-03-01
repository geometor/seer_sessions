def analyze_input_output(input_grid, output_grid):
    """Analyzes the input and output grids to count blue pixels."""

    input_blue_count = 0
    input_blue_positions = []
    for r in range(len(input_grid)):
        for c in range(len(input_grid[0])):
            if input_grid[r][c] == 1:
                input_blue_count += 1
                input_blue_positions.append((r, c))

    output_blue_count = 0
    for r in range(len(output_grid)):
        for c in range(len(output_grid[0])):
            if output_grid[r][c] == 1:
                output_blue_count += 1

    print(f"Input Blue Pixels: Count = {input_blue_count}, Positions = {input_blue_positions}")
    print(f"Output Blue Pixels: Count = {output_blue_count}")
    print("---")


# Example Usage (assuming 'task' is loaded and accessible)
for i, example in enumerate(task["train"]):
    print(f"Example {i+1}:")
    analyze_input_output(example["input"], example["output"])
