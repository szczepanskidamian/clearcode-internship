import pycountry
import csv
import datetime
import re
import sys
import operator


def csv_report(input_csv, output_csv='output.csv'):
    """Extracting data from input_csv file, converting date format, assigning country code
    and getting number of impressions and number of clicks on ad. All data is saved
    to output_csv file ('output.csv' as default)."""
    subdivisions = pycountry.subdivisions
    countries = pycountry.countries
    output = []

    """Open file with utf-8 encoding to get strings."""
    try:
        with open(input_csv, newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')\


            for row in csv_reader:
                """Converting date from MM/DD/YYYY to YYYY-MM-DD."""
                date = datetime.datetime.strptime(row[0], "%m/%d/%Y").strftime("%Y-%m-%d")
                code = None
                impressions = int(row[2])
                """re.sub used to get rid of '%' sign from ctr, converted to float and divided by 100."""
                ctr = round(impressions * (float(re.sub('%', '', row[3]))/100))

                """Find country_code for every row using state name. If name is not found set code as 'XXX'."""
                for state in subdivisions:
                    if state.name == row[1]:
                        code = state.country_code

                if not code:
                    code = 'XXX'
                else:
                    for country in countries:
                        if country.alpha_2 == code:
                            code = country.alpha_3

                """Adding result to output list."""
                output.append([bytes(date.encode('utf-8')),
                               bytes(code.encode('utf-8')),
                               bytes(str(impressions).encode('utf-8')),
                               bytes(str(ctr).encode('utf-8'))]
                              )
    except:
        (sys.stderr.write("There is a problem with input file."))

    """Sorting list in order of date and country code."""
    output = sorted(output, key=operator.itemgetter(0, 1))

    """As we have sorted list already now we compare element i and i+1 to check 
    if dates and country codes match and if they do, we sum their impressions and clicks on ad
    and we remove element i+1 from list decreasing output_len to prevent IndexOutOfRange error."""
    i = 0
    output_len = len(output)-1
    while i < output_len:
        if output[i][:2] == output[i+1][:2]:
            output[i][2] = str(int(output[i][2]) + int(output[i+1][2])).encode('utf-8')
            output[i][3] = str(int(output[i][3]) + int(output[i+1][3])).encode('utf-8')
            output.remove(output[i+1])
            output_len -= 1
        i += 1

    """Writing our data to file output_csv"""
    f = open(output_csv, 'wb')
    for line in output:
        f.write(','.encode('utf-8').join(line))
        f.write('\n'.encode('utf-8'))
    f.close()


csv_report('input.csv')
