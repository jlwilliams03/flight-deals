from datetime import datetime as dt, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

# Google Sheet Details
google_flight_deals_service_account_file = "credentials/Flight Deals-ca97ddb1f87d.json"
google_flight_deals_spreadsheet_id = "1S3DKXiOLybvg5Ec0WlomZF32j1GEXShCD25iUAXOi9g"
SHEET_DATA_RANGE = 'prices!A1:E100'

# Flight Preferences
ORIGIN_CITY = "DFW"
SEARCH_WINDOW_START_FROM_TODAY_DAYS = 7
STAY_LENGTH_DAYS = 6 * 30
UPDATE_TRIGGER_PRICE = True

prices = DataManager(google_flight_deals_service_account_file, google_flight_deals_spreadsheet_id)
flight_search = FlightSearch()
notify = NotificationManager()

# Calculate some handy dates
today = dt.today()
tomorrow = dt.today() + timedelta(days=SEARCH_WINDOW_START_FROM_TODAY_DAYS)
six_months_from_today = dt.today() + timedelta(days=STAY_LENGTH_DAYS)

# Read in the contents of the spreadsheet
sheet_data = prices.get_sheet_data(SHEET_DATA_RANGE)

# Iterate over all rows of the spreadsheet
for row in range(1, len(sheet_data)):
    city = sheet_data[row][0]
    code = sheet_data[row][1]
    trigger_price = int(sheet_data[row][2])

    # If there is no IATA code in the spreadsheet look it up
    # and update the sheet with the code
    if code == '':
        print(f"looking up code for {city}...")
        code = flight_search.get_location_code(city)
        data_range = f"prices!A{row + 1}"
        put_data = [[city, code, trigger_price]]
        prices.put_sheet_data(data_range, put_data)

    # flight_data contains the query details for a flight
    # Will be returned as None if no flight was found that matches the query
    flight_data = flight_search.search_flight(ORIGIN_CITY, code, tomorrow, six_months_from_today)
    if flight_data is not None:
        print(f"{flight_data.destination_city}:  ${flight_data.price}")

        # If the flight price found is less than the trigger price
        # then send SMS with the info
        if flight_data.price < trigger_price:
            print("---------------------------")
            notify.send_notification(
                flight_data.price,
                flight_data.origin_city,
                flight_data.origin_airport,
                flight_data.destination_city,
                flight_data.destination_airport,
                flight_data.leave_date,
                flight_data.return_date
            )
            print('---------------------------')

            # Update sheet with most recent price from query
            data_range = f"prices!D{row + 1}:E{row+1}"
            prices.put_sheet_data(data_range, [[flight_data.price,today.strftime('%m/%d/%Y')]])
            # Update the new low trigger price if the flag is set
            if UPDATE_TRIGGER_PRICE:
                if flight_data.price < int(trigger_price):
                    data_range = f"prices!C{row + 1}"
                    prices.put_sheet_data(data_range, [[flight_data.price]])
