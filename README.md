<h1>Gandi.net live DNS API Client Python Library</h1>

[![PyPI version](https://badge.fury.io/py/gandi-api-livedns.svg)](https://badge.fury.io/py/gandi-api-livedns)

<p>Easily search for trips!</p>

<h3>Installation</h3>
<p>Works on 3.x python.</p>

```
pip install gandi-api-livedns
```

<h3>Usage</h3>

```python
from gandi_api_livedns import GandiApiLiveDNS

# initialize API
gandiApiLiveDNS = GandiApiLiveDNS(api_key="__your_api_key_here__")

# set rrname and domain
gandiApiLiveDNS.rrname = 'dummy'
gandiApiLiveDNS.domain = 'mydomain.com'

# get real ip
RealIP = gandiApiLiveDNS.getRealIP()
pprint.pprint(RealIP)

# get registered dns record
DNSRecord = gandiApiLiveDNS.getDNSRecord()
pprint.pprint(DNSRecord)

# update dns record with detected ip
updateDNSRecord = gandiApiLiveDNS.updateDNSRecord()
pprint.pprint(updateDNSRecord)
```
