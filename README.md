<img src="https://raw.githubusercontent.com/wraldata/venus/master/leg_tracker/static/admin/img/venus_logo.png" width="75" align="left">

# Venus

Venus is WRAL's system for capturing and digesting bills, sponsors and votes of the N.C. General Assembly. Powered by Django and data from the [Legiscan API](Legiscan API).

Created by [Tyler Dukes](https://github.com/mtdukes), WRAL.

## Setting up

Clone repo and install requirements with ```pip```.

```bash
git clone https://github.com/wraldata/venus.git

pip install -r requirements.txt
```

Update database with ```git pull```.

## Current scripts

A rundown of the scripts that manage data in Venus. Most of these can run in the crontab with ```sudo nano /etc/crontab```. Need to move these into Django utils. 

Workflow:

```loadLawmakers.py > voteGen.py```

```get_new_bills.py > loadBills.py > loadVotes.py > lawmakerStats.py```

### getChanges.py

A python script to download a new Master File from the Legiscan API and check against our application's existing master file for any bill changes using the change hash. Currently checks for old file in ```data/master_file_old.json```.

Usage:

```bash
python get_new_bills.py

```

### loadLawmakers.py
Uses a centralized dataset of sitting North Carolina lawmakers maintained by WRAL to load new lawmakers into the database. Need to determine frequency to run this script in crontab.

Usage:

```bash
export DJANGO_SETTINGS_MODULE=leg_tracker.settings

python loadLawmakers.py

```

### loadBills.py
Uses data downloaded to ```data/bills``` to load new legislation into database.

Usage:

```bash
export DJANGO_SETTINGS_MODULE=leg_tracker.settings

python loadBills.py

```

### loadVotes.py
Uses data downloaded to ```data/votes``` to load new rollcall votes into database.

Usage:

```bash
export DJANGO_SETTINGS_MODULE=leg_tracker.settings

python loadVotes.py

```

### lawmakerStats.py
Uses data from rollcall votes to calculate part loyalty score and missed vote totals for each sitting North Carolina lawmaker.

Usage:

```bash
export DJANGO_SETTINGS_MODULE=leg_tracker.settings

python lawmakerStats.py

```

### voteGen.py
Utility function to generate four voting options for each lawmaker ('yea','nay','not voting','absent').

Usage:

```bash
export DJANGO_SETTINGS_MODULE=leg_tracker.settings

python voteGen.py

```

## LICENSE

Released under [MIT license](https://github.com/wraldata/venus/blob/master/LICENSE)

Venus flytrap icon by Daniel Gamage, [Noun Project](https://thenounproject.com/term/venus-flytrap/27589/)