from google.oauth2 import service_account
from googleapiclient.discovery import build


class DataManager():
    def __init__(self, service_account_file, spreadsheet_id):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.SERVICE_ACCOUNT_FILE = service_account_file
        self.creds = service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
        self.service = service = build('sheets', 'v4', credentials=self.creds)
        self.sheet = service.spreadsheets()
        self.spreadsheet_id = spreadsheet_id

    def get_sheet_data(self, data_range_name):
        result = self.sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                         range=data_range_name).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            return values

    def put_sheet_data(self, data_range_name, data, ):
        result = self.sheet.values().update(spreadsheetId=self.spreadsheet_id,
                                            range=data_range_name, valueInputOption='USER_ENTERED',
                                            body={"values": data}).execute()
