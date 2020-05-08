#!/usr/bin/python3
import argparse
from argparse import RawTextHelpFormatter
import csv
import sys
import re
from collections import Counter
import io
def open_file(file_name):
    if file_name == sys.stdin:
        return sys.stdin
    else:
        try:
            fr = open(file_name,'r')
            return fr
        except:
            print("Error: Can not open file {}".format(file_name))
            exit(-1)


def main():
    VERSION = '0.2'
    desc = '''Small program to parse .CSV files.\nWritten by s.maroofi (maroofi@gmail.com)\nVersion {}'''.format(VERSION)

    parser = argparse.ArgumentParser(description=desc,formatter_class=RawTextHelpFormatter)    
    
    parser.add_argument('-v','--version',
                        action='version',
                        version='CSVTOOL version {}. Use --help to see logn description.'.format(VERSION)
    )
    
    parser.add_argument('-l','--line-number',
                        action='store_true',
                        default=False,
                        dest='print_linenum',
                        help="Prints line number for each output line (the line numbers are based on the file line number)."
    )
    parser.add_argument('-c','--column',
                        action='store',
                        default='',
                        dest='column',
                        help="Select specific column(s) in the form of 1,2,.. or 1-3 or 4 or 1,2,3-6,7\n or any combination of values/ranges and perform all operation on these columns (default is all columns)"
    )

    parser.add_argument('-t','--stat',
                        action='store_true',
                        default=False,
                        dest='stat',
                        help="Print some useful statistics about the CSV file."
    )
    parser.add_argument('-e','--no-header',
                        action='store_true',
                        default=False,
                        dest='noheader',
                        help="Specifies that input .CSV file has no header."
    )
    parser.add_argument('-s','--search',
                        action='store',
                        dest='search',
                        default='',
                        help="""Search for a specific python regex pattern (optionally\n on specific columns specified by --column or all columns).\nIf (?i) specified, the search is case-insensitive.\nExample:\n# matches test, Test, TeSt, ...\n csvtool output.csv --search '(?i)test'\n# matches all the lines which have exactly 'US' value in their second columns.\n   csvtool output.csv --column 2 --search '^US$'\n# matches all the lines which have not 'Hello' in their second columns.  \n csvtool output.csv -c 2 -s '^(?:(?!Hello).)*$'  """
    )
    parser.add_argument('-r','--print-header',
                        action='store_true',
                        dest='print_header',
                        default=False,
                        help="Prints the header of the .CSV file"
    )
    parser.add_argument("-m",'--most-common',
                        action='store',
                        dest='most_common',
                        default='-1',
                        help='Prints n most common values for each column'
    )
       
    parser.add_argument("-d",'--delimiter',
                        action='store',
                        dest='delimiter',
                        default=',',
                        help='Specifies the delimiter used in CSV file (default is comma character)'
    )
    parser.add_argument("file",
                        action='store',
                        default=sys.stdin,
                        nargs='?',
                        help=".CSV input file name")   
       
    pargs = parser.parse_args(sys.argv[1:])
    fr = open_file(pargs.file)
    reader = csv.reader(fr,quotechar='"',delimiter=pargs.delimiter,quoting=csv.QUOTE_ALL,skipinitialspace=True)
    header = []
    line_num = 1
    re_search = ''
    ##################parsing search#################
    #################parsing header####################
    if(pargs.noheader):
        header = []
    else:
        header = reader.__next__()
        header = [x.strip() for x in header]
    #end if
    ##################parsing print_linenum###########
    print_linenum = pargs.print_linenum
    ####################parsing print args#############
    if pargs.print_header:
        if(pargs.noheader == False):
            _ = [print("{} - {}".format(i+1,header[i])) for i in range(len(header))]
            fr.close()
            return True
        fr.close()
        return False
        #end if
    ####################parsing column#######################
    cols = []
    if pargs.column != '':
        cl = pargs.column.split(",")
        cl = [x.strip() for x in cl if x.strip() != '']
        for x in cl:
            if x.find("-") != -1:
                temp = x.split("-")
                if(len(temp)==2):
                    st = None;en = None;
                    try:
                        st = int(temp[0].strip())
                        en = int(temp[1].strip())
                    except:
                        print("ERROR: --column/-c should be start-end or colX,colY,.. or just colX starting from 1.")
                        return False
                    if en < st:
                        print("ERROR: --column/-c should be in the form fo start-end (start > end) or colX,colY,.. or just colZ starting from 1.")
                        return False
                    if st<1:
                        print("ERROR: --column/-c should be start-end or colX,colY,.. or just colX starting from 1.")
                        return False
                    cols += list(range(st-1,en))
                else:
                    print("ERROR: --column/-c should be start-end or colX,colY,.. or just colX starting from 1.")
                    return False
                # end if
            else:
                try:
                    if int(x.strip())<1:
                        print("ERROR: --column/-c should be start-end or colX,colY,.. or just colX starting from 1.")
                        return False
                    cols.append(int(x.strip())-1)
                except:
                    print("ERROR: --column/-c should be a number/range separated by comma")
                    return False
            #end if
    #end if
    tmp_cols = []
    for x in cols:
        if x not in tmp_cols:
            tmp_cols.append(x)
    cols = tmp_cols
    #print(cols)
    ###################parsing stat#########################
    stat = pargs.stat
    ##################parsing most_common###################
    try:
        most_common = int(pargs.most_common)  #no means -1
    except:
        print("ERROR: --most-common/-m value should be an integer greater than zero")
        return False
    ########################################################
    # now go through switches one by one.
    # the first one is stat, if stat is true -> print statistics and exit peacefully
    try:
        if stat == True:
            data = []
            for line in reader:
                data.append(line)
            fr.close()
            print("File name: {}".format(pargs.file))
            print("Number of entries: {}".format(len(data)))
            if pargs.noheader == False:
                print("Headers of CSV")
                print("--------------")
                print(create_write_object(pargs.delimiter,header))
            if len(data) == 0:return False
            col_cnt = len(data[0])
            for x in data:
                if len(x) != col_cnt:
                    print("CSV records have different column length(probably malformed): {}, {}".format(col_cnt,len(x)))
                    return False
            col_dict = dict()
            print("----------------")
            print("Most common value for each column")
            print("----------------")
            for i in range(len(data[0])):
                col_cnt = []
                for line in data:
                    col_cnt.append(line[i])
                header_name = header[i] if pargs.noheader == False else i+1
                col_cnt = Counter(col_cnt).most_common()
                print("Col '{}' - {} unique value(s):".format(header_name,len(col_cnt)))
                print("--------most common(s)--------")
                _ = [print("\tValue: '{}' - Count: '{}'".format(col_cnt[z][0],col_cnt[z][1])) for z in range(len(col_cnt)) if z < 3 ];
                print("------------------------------")
            #end for
            return True
        #end if
    except IOError as e:
        return False
    # end except
    #then handle search query for columns
    #only search the specified columns for pattern otherwise all columns.
    try:
        re_search = None
        if pargs.search != '':
            re_search = re.compile(pargs.search)
        if pargs.search != '':
            if re_search == None:return False
            ln = 0 if pargs.noheader == True else 1
            if not pargs.noheader: # print header if there is
                print("{}".format(create_write_object(pargs.delimiter,header)))
            for line in reader:
                ln += 1
                if len(cols) == 0:
                    for c in line:
                        if re_search.search(c) != None:
                            if print_linenum:
                                print("{} - {}".format(ln,create_write_object(pargs.delimiter,line)))
                                break
                            else:
                                print("{}".format(create_write_object(pargs.delimiter,line)))
                                break
                            #end if
                        #end if
                    #end for
                else:
                    for c in cols:
                        if re_search.search(line[c]) != None:
                            if print_linenum:
                                print("{} - {}".format(ln,create_write_object(pargs.delimiter,line)))
                                break
                            else:
                                print("{}".format(create_write_object(pargs.delimiter,line)))
                                break
                            #end if
                        #end if
                    #end for
                #end if
            #end for
            fr.close()
            return True
        #end if
    except IOError as e:
        return False
    # end except
    #Now handle most common
    #Print n most common values for cols (or all)
    try:
        if most_common != -1:
            col_cnt = dict()
            if len(cols)>0:
                data = []
                for line in reader:
                    data.append(line)
                fr.close()
                if len(data) == 0:return False
                for c in cols:
                    cnt_cols = [x[c] for x in data]
                    cnt_cols = Counter(cnt_cols).most_common()
                    header_name = header[c] if pargs.noheader == False else c+1
                    print("------column: {}------".format(header_name))
                    _ = [print("Value: '{}' - Count: '{}'".format(cnt_cols[z][0],cnt_cols[z][1])) for z in range(len(cnt_cols)) if z < most_common];
                #end for
                return True
            else:
                data = []
                for line in reader:
                    data.append(line)
                fr.close()
                tmp_cols = [i for i in range(len(data[0]))]
                
                for c in tmp_cols:
                    cnt_cols = [x[c] for x in data]
                    cnt_cols = Counter(cnt_cols).most_common()
                    header_name = header[c] if pargs.noheader == False else c+1
                    print("------column: {}------".format(header_name))
                    _ = [print("Value: '{}' - Count: '{}'".format(cnt_cols[z][0],cnt_cols[z][1])) for z in range(len(cnt_cols)) if z < most_common];
                #end for
                return True
            #end if
            return True
        #end if
    except IOError as e:
        return False
    # end except
    ## if nothing specified, print csv file (all or specific columns)
    ## with header (if there is one) with all or specific columns
    try:
        ln = 0 if pargs.noheader == True else 1
        if not pargs.noheader:
            if len(cols) == 0:
                print("{}".format(create_write_object(pargs.delimiter,header)))
            else:
                print("{}".format(create_write_object(pargs.delimiter,[header[c] for c in cols])))
        for line in reader:
            ln += 1
            if len(cols) == 0:
                if print_linenum:
                    print("{} - {}".format(ln,create_write_object(pargs.delimiter,line)))
                else:
                    print("{}".format(create_write_object(pargs.delimiter,line)))
            else:
                if print_linenum:
                    print("{} - {}".format(ln,create_write_object(pargs.delimiter,[line[c] for c in cols])))
                else:
                    print("{}".format(create_write_object(pargs.delimiter,[line[c] for c in cols])))
            #end if
        fr.close()
        return True
    except IOError as e:
        return False
    # end except

def create_write_object(delimiter,write_array):
    data = io.StringIO()
    writer = csv.writer(data,delimiter=delimiter,quoting=csv.QUOTE_MINIMAL,skipinitialspace=True)
    writer.writerow(write_array)
    return data.getvalue().strip()

if __name__ == "__main__":
    main()
