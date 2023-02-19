import sys, getopt
from spotify_api_client import SpotifyApiClient
import configparser
import json

def wipe_account():
    print("*WIPE ACCOUNT*")
    print("Logging in to TO BE WIPED account...")
    wipe_client = SpotifyApiClient(client_id, client_secret, redirect_uri, forced_follow_user_list)
    if (wipe_client.get_logged_in_status()):
        print(f"Logged in as {wipe_client.get_username()}.")
    else:
        print("LOGIN FAILED!")
        return 1

    confirm = input(f"Are you sure you want to wipe the account {wipe_client.get_username()}? (y/n): ")
    if (confirm == "y"):
        print("Wiping account...")
        wipe_client.wipe_account()
        print("Done.")

def sync_accounts():
    print("*SYNC ACCOUNTS*")
    print("Logging in to SAMPLE account...")
    sample_client = SpotifyApiClient(client_id, client_secret, redirect_uri, forced_follow_user_list)
    if (sample_client.get_logged_in_status()):
        print(f"Logged in as {sample_client.get_username()}.")
    else:
        print("LOGIN FAILED!")
        return 1

    print("Logging in to TARGET account...")
    target_client = SpotifyApiClient(client_id, client_secret, redirect_uri, forced_follow_user_list)
    if (target_client.get_logged_in_status()):
        print(f"Logged in as {target_client.get_username()}.")
    else:
        print("LOGIN FAILED!")
        return 1

    print()

    print("Getting data from sample account...")
    sample_account_data = sample_client.get_account_data()

    print("Adding sample account data to target account...")
    target_client.add_account_data(sample_account_data)

    print("Done.")

def print_help():
    print("Use -w flag to wipe account. Use -s flag to sync accounts.")

def init_settings():
    global client_id, client_secret, redirect_uri, forced_follow_user_list
    config = configparser.ConfigParser()
    config.read("settings.ini")

    client_id = config["SPOTIFY_API"]["client_id"]
    client_secret = config["SPOTIFY_API"]["client_secret"]
    redirect_uri = config["SPOTIFY_API"]["redirect_uri"]

    forced_follow_user_list = json.loads(config["USER_SETTINGS"]["forced_follow_user_list"])
    
def init():
    init_settings()

    opts, args = getopt.getopt(sys.argv[1:], "hws")
    for opt, val in opts:
        if (opt == "-h"):
            print_help()
            return 0
        if (opt == "-w"):
            wipe_account()
            return 0
        if (opt == "-s"):
            sync_accounts()
            return 0

if __name__ == "__main__":
    init()
