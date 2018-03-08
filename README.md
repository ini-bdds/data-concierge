# Concierge Service

Your bags will be handled with care.

The Concierge Services implement REST APIs secured with Globus Auth that handle common patterns around data management, using standards wherever possible.

* `search2bag` accepts a set of URIs to datasets and returns a digital identifier (a Minid) that references a BDBag stored in a configurable location such as S3. 
This can be used to track groupings of datasets by users in a portal, for example, with the Minid acting as the primary key. 

* `stagebag` is intended be incorporated into workflows or to simplify data transfers and staging by users. 
As one parameter, it accepts one or more Minids referencing BDBags, on the assumption that the remote references for the data in the BDBags are Globus URIs. 
The other parameters are a destination Globus endpoint and path. 
The Service iterates through the URIs referenced in the BDBags and submits a Globus Transfer request to the destination. 
The identifier of the Transfer request is returned for the portal or user to monitor its progress. 

* `checkbag` (in development) will utilize a remote checksum storage API to compare the checksums of files on an endpoint with those in the BDBag. 
This will enable the creation of integrity checking services, and also allow users to know which files they may have modified during their work.

## Environment Setup

* `git clone https://github.com/globusonline/search2bag`
* `cd search2bag`
* `virtualenv venv`
* `source venv/bin/activate`
* `pip install -r requirements.txt`

BDBags requires the following:

* `pip install --process-dependency-links git+https://github.com/ini-bdds/bdbag`

## Running the App

### Local

* `python manage.py migrate`
* `python manage.py runserver`

This will start the flask server running on `http://localhost:8000`
