import os
import time
import kerberos
from selenium import webdriver


class KerberosTicket(object):
    def __init__(self, service):
        __, krb_context = kerberos.authGSSClientInit(service)
        kerberos.authGSSClientStep(krb_context, "")
        self._krb_context = krb_context
        self.auth_header = ("Negotiate " +
                            kerberos.authGSSClientResponse(krb_context))

    def verify_reponse(self, auth_header):
        for field in auth_header.split(","):
            kind, __, details = field.strip().partition(" ")
            if kind.lower() == "negotiate":
                auth_details = details.strip()
                break
            else:
                raise ValueError("Negotiate not found in %s" % auth_header)
        krb_context = self._krb_context
        if krb_context is None:
            raise RuntimeError("Ticket already used for verification")
        self._krb_context = None
        kerberos.authGSSClientStep(krb_context, auth_details)
        kerberos.authGSSClientClean(krb_context)


def get_kerberos_auth_headers():
    krb = KerberosTicket("HTTP@errata.devel.redhat.com")
    headers = {"Authorization": krb.auth_header}
    return headers

def sele_test():
    headers = get_kerberos_auth_headers()
    driver = webdriver.Firefox()
    driver.get("https://errata.devel.redhat.com/package/show/ovirt-node")
    time.sleep(10)

    list1 = driver.find_element_by_css_selector("table").find_elements_by_css_selector("tr")
    print list1

# sele_test()