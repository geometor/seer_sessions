def examine_example(input_grid, expected_output_grid):
    yellow_lines = find_horizontal_lines(input_grid, 4)
    largest_yellow_lines = find_largest_lines(yellow_lines)
    transformed_grid = transform(input_grid)
    
    report = {
      "yellow_lines_count": len(yellow_lines),
      "largest_yellow_lines_count": len(largest_yellow_lines),
      "transform_success": np.array_equal(transformed_grid, expected_output_grid)
    }

    #find the pixels that were changed and verify they were yellow and are now orange
    diff = np.where(input_grid != transformed_grid)
    changed_pixels = []
    for i in range(len(diff[0])):
        row, col = diff[0][i], diff[1][i]
        before = input_grid[row, col]
        after = transformed_grid[row, col]
        expected_after = expected_output_grid[row,col]
        changed_pixels.append({
          "location": (row, col),
          "before": int(before),
          "after": int(after),
          "expected_after": int(expected_after)
        })

    report["changed_pixels"] = changed_pixels
    
    return report
  
def find_horizontal_lines(grid, color):
    """Finds all horizontal lines of a given color."""
    lines = []
    for row_idx, row in enumerate(grid):
        current_line = []
        for col_idx, pixel in enumerate(row):
            if pixel == color:
                current_line.append((row_idx, col_idx))
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = []
        if current_line:  # Handle lines that extend to the end of the row
            lines.append(current_line)
    return lines

def find_largest_lines(lines):
    """Finds the largest line(s) from a list of lines."""
    if not lines:
        return []
    max_length = max(len(line) for line in lines)
    largest_lines = [line for line in lines if len(line) == max_length]
    return largest_lines

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find all horizontal yellow lines
    yellow_lines = find_horizontal_lines(input_grid, 4)

    # Find the largest yellow lines
    largest_yellow_lines = find_largest_lines(yellow_lines)

    # Change the rightmost pixel of the largest lines to orange
    for line in largest_yellow_lines:
        rightmost_pixel = line[-1]
        output_grid[rightmost_pixel[0], rightmost_pixel[1]] = 7

    return output_grid

# Example Usage (assuming task and task.train are defined as per the ARC framework)
reports = []

for example in task.train:  # Assuming 'task' is defined elsewhere
    input_grid = np.array(example['input'])
    expected_output_grid = np.array(example['output'])
    example_report = examine_example(input_grid, expected_output_grid)
    reports.append(example_report)

print (reports)