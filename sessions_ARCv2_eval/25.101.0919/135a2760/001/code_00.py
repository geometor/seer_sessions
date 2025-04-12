import copy
from collections import Counter

"""
The transformation rule identifies specific rows in the input grid that contain a repeating horizontal pattern flanked by a specific color (Red=2). It then determines the intended repeating unit of the pattern within that row, considering a 'frame' color (usually the border color of the grid/section) and a 'pattern' color specific to that row. Finally, it corrects any deviations within the pattern segment of the row in the output grid to strictly follow the identified repeating pattern unit.

1.  **Initialize Output:** Create an exact copy of the input grid.
2.  **Iterate Rows:** Go through each row `r` of the grid.
3.  **Identify Pattern Rows:** Check if the row `r` has Red (2) pixels at column 1 and column `width-2`. These define the boundaries of the pattern segment.
4.  **Process Pattern Rows:** If it is a pattern row:
    a.  **Extract Segment and Colors:** Get the sequence of pixels between the Red markers (columns 2 to `width-3`). Identify the Frame Color `F` (typically `grid[r][0]`) and the Pattern Color `P` (the other dominant color in the segment, excluding `F`).
    b.  **Determine Dominant Pattern Unit:** Analyze the segment to find the most likely repeating unit (`PUnit`) composed of `F` and `P`. This is done by testing short potential pattern units (lengths 1 to 6) and selecting the one that matches the most pixels in the segment. If there's a tie in match count, the shortest pattern unit is preferred.
    c.  **Correct the Segment:** Iterate through the segment columns (2 to `width-3`). For each column `c`, calculate the expected color based on the `PUnit` and the position within the pattern (`(c - 2) % len(PUnit)`). Update the corresponding pixel in the output grid with this expected color.
5.  **Return Output:** Return the modified grid.
"""

def _determine_pattern_unit(segment: list[int], frame_color: int) -> list[int] | None:
    """
    Analyzes a segment to find the most likely repeating pattern unit.

    Args:
        segment: The list of pixel values in the row segment.
        frame_color: The frame color F.

    Returns:
        The determined pattern unit (list of ints) or None if no pattern is found.
    """
    if not segment:
        return None

    # Find unique colors in the segment, exclude frame_color and potential boundary color (2)
    # Although boundary color 2 shouldn't be in the segment itself.
    unique_colors = set(segment)
    pattern_colors = [c for c in unique_colors if c != frame_color]

    # Expecting frame_color and one pattern_color, maybe more if highly corrupted.
    # Heuristic: use the first identified pattern color if multiple exist, or just the frame color if none else exist
    # This part might need refinement if segments can contain >2 colors legitimately.
    # For now, we assume the pattern is made of frame_color and *at most* one other color.

    best_pattern = None
    max_score = -1
    min_len_for_max_score = float('inf')

    # Limit pattern search length to avoid excessive computation and overfitting short segments
    max_pattern_len = min(len(segment), 6)

    for length in range(1, max_pattern_len + 1):
        if length > len(segment):
            continue

        candidate_pattern = segment[:length]

        # Check if the candidate pattern contains only expected colors (F and P)
        # This check might be too strict if the start of the segment is corrupted.
        # Let's relax this for now and rely purely on the score.
        # allowed_colors = {frame_color}
        # if pattern_colors:
        #     allowed_colors.add(pattern_colors[0]) # Assuming one main pattern color P
        # if not all(c in allowed_colors for c in candidate_pattern):
        #     continue

        # Score the candidate pattern by counting matches
        score = 0
        for i, pixel in enumerate(segment):
            expected_pixel = candidate_pattern[i % length]
            if pixel == expected_pixel:
                score += 1

        # Update best pattern if this one is better
        if score > max_score:
            max_score = score
            best_pattern = candidate_pattern
            min_len_for_max_score = length
        elif score == max_score:
            # If scores are equal, prefer the shorter pattern
            if length < min_len_for_max_score:
                best_pattern = candidate_pattern
                min_len_for_max_score = length

    return best_pattern


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Identifies rows with specific patterns flanked by Red(2) pixels and corrects
    deviations within those patterns based on the most frequent repeating unit.
    """
    # Initialize output_grid as a deep copy of input_grid
    output_grid = [row[:] for row in input_grid]
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width < 4: # Need at least 4 columns for pattern rows (F, 2, P..., 2, F)
        return output_grid

    # Iterate through each row
    for r in range(height):
        # Check if the row is a potential pattern row
        # It needs Red(2) markers at columns 1 and width-2
        if input_grid[r][1] == 2 and input_grid[r][width - 2] == 2:
            # Extract the segment between the markers
            segment = input_grid[r][2 : width - 2]
            if not segment: # Skip if segment is empty
                continue

            # Determine the frame color (usually the color in column 0)
            frame_color = input_grid[r][0] # Assuming frame color is consistent

            # Determine the repeating pattern unit for this segment
            pattern_unit = _determine_pattern_unit(segment, frame_color)

            # If a pattern unit was successfully determined
            if pattern_unit:
                pattern_len = len(pattern_unit)
                # Correct the segment in the output grid
                for c in range(2, width - 2):
                    # Calculate the index within the pattern unit
                    pattern_index = (c - 2) % pattern_len
                    # Get the expected color from the pattern unit
                    expected_color = pattern_unit[pattern_index]
                    # Update the output grid
                    output_grid[r][c] = expected_color

    return output_grid