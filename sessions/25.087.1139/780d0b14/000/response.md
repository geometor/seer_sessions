*   **Perception:** The input grids are large and contain multiple distinct rectangular areas separated by solid white (0) lines, either rows or columns. Each non-white area contains patterns made of a single color other than white. The output grids are much smaller and their dimensions correspond to the number of distinct areas in the input grid, arranged according to their relative positions. Each cell in the output grid contains the single non-white color found within the corresponding area in the input grid.

*   **YAML Facts:**
    
```yaml
    task_description: Identify distinct rectangular sections in the input grid separated by white lines and map the single non-white color from each section to a corresponding cell in a smaller output grid representing the layout of the sections.

    elements:
      - element: grid
        description: The input is a 2D grid of pixels.
      - element: pixel
        description: Each cell in the grid, having a color value from 0-9.
      - element: color_white
        value: 0
        description: Used as a background and separator.
      - element: color_non_white
        description: Colors 1 through 9, used to form patterns within sections.
      - element: separator_line
        description: A contiguous line (row or column) consisting entirely of white pixels that separates sections. These lines do not include the grid borders.
      - element: section
        description: A rectangular subgrid area bounded by separator lines or grid borders, containing a pattern of a single non-white color and potentially some white pixels.
      - element: section_layout
        description: The arrangement of sections in the input grid, forming a meta-grid (e.g., 2x3, 2x2).
      - element: representative_color
        description: The single non-white color present within a section.
      - element: output_grid
        description: A smaller grid whose dimensions match the section_layout and whose cells contain the representative_color of the corresponding input section.

    relationships:
      - relationship: separation
        subject: section
        object: section
        description: Sections are separated from each other by separator_lines (rows or columns of white pixels).
      - relationship: containment
        subject: section
        object: representative_color
        description: Each section contains exactly one type of non-white color, which is its representative_color.
      - relationship: correspondence
        subject: section
        object: output_grid_cell
        description: Each section in the input grid corresponds to a specific cell in the output_grid based on its relative position in the section_layout.
      - relationship: representation
        subject: output_grid_cell
        object: representative_color
        description: Each cell in the output grid holds the representative_color of its corresponding section.

    transformation:
      - action: identify_separators
        description: Find all full rows and full columns within the input grid (excluding borders) that consist entirely of white pixels.
      - action: segment_grid
        input: input_grid, separator_lines
        output: list_of_sections, section_layout (rows, columns)
        description: Use the identified separator lines to divide the input grid into distinct rectangular sections and determine their layout.
      - action: identify_representative_color
        input: section
        output: representative_color
        description: For each section, find the single non-white color present within it.
      - action: construct_output
        input: list_of_representative_colors, section_layout
        output: output_grid
        description: Create a new grid with dimensions matching the section_layout and populate each cell with the representative_color from the corresponding section, maintaining the relative positions.
    ```


*   **Natural Language Program:**
    1.  Identify all horizontal separator lines: Scan the input grid rows (excluding the first and last row) to find any row composed entirely of white (0) pixels. Record the indices of these rows.
    2.  Identify all vertical separator lines: Scan the input grid columns (excluding the first and last column) to find any column composed entirely of white (0) pixels. Record the indices of these columns.
    3.  Determine the grid segmentation: The number of horizontal sections is one more than the number of horizontal separator lines found. The number of vertical sections is one more than the number of vertical separator lines found. These numbers define the dimensions (rows x columns) of the output grid.
    4.  Define the boundaries of each section: Use the grid borders and the identified separator line indices to calculate the top-left and bottom-right coordinates of each rectangular section.
    5.  Extract the representative color for each section: Iterate through the identified sections based on their layout (e.g., row by row, column by column). For each section, scan its pixels until the first non-white pixel is found. This pixel's color is the representative color for that section.
    6.  Construct the output grid: Create a new grid with the dimensions determined in step 3. Populate this grid cell by cell, placing the representative color found for each section (in step 5) into the corresponding cell position based on the section's layout.