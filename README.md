# Rabenyx

An ally for the fight against the chaos of Corona organisation at synyx. It is
intended to use the [Polls app for Nextcloud][1] and uses [its rudimentary
API][2].

If you seek information for the web application see
[its documentation](documentation/webapp.md) for details.

## How to configure

### INI file
Create a file `~/.config/rabenyx.ini` and use the following syntax:

````ini
[DEFAULT]
username=
password=
url=https://nextcloud.example.com
````

### Environment variables
If you cannot or do not want to use an ini file, you can use environment 
variables instead:

````bash
NEXTCLOUD_USERNAME=
NEXTCLOUD_PASSWORD=
NEXTCLOUD_URL=https://nextcloud.example.com
````

You need to add a new app password to use this feature, see [the security
section of your Nextcloud account][3] to add one.

## How to use

Use `python3 rabenyx.py --help` to see all of its features.

## How to develop

Run initially

````bash
pip install -e . -r requirements.txt
````

to setup your environment for testing. Run

````bash
pytest
````

to run the tests.

### API, DB or web?

There are three ways to talk to the Poll app:
* via [its API](./pollapi)
* via [the web way](./pollweb)
* via [the database](./polldb)

If you develop for Rabenyx, try the API way first. It is partly 
[documented][5]. Sometimes it helps to look at [its routes][6] too. If the API
does not satisfy your needs try the web way. If this doesn't help at all you
can consider using the database at last.

[Document the used API bits](documentation/pollapi.yaml) in [OAS3][4].

[1]: https://github.com/nextcloud/polls/
[2]: https://github.com/nextcloud/polls/blob/master/docs/API_v1.0.md
[3]: https://nextcloud.example.com/settings/user/security
[4]: https://swagger.io/docs/specification/about/
[5]: https://github.com/nextcloud/polls/blob/master/docs/API_v1.0.md
[6]: https://github.com/nextcloud/polls/blob/master/appinfo/routes.php
