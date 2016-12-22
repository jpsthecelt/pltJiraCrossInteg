import requests
import pprint
import argparse
import requests_oauthlib
import json

#
# This is a sample program intended to demonstratge pulling information from both JIRA and from Plutora
# eventually pushing JIRA information into Plutora.
# it requires previously 'set up' access to instances of both.
# Some of the code was originally adapted from 'snippets' produced by the
# Chrome program POSTMAN.
#

# Set up JSON prettyPrinting
pp = pprint.PrettyPrinter(indent=4)

# parse commandline and get appropriate passwords
parser = argparse.ArgumentParser(description='Get user/password information for both JIRA & Plutora.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()

# ClientId & Secret from manual setup of Plutora Oauth authorization.
pClientId = r'E7EJZTL67OAURNKMKOKPD5W7ZE'
pClientSecret = r'SMQVSO7HHA2EBMVT6ICQF4RNDQ'

# Setup for Get authorization-token
authTokenUrl = "https://usoauth.plutora.com/oauth/token"
payload = "client_id=E7EJZTL67OAURNKMKOKPD5W7ZE&client_secret=SMQVSO7HHA2EBMVT6ICQF4RNDQ&grant_type=password&username=john.singer%40plutora.com&password=jps53.jps53&="
headers = {
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    'postman-token': "bc355474-15d1-1f56-6e35-371b930eac6f"
    }

# Connect to get Plutora access token for subsequent queries
authResponse = requests.post(authTokenUrl, data=payload, headers=headers)
if authResponse.status_code != 200:
    print(authResponse.status_code)
    print('pltJiraCrossInteg.py: Sorry! - [failed on getAuthToken]: ', authResponse.text)
    exit('Sorry, unrecoverable error; gotta go...')
else:
    print('\npltJiraCrossInteg.py - authTokenGet: ')
    pp.pprint(authResponse.json())
accessToken = authResponse.json()["access_token"]

# Setup to query both JIRA & Maersk Plutora instances
plutoraMaerskUrl = r'http://maersk.plutora.com/changes/12/comments'
plutoraMaerskTestUrl = r'https://usapi.plutora.com/me'
payload = "client_id=E7EJZTL67OAURNKMKOKPD5W7ZE&client_secret=SMQVSO7HHA2EBMVT6ICQF4RNDQ&grant_type=password&username=john.singer%40plutora.com&password=jps53.jps53&="
jiraURL = r'http://localhost:8080/rest/api/2/search?jql=project="DemoRevamp"&expand'
headers = {
    'content-type': "application/x-www-form-urlencoded",
    'authorization': "bearer "+accessToken,
    'cache-control': "no-cache",
    'postman-token': "bc355474-15d1-1f56-6e35-371b930eac6f"
}

# Make the call to connect to local JIRA instance
r = requests.get(jiraURL, auth=('john.singer','jps.jps' ))
if r.status_code != 200:
    print r.status_code
    print('\npltJiraCrossInteg.py: Sorry! - [failed on JIRA get]')
    exit('Sorry, unrecoverable error; gotta go...')
else:
    print('\npltJiraCrossInteg.py - JIRA get:')
    pp.pprint(r.json())

# Get Plutora information for a particular release
plutoraGetReleaseUrl = 'https://usapi.plutora.com/releases/9d18a2dc-b694-4b20-971f-4944420f4038'
r = requests.get(plutoraGetReleaseUrl, data=payload, headers=headers)
if r.status_code != 200:
    print r.status_code
    print('\npltJiraCrossInteg.py: too bad sucka! - [failed on JIRA get]')
    exit('Sorry, unrecoverable error; gotta go...')
else:
    print('\npltJiraCrossInteg.py - Plutora get of release information:')
    pp.pprint(r.json())

print('\n\nwere all done here, boys')
#for i in r.json()["issues"]:
#    print("field is", i["fields"]["description"])
#    r = requests.post(plutoraMaerskUrl, data=i["fields"]["description"], headers=headers)
#    if r.status_code != 200:
#       print "Error inserting record into Plutora:", i, r.status_code
#       exit('Cant insert into Plutora')
#    else:
#       print('pltJiraCrossInteg.py: too bad sucka! - [failed on POST]')
