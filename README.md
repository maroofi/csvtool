# csvtool
#### Command-line utility to work with .CSV files in bash.

##### Installation:

###### Using pypi:
```bash
pip3 install csvtool
```
###### Directly using Git repo:
```bash
git clone https://github.com/maroofi/csvtool.git

cd csvtool

python3 setup.py install --user
```
Note: To use it independetly as a command-line tool, make sure you have ~/.local/bin in $PATH variable.

1. Change to your home directory by: cd $HOME
2. Open the .bashrc file.
3. Add the following line to the file.
```
export PATH=~/.local/bin/:$PATH
```
4. Save the file and exit
5. then use:
```
source .bashrc
```
#### Example:
```bash
csvtool -h
```
Show the long version of the help for more information.

Sample test.csv file:

Year | Make | Model | Description | Price
-----|------|-------|-------------|------
1997|Ford|E350|"ac, abs, moon"|3000.00
1999|Chevy|"Venture ""Extended Edition"""|""|4900.00
1999|Chevy|"Venture ""Extended Edition, Very Large"""| |5000.00
1996|Jeep|Grand Cherokee|"MUST SELL! air, moon roof, loaded"|4799.00

1. Select all the 'Chevy' car and show the year, price and model:
```bash
csvtool -c 2 -s '^Chevy$' test.csv | csvtool --no-header -c 1,5,3
```
output:

```
Year,Price,Model
1999,4900.00,"Venture ""Extended Edition"""
1999,5000.00,"Venture ""Extended Edition, Very Large"""
```

2. Select only year and name of the cars:
```bash
csvtool -c 1,2 test.csv
```
output:

```
Year,Make
1997,Ford
1999,Chevy
1999,Chevy
1996,Jeep
```

#### TODO LIST
1. ~~Add header to the output.~~ :heavy_check_mark:
2. Add replace command to replace some specific values.
