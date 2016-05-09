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

## Current scripts

A rundown of the scripts that manage data in Venus. Most of these can run in the crontab with ```sudo nano /etc/crontab```. Need to move these into Django utils. 

Workflow:

```loadLawmakers.py > voteGen.py```

```get_new_bills.py > loadBills.py > loadVotes.py > lawmakerStats.py```

### get_new_bills.py

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

### To-do list

- [ ] Add watch field for rollcall votes
- [ ] Make sure bill title is always replaced when there's a change
- [ ] Prevent user from altering bill title
- [ ] Make sure description isn't overwritten when there's a change, allowing user to customize
- [ ] Differentiate between primary/co-sponsors by filtering for ```sponsor_type_id=1```
- [ ] Create party model for generating stats and other information
- [ ] Calculate party loyalty average for dems/gop
- [ ] Calculate missed vote score for dems/gop
- [ ] Add bill number to rollcall votes
- [ ] Integrate scripts into Django util functions ([example](https://github.com/datadesk/django-for-data-analysis-nicar-2016))
- [ ] Improve error handling and reporting
- [ ] Add check for sitting lawmakers to check inactive members
- [ ] Refactor.
- [ ] Refactor.
- [ ] REFACTOR.

### Feature requests

- [ ] Calculate "batting average" of sponsored bills passed
- [ ] Show lawmaker tenure

## LICENSE

Released under [MIT license](https://github.com/wraldata/venus/blob/master/LICENSE)

Venus flytrap icon by Daniel Gamage, [Noun Project](https://thenounproject.com/term/venus-flytrap/27589/)