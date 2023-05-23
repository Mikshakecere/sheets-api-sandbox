import os
import math

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#spreadsheet used
#https://docs.google.com/spreadsheets/d/1Uos-0UdmOgryvWNFL3EdTqX5lpoLcumQw3tGuff99Rc/edit?usp=drivesdk
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = "1Uos-0UdmOgryvWNFL3EdTqX5lpoLcumQw3tGuff99Rc"

def main():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()
        #updates google sheets columns
        deviation_list = []
        deviation_mean = 21.73

        for row in range(2, 23):

            num1 = float(sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!L{row}").execute().get("values")[0][0])
            num2 = str(sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!L{row}").execute().get("values")[0][0])
            """
            print(f"Processing deviation using {mean} minus {num1}")

            calculation_result = math.fabs(round((num1 - mean),2))

            sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!L{row}",
                                   valueInputOption="USER_ENTERED", body={"values": [[f"{calculation_result}"]]}).execute()

            sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!K{row}",
                                   valueInputOption="USER_ENTERED", body={"values": [["Done"]]}).execute()
            """
            deviation_list.append(num1)
        sd = standard_dev(len(deviation_list), deviation_mean, deviation_list)
        print(round(sd,2))

    except HttpError as error:
        print(error)

def standard_dev(size, mean, observed_values):
    deviation = 0
    for value in observed_values:
        deviation += math.pow((value-mean),2)
    deviation /= size
    return math.sqrt(deviation)

def get_sec_from_ms(time_str):
    m, s = time_str.split(':')
    return float(m) * 60 + float(s)

if __name__ == "__main__":
    main()
