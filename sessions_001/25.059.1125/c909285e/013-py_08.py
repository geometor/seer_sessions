import numpy as np

def find_framing_object(grid):
    """
    Finds the largest contiguous object that encloses other pixels.
    """
    unique_colors = np.unique(grid)
    largest_object = None
    max_area = 0

    for color in unique_colors:
        rows, cols = np.where(grid == color)
        if rows.size == 0:
            continue

        min_row, max_row = np.min(rows), np.max(rows)
        min_col, max_col = np.min(cols), np.max(cols)
        
        #check if there are other colors within this bounding box
        has_enclosed_pixels = False
        for r in range(min_row + 1, max_row):
            for c in range(min_col + 1, max_col):
                if grid[r,c] != color:
                    has_enclosed_pixels = True
                    break
            if has_enclosed_pixels:
                break
        
        if has_enclosed_pixels:
          area = (max_row - min_row + 1) * (max_col - min_col + 1)
          if area > max_area:
              max_area = area
              largest_object = (min_row, max_row, min_col, max_col, color)

    return largest_object

def get_enclosed_pixels(grid, frame_bbox):
    """Extracts pixels inside the frame, along with their coordinates relative to the frame."""
    min_row, max_row, min_col, max_col, frame_color = frame_bbox
    enclosed_pixels = []
    for r in range(min_row + 1, max_row):
        for c in range(min_col + 1, max_col):
            if grid[r, c] != frame_color:
                enclosed_pixels.append((r - min_row -1, c - min_col - 1, grid[r, c])) # Store relative coordinates and color
    return enclosed_pixels

def find_adjacent_frame_pixel(grid, frame_bbox, enclosed_pixels):
    """Finds a frame pixel adjacent to the enclosed pixels."""
    min_row, max_row, min_col, max_col, frame_color = frame_bbox
    
    # Convert enclosed pixel coordinates to absolute coordinates
    enclosed_abs = [(r + min_row + 1, c + min_col + 1) for r, c, _ in enclosed_pixels]

    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if grid[r, c] == frame_color:
                # Check for adjacency to any enclosed pixel
                for er, ec in enclosed_abs:
                    if (abs(r - er) <= 1 and abs(c - ec) <= 1) and (abs(r-er) + abs(c-ec) > 0) :
                        return (r - min_row -1 , c - min_col - 1)  # Return relative coordinates
    return None

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the framing object
    frame_bbox = find_framing_object(input_grid)
    if frame_bbox is None:
        return None  # Or handle cases with no framing object

    # Extract pixels inside the frame
    enclosed_pixels = get_enclosed_pixels(input_grid, frame_bbox)
    if not enclosed_pixels:
        return None

    # Determine output grid size based on enclosed pixels, adding 1 for possible frame inclusion.
    max_r = max(r for r, _, _ in enclosed_pixels)
    max_c = max(c for _, c, _ in enclosed_pixels)

    #check for frame inclusion
    all_same_color = all(color == enclosed_pixels[0][2] for _, _, color in enclosed_pixels)
    
    if all_same_color:
        frame_pixel = find_adjacent_frame_pixel(input_grid, frame_bbox, enclosed_pixels)
        if frame_pixel is not None:
            #adjust grid size
            max_r = max(max_r, frame_pixel[0])
            max_c = max(max_c, frame_pixel[1])

    
    output_grid = np.zeros((max_r + 1, max_c + 1), dtype=int)
    

    # Fill the output grid with the enclosed pixels
    for r, c, color in enclosed_pixels:
        output_grid[r, c] = color


    # Conditionally add a frame pixel
    if all_same_color:
        if frame_pixel is not None:
          output_grid[frame_pixel[0], frame_pixel[1]] = frame_bbox[4]

    return output_grid.tolist()


task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [5, 0, 0, 0, 0, 0, 0, 5], [5, 0, 0, 0, 0, 0, 0, 5], [5, 0, 0, 0, 0, 0, 0, 5], [5, 0, 0, 0, 0, 0, 0, 5], [5, 0, 0, 0, 0, 0, 0, 5], [5, 5, 5, 5, 5, 5, 5, 5]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0], [0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [4, 0, 0, 0, 0, 4], [4, 4, 4, 4, 4, 4]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0], [0, 0, 0, 0], [8, 0, 0, 8], [8, 0, 0, 8], [8, 0, 0, 8], [8, 8, 8, 8]]
        },
        {
            "input": [[6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0], [6, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 6, 6, 6], [6, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 6, 0, 6], [6, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 6, 6, 6], [6, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0], [6, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0], [6, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0], [6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 6], [0, 0, 0, 0, 6], [0, 0, 0, 0, 6], [0, 0, 0, 0, 6], [0, 0, 0, 0, 6], [0, 0, 0, 0, 6]]
        }

    ],
    "test": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0], [0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0], [7, 0, 0, 0, 0, 7], [7, 0, 0, 0, 0, 7], [7, 0, 0, 0, 0, 7], [7, 7, 7, 7, 7, 7]]
        }
    ]
}

for i, example in enumerate(task["train"]):
    input_grid = example["input"]
    expected_output = example["output"]
    
    # Convert to numpy arrays for easier handling
    input_grid_np = np.array(input_grid)
    expected_output_np = np.array(expected_output)
    
    # Get the transformed output
    transformed_output_np = transform(input_grid)

    print(f"Example {i+1}:")
    print(f"  Input:\n{input_grid_np}")
    if transformed_output_np is not None:
        print(f"  Transformed Output:\n{np.array(transformed_output_np)}")
    else:
        print("  Transformed Output: None")
    print(f"  Expected Output:\n{expected_output_np}")
    
    #get intermediate data
    frame_bbox = find_framing_object(input_grid_np)
    print(f" frame_bbox: {frame_bbox}")
    if frame_bbox is not None:
        enclosed_pixels = get_enclosed_pixels(input_grid_np, frame_bbox)
        print(f" enclosed_pixels: {enclosed_pixels}")
        all_same_color = all(color == enclosed_pixels[0][2] for _, _, color in enclosed_pixels)
        if all_same_color:
          frame_pixel = find_adjacent_frame_pixel(input_grid_np, frame_bbox, enclosed_pixels)
          print(f" frame_pixel: {frame_pixel}")
    
    if transformed_output_np is not None:
      print(f"  Correct: {np.array_equal(np.array(transformed_output_np), expected_output_np)}")
    else:
      print(f"  Correct: False")

    print("-" * 20)