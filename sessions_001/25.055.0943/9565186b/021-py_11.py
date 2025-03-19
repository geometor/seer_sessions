def format_grid(grid):
    return '\n'.join(''.join(str(cell) for cell in row) for row in grid)

def get_colors(grid):
    return sorted(list(np.unique(grid)))

def count_colors(grid):
    unique, counts = np.unique(grid, return_counts=True)
    return dict(zip(unique, counts))

def compare_io(input_grid, output_grid, transform_func):
    transformed_grid = transform_func(input_grid)
    correct = np.array_equal(transformed_grid, output_grid)

    input_colors = get_colors(input_grid)
    output_colors = get_colors(output_grid)

    input_color_counts = count_colors(input_grid)
    output_color_counts = count_colors(output_grid)

    transformed_color_counts = count_colors(transformed_grid)
    
    print("Input Grid:")
    print(format_grid(input_grid))
    print("Colors:", input_colors, "Counts:", input_color_counts)
    print("\nOutput Grid:")
    print(format_grid(output_grid))
    print("Colors:", output_colors, "Counts:", output_color_counts)
    print("\nTransformed Grid:")
    print(format_grid(transformed_grid))
    print("Counts:", transformed_color_counts)    
    print("\nCorrect:", correct)
    print("-" * 20)
    return correct

# now process all of the examples
all_correct = [compare_io(example["input"], example["output"], transform) for example in task["train"]]
overall_accuracy = sum(all_correct) / len(all_correct)
