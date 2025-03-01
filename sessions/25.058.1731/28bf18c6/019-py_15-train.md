
## example 1
*input:*
```
0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0
0 0 8 0 0 0 0 0
0 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```
*expected output:*
```
8 8 0 8 8 0
0 8 0 0 8 0
8 8 8 8 8 8
```
*transformed output:*
```
8 8 0
0 8 0
8 8 8
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0
0 0 2 2 2 0 0 0
0 0 2 2 0 0 0 0
```
*expected output:*
```
0 2 0 0 2 0
2 2 2 2 2 2
2 2 0 2 2 0
```
*transformed output:*
```
0 2 0
2 2 2
2 2 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 0
0 0 0 0 1 0 0 0
0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```
*expected output:*
```
0 1 1 0 1 1
1 0 0 1 0 0
0 1 0 0 1 0
```
*transformed output:*
```
0 1 1
1 0 0
0 1 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**
