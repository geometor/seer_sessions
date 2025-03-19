
## example 1
*input:*
```
0 0 0 8 0 8 0 0 0
0 0 0 0 8 8 0 0 0
0 0 0 0 0 8 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0
```
*expected output:*
```
8 0 8 8 0 8 0 0 0
8 8 0 0 8 8 0 0 0
8 0 0 0 0 8 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0
```
*transformed output:*
```
0 0 0 8 8 8 8 8 8
0 0 0 8 8 8 8 8 8
0 0 0 8 8 8 8 8 8
0 0 0 4 8 8 8 8 8
0 0 0 4 4 4 8 8 8
0 0 0 0 4 0 8 8 8
```
size: True
palette: True
color count: False
pixels off: 29
**FAILED!**

## example 2
*input:*
```
0 0 0 8 0 8 0 0 0
0 0 0 8 8 8 0 0 0
0 0 0 8 8 0 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0
```
*expected output:*
```
0 0 0 8 0 8 8 0 8
0 0 0 8 8 8 8 8 8
0 0 0 8 8 0 0 8 8
0 0 0 0 0 4 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0
```
*transformed output:*
```
0 0 0 8 8 8 8 8 8
0 0 0 8 8 8 8 8 8
0 0 0 8 8 8 8 8 8
0 0 0 8 8 4 8 8 8
0 0 0 4 4 4 8 8 8
0 0 0 0 4 0 8 8 8
```
size: True
palette: True
color count: False
pixels off: 15
**FAILED!**

## example 3
*input:*
```
0 0 0 8 0 0 0 0 0
0 0 0 0 8 8 0 0 0
0 0 0 8 0 0 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0
```
*expected output:*
```
0 0 8 8 0 0 0 0 0
8 8 0 0 8 8 0 0 0
0 0 8 8 0 0 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0
```
*transformed output:*
```
0 0 0 8 8 8 8 8 8
0 0 0 8 8 8 8 8 8
0 0 0 8 8 8 8 8 8
0 0 0 4 8 8 8 8 8
0 0 0 4 4 4 8 8 8
0 0 0 0 4 0 8 8 8
```
size: True
palette: True
color count: False
pixels off: 29
**FAILED!**
