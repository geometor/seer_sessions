# e509e548 • 015 • example_3 • investigate_dreamer

---


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 3 0 0
0 3 0 0 0 0 0 0 0 3 3 3
0 3 0 0 0 3 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 3 0 3 0 0 0 0
0 0 0 0 0 3 0 3 0 0 0 0
3 3 3 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 3 0 3
0 0 0 0 0 0 0 0 0 3 3 3
```

<PIL.Image.Image image mode=RGB size=768x896 at 0x716635BBB750>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 1 0 0
0 6 0 0 0 0 0 0 0 1 1 1
0 6 0 0 0 6 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 2 0 2 0 0 0 0
0 0 0 0 0 2 0 2 0 0 0 0
1 1 1 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 6 6 6
```

<PIL.Image.Image image mode=RGB size=768x896 at 0x716635BBB550>

**INSTRUCTIONS**

above is an example pair for a task

this is your opportunity to perceive the underlying logic that transforms the
input into the output

respond with the following deliverables:

- your perception of the elements of the task
- a YAML block documenting facts - Focus on identifying objects, their properties, actions performed on them, and the relationships between them
- a natural language program - Be as clear and concise as possible, providing a complete description of the transformation rule.


your responses should be considered as information in a report - not a conversation
