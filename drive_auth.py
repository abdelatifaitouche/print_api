from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os

SCOPES = ["https://www.googleapis.com/auth/drive"]


def authenticate_printshop_account():
    """
    Run this ONCE to authenticate the print shop Google account.
    This will open a browser window for the print shop owner to log in.
    """

    if not os.path.exists("printflow_dev.json"):
        print("ERROR: credentials.json not found!")
        print("Please download it from Google Cloud Console")
        return

    print("🔐 Starting authentication process...")
    print(
        "A browser window will open. Please log in with the PRINT SHOP Google account."
    )
    print("(The account that owns the Drive folder where files will be stored)")

    try:
        flow = InstalledAppFlow.from_client_secrets_file("printflow_dev.json", SCOPES)

        # This will open a browser for authentication
        creds = flow.run_local_server(port=8080, timeout=120)

        # Save the credentials for future use
        with open("printshop_token.pickle", "wb") as token:
            pickle.dump(creds, token)

        print("✅ Authentication successful!")
        print("✅ Token saved to 'printshop_token.pickle'")
        print("✅ You can now use the Google Drive service in your app")

    except Exception as e:
        print(f"❌ Authentication failed: {e}")


if __name__ == "__main__":
    authenticate_printshop_account()
