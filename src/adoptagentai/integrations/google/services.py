import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleUtilsTool:
    """Base class for Google service tools."""
    def __init__(self, tool_account_name: str = None):
        self.tool_account_name = tool_account_name
        self.tool_credentials = get_api_credentials("google", self.tool_account_name)


class GoogleSheetsTool(GoogleUtilsTool):
    """Tool for Google Sheets integration."""
    def __init__(self, tool_account_name: str = None):
        super().__init__(tool_account_name)
        self.sheets_service = self._build_sheets_service()
    
    def _build_sheets_service(self):
        """Build and return the Google Sheets service."""
        return build('sheets', 'v4', credentials=self.tool_credentials)
    
    def read_spreadsheet(self, spreadsheet_id, range_name):
        """Read data from a Google Sheets spreadsheet."""
        try:
            result = self.sheets_service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, range=range_name).execute()
            values = result.get('values', [])
            
            if not values:
                print("No data found.")
                return []
                
            return values
        except HttpError as err:
            print(f"An error occurred: {err}")
            return []
    
    def update_spreadsheet(self, spreadsheet_id, range_name, values):
        """Update data in a Google Sheets spreadsheet."""
        try:
            body = {'values': values}
            result = self.sheets_service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id, range=range_name,
                valueInputOption='USER_ENTERED', body=body).execute()
            return result
        except HttpError as err:
            print(f"An error occurred: {err}")
            return None


class GoogleDriveTool:
    """Tool for Google Drive integration."""
    def __init__(self):
        pass
    

class GoogleGmailTool:
    """Tool for Google Gmail integration."""
    def __init__(self):
        pass


class GoogleCalendarTool:
    """Tool for Google Calendar integration."""
    def __init__(self):
        pass
