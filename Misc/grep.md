### 1. `grep` command

- `grep <keyword> <file_name.txt>`
- `cat <file_name.txt> | grep <keyword>`
- `grep <keyword> *.txt`
- `grep <keyword> *.txt -vc`
- `grep -x <div> *.txt`
- `grep '\biv' *.txt`
- `grep -w <iv> *.txt`
- `grep -w B 3 <iv> *.txt`
- `grep -w A 3 <iv> *.txt`

##### Flags:

* `-v`        # Prints all lines that do NOT match pattern.
* `-n`        # Prints the matched line and its line number.
* `-l`        # Prints only the names of files with matching lines
* `-c`        # Prints only the count of matching lines.
* `-i`        # Makes grep searches case insensitive
* `-x`        # Searches the "string" in that file
* `-w`        # Searches only the "string" in that file
* `-\b`        # "string" starting with the keyword (Same as above)
* `-e`        # Excludes the flag
* `-B`        # Searches the number of line BEFORE the keyword
* `-A`        # Searches the number of line AFTER the keyword
* `-C`        # Searches the number of line CONTEXT/CIRCA the keyword

### 2. RegEx

- `$cat example.txt | grep '^keyword'`
- `$cat example.txt | grep 'keyword$'`
- `$cat example.txt | grep '^keyword$'`
- `$grep -E '([0-9]{3}\.){3}[0-9]{1,3}' 'logs.txt'`

##### Flags:

* `^`            # Matches START of the line
* `$`            # Matches END of the line
* `I`            # OR
* `[0-9]`        # range
* `([0-9]{3}\.){3}[0-9]{1,3}`        # First 3 octets with 3 digits. Last octet can be of 1, 2 or 3 digits

### 3. `sort` Command

* `-n`        # Sorts numerically. (Ignores blanks and tabs.)
* `-r`        # Reverses the order of sort.
* `-f`        # Sorts upper and lowercase together.
* `+x`        # Ignores first x fields when sorting.

> Below example will sort the files based on its size, modified in Aug month
> +4 is ignoring first 4 fileds here

```
$ls -l | grep "Aug" | sort +4n
-rw-rw-r--  1 carol doc      1605 Aug 23 07:35 macros
-rw-rw-r--  1 john  doc      2488 Aug 15 10:51 intro
-rw-rw-rw-  1 john  doc      8515 Aug  6 15:30 ch07
-rw-rw-rw-  1 john  doc     11008 Aug  6 14:10 ch02
$
```
