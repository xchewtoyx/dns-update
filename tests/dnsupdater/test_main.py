from cement.core import foundation, handler
from cement.utils import test

from dnsupdater.main import DNSUpdateController

class TestApp(foundation.CementApp):
    class Meta:
        label = 'dnsupdater'
        argv = []
        base_controller = DNSUpdateController
        config_files = []

class DnsUpdateTest(test.CementTestCase):
    app_class = TestApp

    def test_update_controller(self):
        self.app.setup()
        dnscontroller = handler.get('controller', 'base')
        self.assertTrue(hasattr(dnscontroller, 'default'))

    def test_detect_ip(self):
        self.app.setup()
        dnscontroller = handler.get('controller', 'base')()
        dnscontroller._setup(self.app)

        myip = dnscontroller.detect_ip()

        self.assertRegexpMatches(myip, r'\d+(?:\.\d+){3}')
