
## example 1
*input:*
```
0 0 0 0 0 0 0 0 0
0 8 0 0 0 8 0 0 8
0 5 0 0 0 5 0 0 0
0 5 0 8 0 5 0 8 0
0 5 0 0 0 5 0 0 0
0 8 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 8 0
0 8 0 0 0 0 0 0 0
```
*expected output:*
```
8 0 0 0 8
5 0 0 0 5
5 0 8 0 5
5 0 0 0 5
8 0 0 0 8
```
*transformed output:*
```
8
5
5
5
8
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 8 0 0 0 8
0 0 0 0 0 0 0 0 0 8 8
0 0 8 0 0 0 0 0 8 0 0
8 0 5 0 0 0 0 0 5 0 0
0 0 5 0 0 8 8 0 5 0 0
0 0 5 0 0 0 0 0 5 0 0
0 0 8 0 8 0 0 0 8 0 0
0 8 0 0 0 0 0 0 8 8 0
```
*expected output:*
```
8 0 0 0 0 0 8
5 0 0 0 0 0 5
5 0 0 8 8 0 5
5 0 0 0 0 0 5
8 0 8 0 0 0 8
```
*transformed output:*
```
0 0 8
0 8 8
8 0 0
5 0 0
5 0 0
5 0 0
8 0 0
8 8 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 8 0 0 0 0 0
0 0 0 5 0 0 0 5 0 8 0 0 0
0 0 8 5 0 8 0 5 0 0 0 0 0
0 0 0 5 0 0 0 5 8 0 0 0 0
0 0 8 5 0 8 0 5 0 0 0 0 0
0 0 0 8 0 0 0 8 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 8 8 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0
```
*expected output:*
```
8 0 0 0 8
5 0 0 0 5
5 0 8 0 5
5 0 0 0 5
5 0 8 0 5
8 0 0 0 8
```
*transformed output:*
```
0 8
0 5
8 5
0 5
8 5
0 8
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**
