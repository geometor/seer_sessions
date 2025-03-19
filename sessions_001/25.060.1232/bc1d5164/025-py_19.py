def analyze_example(input_grid, output_grid):
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)

    input_colors = {obj['color'] for obj in input_objects}
    output_colors = {obj['color'] for obj in output_objects}
    
    print(f"Input Colors: {input_colors}")
    print(f"Output Colors: {output_colors}")

    print(f"Input Objects:")
    for obj in input_objects:
        print(f"  Color: {obj['color']}, Count: {len(obj['pixels'])}, BBox: {bounding_box(obj['pixels'])}")

    print(f"Output Objects:")
    for obj in output_objects:
        print(f"  Color: {obj['color']}, Count: {len(obj['pixels'])}, BBox: {bounding_box(obj['pixels'])}")

    print(f"Input Grid Size: {len(input_grid)}x{len(input_grid[0])}")
    print(f"Output Grid Size: {len(output_grid)}x{len(output_grid[0])}")

# Example data provided in the prompt
example_pairs = [
    ([[4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4]], [[4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4]]),
    ([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[1, 1], [1, 1]]),
    ([[0, 0, 0, 2, 2, 0, 0, 0], [0, 0, 0, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 0, 0, 0, 2, 2], [0, 2, 2, 0, 0, 0, 2, 2]], [[2, 2, 2, 2], [2, 2, 2, 2]]),
    ([[0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]], [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]])
]

for i, (input_grid, output_grid) in enumerate(example_pairs):
    print(f"----- Example {i+1} -----")
    analyze_example(input_grid, output_grid)
    print(transform(input_grid))