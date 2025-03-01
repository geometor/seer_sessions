
## example 1
*input:*
```
0 0 0 0 0
0 2 0 0 0
0 0 0 0 0
```
*expected output:*
```
3 0 6 0 0
0 0 0 0 0
8 0 7 0 0
```
*transformed output:*
```
3 0 6 0
0 0 0 0
8 0 7 0
0 0 0 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 2
```
*expected output:*
```
0 0 0 0 0
0 0 0 3 0
0 0 0 0 0
```
*transformed output:*
```
3 0 6 0
0 0 0 0
8 0 7 0
0 0 0 0
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 3
*input:*
```
0 0 2 0 0
0 0 0 0 0
0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0
0 8 0 7 0
0 0 0 0 0
```
*transformed output:*
```
3 0 6 0
0 0 0 0
8 0 7 0
0 0 0 0
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 4
*input:*
```
0 0 0 0 0
0 0 0 2 0
0 0 0 0 0
```
*expected output:*
```
0 0 3 0 6
0 0 0 0 0
0 0 8 0 7
```
*transformed output:*
```
3 0 6 0
0 0 0 0
8 0 7 0
0 0 0 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**
