"""
The input grid's dominant repeating horizontal line pattern (background) is identified. Pixels deviating from this pattern (foreground) are detected. A 3x3 output grid is constructed. The output grid's cell colors are determined by the colors of the foreground pixels, following a top-to-bottom, left-to-right order within sections of the input corresponding to output rows. If fewer than 3 foreground pixels are in a section, the remaining cells are 0 (white).
"""

import numpy as np

def find_repeating_pattern_and_disruptions(grid):
    """Finds the repeating horizontal line pattern and disrupting pixels."""
    height, width = grid.shape
    pattern_counts = {}
    disruptions = []

    for r in range(height):
        row_pattern = tuple(grid[r])  # Convert row to tuple for hashing
        if row_pattern in pattern_counts:
            pattern_counts[row_pattern]['count'] += 1
            pattern_counts[row_pattern]['rows'].append(r)

        else:
            pattern_counts[row_pattern] = {'count': 1, 'rows': [r]}

    # Find the most frequent pattern (background)
    dominant_pattern = max(pattern_counts, key=lambda k: pattern_counts[k]['count'])
    dominant_rows = pattern_counts[dominant_pattern]['rows']

    # Find the next two most frequent patterns
    pattern_counts.pop(dominant_pattern)
    
    # Find all disrupting pixels
    for r in range(height):
        for c in range(width):
            if tuple(grid[r]) != dominant_pattern:
                disruptions.append((r, c, grid[r, c]))

    # determine row sections corresponding to 3x3 output
    row_sections = []
    if len(dominant_rows)>0:
       section_size = len(dominant_rows) // 3
       for i in range(3):
            start_index = i * section_size
            if i==2:
               end_index = len(dominant_rows) # take all remaining rows
            else:
               end_index = (i + 1) * section_size
            section_rows = dominant_rows[start_index:end_index]
            row_sections.append(section_rows)

    return dominant_pattern, disruptions, row_sections

def transform(input_grid):
    """Transforms the input grid into a 3x3 output grid."""
    grid = np.array(input_grid)
    dominant_pattern, disruptions, row_sections = find_repeating_pattern_and_disruptions(grid)

    output_grid = np.zeros((3, 3), dtype=int)

    # Populate the output grid based on disruptions in each section
    for i, section_rows in enumerate(row_sections): # process row sections
        section_disruptions = []
        for r, c, color in disruptions:
            if r in section_rows: # is disruption within section?
                section_disruptions.append( (c, color) ) # add disruptions to section
        section_disruptions.sort() # sort by column

        for j in range(min(3, len(section_disruptions))): # take first 3
            output_grid[i, j] = section_disruptions[j][1] # set color

    return output_grid