# 2dd70a9a • 001 • all training • investigate_dreamer

---


## train_1

**input:**
```
0 0 0 0 8 8 8 8 8 0 0 8 0 8 8 8 0 8 0 8
0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 8 0 0 0 0
8 8 8 8 8 0 8 0 8 0 0 0 8 8 8 0 0 2 0 0
8 0 8 8 0 0 0 0 0 0 8 8 8 8 8 8 0 2 0 0
8 0 0 8 8 0 0 0 0 0 0 8 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8
8 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 8
0 0 0 0 0 0 0 0 0 8 0 0 8 0 0 0 0 0 8 8
0 8 0 0 0 0 8 8 8 0 8 0 0 8 0 8 8 0 0 0
8 0 0 0 0 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 8 8 8 0 0 8 8 8 0 8 0 0 8 8
0 0 0 0 0 0 8 8 0 0 0 0 8 0 0 0 8 0 0 8
0 0 0 3 0 0 0 8 0 8 0 8 0 0 8 0 0 8 0 8
0 0 0 3 0 0 8 8 8 0 0 0 8 8 8 8 0 0 0 0
0 8 0 0 0 0 0 8 0 8 8 0 8 0 8 0 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0 8 0 0 0 0 0 8 8 0
0 0 0 8 0 0 0 8 0 8 0 0 8 8 8 0 0 0 0 8
0 0 0 0 8 8 8 8 0 0 8 0 0 0 0 8 8 8 0 0
```

<PIL.Image.Image image mode=RGB size=1280x1280 at 0x7C360454EFD0>

**output:**
```
0 0 0 0 8 8 8 8 8 0 0 8 0 8 8 8 0 8 0 8
0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 8 0 0 0 0
8 8 8 8 8 0 8 0 8 0 0 0 8 8 8 0 0 2 0 0
8 0 8 8 0 0 0 0 0 0 8 8 8 8 8 8 0 2 0 0
8 0 0 8 8 0 0 0 0 0 0 8 0 8 0 0 0 3 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0 8 0 0 0 3 0 0
8 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 8 0
0 0 8 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8
8 0 0 3 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 8
0 0 0 3 0 0 0 0 0 8 0 0 8 0 0 0 0 0 8 8
0 8 0 3 0 0 8 8 8 0 8 0 0 8 0 8 8 0 0 0
8 0 0 3 0 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8
0 0 0 3 0 0 8 8 8 0 0 8 8 8 0 8 0 0 8 8
0 0 0 3 0 0 8 8 0 0 0 0 8 0 0 0 8 0 0 8
0 0 0 3 0 0 0 8 0 8 0 8 0 0 8 0 0 8 0 8
0 0 0 3 0 0 8 8 8 0 0 0 8 8 8 8 0 0 0 0
0 8 0 0 0 0 0 8 0 8 8 0 8 0 8 0 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0 8 0 0 0 0 0 8 8 0
0 0 0 8 0 0 0 8 0 8 0 0 8 8 8 0 0 0 0 8
0 0 0 0 8 8 8 8 0 0 8 0 0 0 0 8 8 8 0 0
```

<PIL.Image.Image image mode=RGB size=1280x1280 at 0x7C360455E0D0>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 8
0 3 8 0 0 0 0 0 0 0
0 3 0 0 0 0 0 8 0 0
0 0 0 0 0 0 8 0 0 8
0 8 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 8 8 0 0 2 0 0 0 0
0 0 8 0 0 2 0 0 0 0
0 0 8 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360455C850>

**output:**
```
0 0 0 0 0 0 0 0 0 8
0 3 8 0 0 0 0 0 0 0
0 3 0 0 0 0 0 8 0 0
0 3 3 3 3 3 8 0 0 8
0 8 0 8 0 3 0 0 0 0
0 0 0 8 0 3 0 0 0 0
0 8 8 0 0 2 0 0 0 0
0 0 8 0 0 2 0 0 0 0
0 0 8 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360BFEABD0>

## train_3

**input:**
```
0 0 0 0 0 8 0 8 0 0 8 0 0 8 0
0 0 0 8 0 0 8 0 0 0 0 8 0 8 8
8 0 0 0 8 8 8 0 0 0 0 8 8 8 0
0 0 0 0 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 8 0
0 3 3 0 0 0 0 0 8 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0 8 0
0 8 8 0 0 8 0 0 8 0 8 8 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
8 2 2 0 0 0 0 0 0 0 0 0 0 8 0
8 0 0 0 0 0 0 8 8 8 0 0 0 0 0
0 8 0 0 8 0 8 0 0 0 8 8 8 8 0
0 0 0 0 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 8 0 0 8 0 0 8
0 8 0 0 8 8 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=960x960 at 0x7C36045DF1D0>

**output:**
```
0 0 0 0 0 8 0 8 0 0 8 0 0 8 0
0 0 0 8 0 0 8 0 0 0 0 8 0 8 8
8 0 0 0 8 8 8 0 0 0 0 8 8 8 0
0 0 0 0 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 8 0
0 3 3 3 3 3 3 3 8 0 0 0 8 0 0
0 0 0 0 0 0 0 3 0 0 0 8 0 8 0
0 8 8 0 0 8 0 3 8 0 8 8 0 0 0
0 8 0 0 0 0 0 3 0 0 0 0 0 0 0
8 2 2 3 3 3 3 3 0 0 0 0 0 8 0
8 0 0 0 0 0 0 8 8 8 0 0 0 0 0
0 8 0 0 8 0 8 0 0 0 8 8 8 8 0
0 0 0 0 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 8 0 0 8 0 0 8
0 8 0 0 8 8 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=960x960 at 0x7C360BFEAF50>
<PIL.Image.Image image mode=RGB size=2960x2610 at 0x7C360BFEB350>
**INSTRUCTIONS**

above is an example pair for a task

this is your opportunity to perceive the underlying logic that transforms the
input into the output

respond with the following deliverables:

- your perception of the elements of the task
- a YAML block documenting facts - Focus on identifying objects, their properties, actions performed on them, and the relationships between them
- a natural language program - Be as clear and concise as possible, providing a complete description of the transformation rule.


your responses should be considered as information in a report - not a conversation
