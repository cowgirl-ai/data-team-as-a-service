# October 2026 TLS trust update

This repository pinned a certifi CA bundle from 2024 that trusts the emSign ECC
Root CA - G3 and AAA Certificate Services paths implicated in the eMudhra
intermediate-key compromise. certifi 2026.10.19 removes these paths. Requests,
HTTPX, and the OpenAI Python SDK use certifi by default. A forged certificate can
impersonate an unrelated API hostname if an attacker can intercept its traffic;
this finding does not establish interception, credential theft, or exploitation.

Rebuild environments from the updated requirements and restart/redeploy after
review. Existing processes, installed packages, published Cowgirl package releases,
and deployed services are not changed by this PR. TLS verification stays enabled.
Custom CA overrides and the operating system trust store need separate review.

Run `python -m unittest discover -s tests -p 'test_tls*.py'` for offline trust checks.
The checks inspect the actual HTTPX context and Requests CA file; they make no API
requests. Before installing dependencies, use Python 3.10 or newer and bootstrap
pip 26.2.2 or newer using the hash-pinned wheel in the PSF advisory below. App
Engine's managed build installer and base-image trust remain provider
responsibilities; an application certifi pin
does not update either one.

Sources:
- [Mozilla incident report](https://blog.mozilla.org/security/2026/10/20/protecting-firefox-users-following-the-compromise-of-emudhra-intermediate-certificates/)
- [certifi 2026.10.19](https://github.com/certifi/python-certifi/releases/tag/2026.10.19)
- [Python installer advisory](https://discuss.python.org/t/information-for-python-users-regarding-emudhra-emsign-ca-certificate-security-incident/109576)

Package installation also requires `certifi>=2026.10.19` in `setup.py`, so installing
this project from a wheel or source distribution retains the patched CA-bundle
floor even without installing `requirements.txt` separately. The requirements file
continues to define the full application environment.
