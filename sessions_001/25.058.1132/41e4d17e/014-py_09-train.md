
## example 1
*input:*
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 1 8 8 8 8 8 8 8
8 8 8 1 8 8 8 1 8 8 8 8 8 8 8
8 8 8 1 8 8 8 1 8 8 8 8 8 8 8
8 8 8 1 8 8 8 1 8 8 8 8 8 8 8
8 8 8 1 1 1 1 1 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
*expected output:*
```
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 1 8 8 8 8 8 8 8
8 8 8 1 8 6 8 1 8 8 8 8 8 8 8
6 6 6 1 6 6 6 1 6 6 6 6 6 6 6
8 8 8 1 8 6 8 1 8 8 8 8 8 8 8
8 8 8 1 1 1 1 1 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
```
*transformed output:*
```
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 1 1 1 1 1 6 6 6 6 6 6 6
6 6 6 1 6 6 6 1 6 6 6 6 6 6 6
6 6 6 1 6 6 6 1 6 6 6 6 6 6 6
6 6 6 1 6 6 6 1 6 6 6 6 6 6 6
6 6 6 1 1 1 1 1 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```
size: True
palette: True
color count: False
pixels off: 184
**FAILED!**

## example 2
*input:*
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 1 8 8 8 8 8 8 8
8 8 8 1 8 8 8 1 8 8 8 8 8 8 8
8 8 8 1 8 8 8 1 8 8 8 8 8 8 8
8 8 8 1 8 8 8 1 8 8 8 8 8 8 8
8 8 8 1 1 1 1 1 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 1 1 1 1 1 8 8
8 8 8 8 8 8 8 8 1 8 8 8 1 8 8
8 8 8 8 8 8 8 8 1 8 8 8 1 8 8
8 8 8 8 8 8 8 8 1 8 8 8 1 8 8
8 8 8 8 8 8 8 8 1 1 1 1 1 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
*expected output:*
```
8 8 8 8 8 6 8 8 8 8 6 8 8 8 8
8 8 8 8 8 6 8 8 8 8 6 8 8 8 8
8 8 8 8 8 6 8 8 8 8 6 8 8 8 8
8 8 8 1 1 1 1 1 8 8 6 8 8 8 8
8 8 8 1 8 6 8 1 8 8 6 8 8 8 8
6 6 6 1 6 6 6 1 6 6 6 6 6 6 6
8 8 8 1 8 6 8 1 8 8 6 8 8 8 8
8 8 8 1 1 1 1 1 8 8 6 8 8 8 8
8 8 8 8 8 6 8 8 8 8 6 8 8 8 8
8 8 8 8 8 6 8 8 1 1 1 1 1 8 8
8 8 8 8 8 6 8 8 1 8 6 8 1 8 8
6 6 6 6 6 6 6 6 1 6 6 6 1 6 6
8 8 8 8 8 6 8 8 1 8 6 8 1 8 8
8 8 8 8 8 6 8 8 1 1 1 1 1 8 8
8 8 8 8 8 6 8 8 8 8 6 8 8 8 8
```
*transformed output:*
```
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 1 1 1 1 1 6 6 6 6 6 6 6
6 6 6 1 6 6 6 1 6 6 6 6 6 6 6
6 6 6 1 6 6 6 1 6 6 6 6 6 6 6
6 6 6 1 6 6 6 1 6 6 6 6 6 6 6
6 6 6 1 1 1 1 1 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 1 1 1 1 1 6 6
6 6 6 6 6 6 6 6 1 6 6 6 1 6 6
6 6 6 6 6 6 6 6 1 6 6 6 1 6 6
6 6 6 6 6 6 6 6 1 6 6 6 1 6 6
6 6 6 6 6 6 6 6 1 1 1 1 1 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```
size: True
palette: True
color count: False
pixels off: 145
**FAILED!**
