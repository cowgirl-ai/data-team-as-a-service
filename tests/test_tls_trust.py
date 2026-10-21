"""Offline checks for the CA bundle used by Requests and HTTPX."""
import hashlib
import ssl
import unittest

import certifi
import httpx
import requests

# Trust paths removed by certifi 2026.10.19 after the eMudhra incident.
REMOVED_ROOTS = {
    "86a1ecba089c4a8d3bbe2734c612ba341d813e043cf9e8a862cd5c57a36bbe6b",
    "d7a7a0fb5d7e2731d771e9484ebcdef71d5f0c3e0a2948782bc83ee0ea699ef4",
}


class TLSTrustTests(unittest.TestCase):
    def assert_safe_context(self, context):
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(context.check_hostname)
        fingerprints = {
            hashlib.sha256(der).hexdigest()
            for der in context.get_ca_certs(binary_form=True)
        }
        self.assertGreater(len(fingerprints), 100)
        self.assertFalse(REMOVED_ROOTS & fingerprints)

    def test_requests_bundle(self):
        self.assertEqual(requests.certs.where(), certifi.where())
        self.assert_safe_context(ssl.create_default_context(cafile=requests.certs.where()))

    def test_httpx_default_bundle(self):
        # Inspect the actual client's context without making a network request.
        with httpx.Client(trust_env=False) as client:
            self.assert_safe_context(client._transport._pool._ssl_context)


if __name__ == "__main__":
    unittest.main()
