
## example 1
*input:*
```
0 7 0
0 0 7
0 7 7
```
*expected output:*
```
0 7 0 0 7 0
0 0 7 7 0 0
0 7 7 7 7 0
```
*transformed output:*
```
0 7 0 7 7
0 0 7 0 0
0 7 7 0 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
0 0 0
0 7 7
0 0 0
```
*expected output:*
```
0 0 0 0 0 0
0 7 7 7 7 0
0 0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0
0 7 7 0 0
0 0 0 0 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 3
*input:*
```
0 0 0
7 0 0
0 0 0
```
*expected output:*
```
0 0 0 0 0 0
7 0 0 0 0 7
0 0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0 0 0
7 0 0 0 0 0 0
0 0 0 0 0 0 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**
