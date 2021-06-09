'''
Provide an interface for if a date is a holiday in a country 

'''
import csv
import json
from flask import Flask, abort
import holidays


app = Flask(__name__)

@app.before_first_request
def before_first_request():
    """
    Read csv file before first request
    """
    countries = {}
    with open('./holidays.csv', mode='r') as csv_file:
        reader = csv.reader(csv_file)
        i = 0 # skip header
        for rows in reader:
            if i != 0:
                countries[rows[0]] = rows[1]
            i += 1
    return countries

@app.route('/')
def hello():
    return """
        <html><body>
            <h1>Check for holiday</h1>
            Write: http://localhost:8080/ISO/Date to check if a certain date is a holiday in a country.
            <br>
            <br>
            Supported for: <br>
            <b>ISO:</b> 3 characters <br>
            <b>Date:</b> 8 characters <br>
            <br>
            E.g: <br>
            http://localhost:8080/USA/20160101
            
        </body></html>"""
    



@app.route('/<iso>/<holidate>')
def is_holiday(iso, holidate): 
    '''Check if date is holiday in a country

    :param iso: iso code for country
    :type iso: str
    :param holidate: date for holiday check
    :type holidate: str

    '''
    countries = before_first_request()
    if len(iso) != 3:
        abort(400, 'ISO must be 3 characters long.')
    elif iso not in countries:
        abort(400, 'Country is not supported in this calendar.')
    elif len(holidate) != 8:
        abort(400, 'Date must be 8 characters long.')

    year = int(holidate[:4])
    iso_holidays = holidays.CountryHoliday(iso, years=year)

    date_ = f'{holidate[:4]}-{holidate[4:6]}-{holidate[6:]}'
    check = iso_holidays.get(date_)
    is_date_holiday = False

    # Handle case where Sweden and Norway count Sunday as holiday
    if check is not None and check not in ['Söndag', 'Søndag']:
        is_date_holiday = True

    apireturn = {
        'success': True,
        'data': {
        'country': iso,
        'date': holidate,
        'isHoliday': is_date_holiday,
        }
    }

    return json.dumps(apireturn, indent=4)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

    is_holiday()

