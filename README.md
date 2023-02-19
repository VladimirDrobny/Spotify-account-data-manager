# Spotify account data manager

## FEATURES

- Transferring all data from one account to another:

> - saved tracks
> - saved albums
> - saved playlists
> - created playlists
> - followed artists
> - followed users (Spotify API doesn't support getting followed users, so we have to use a hardcoded list of users)

- Wiping all data from an account

## USAGE

### Spotify API setup

- Set up a spotify developer account ([official guide here](https://developer.spotify.com/documentation/web-api/quick-start/))
> 1. Register at the [Developer Dashboard](https://developer.spotify.com/dashboard/)
> 2. Create a new app
> 3. Add a redirect URI under the 'EDIT SETTINGS' option (I use 'http://localhost:8888/SpotifySync/')
> 4. ADD ALL USERS WHOSE DATA YOU WANT TO ACCESS under the 'USERS AND ACCESS' option

### Settings setup

- Put your settings in the 'settings.ini' file
- Because Spotify API doesn't support getting followed users, also put a list of user ids, who you want to automatically follow whensyncing accounts

Sample settings:

```
[SPOTIFY\_API]
client\_id = h8g5h23487f695234y768dfg784327gf
client\_secret = 8932hg89h3248fuh792h8f3n4dnxn98a
redirect\_uri = http://localhost:8888/SpotifySync/

[USER\_SETTINGS]
forced\_follow\_user\_list = ["89fh43279fg9873h2fg7d8g81"]
```

### Commands

**All of the following commands should open a login dialogue in your browser. The console prints which account it want you to log into (SAMPLE or TARGET), read it.

YOU MAY BE ALREADY LOGGED IN TO THE ACCOUNT YOU LAST ACCESSED, AND MAY NEED TO LOG OUT (by clicking on 'Not you?'). After logging into the correct account, you will still have to click AGREE.**

**SYNC command**

```console
$ python3 main.py -s
```

- Gets all data from SAMPLE account, and transfers it to TARGET account. SAMPLE account doesn't get affected. Data from TARGET account doesn't get deleted, only more data is added on top.

**WIPE command**

```console
$ python3 main.py -w
```

- Wipes ALL data from an account.
