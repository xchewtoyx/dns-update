import socket

from cement.core import controller, foundation, handler
import pycurl

IP_DETECT_URL = 'http://rgh-go-sandpit.appspot.com/myip/'
IP_UPDATE_URL = (
  'http://svc.joker.com/nic/update?username=%s&password=%s&hostname=%s')

class DNSUpdateController(controller.CementBaseController):
  class Meta:
    label = 'base'
    description = 'DNS Updater'
    config_defaults = {}

  def _receive_addr(self, data):
    self._my_address = data

  def detect_ip(self):
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, IP_DETECT_URL)
    curl.setopt(pycurl.IPRESOLVE, pycurl.IPRESOLVE_V4)
    curl.setopt(pycurl.WRITEFUNCTION, self._receive_addr)
    curl.perform()
    self.app.log.debug('Detected IP address: %s' % self._my_address)
    return self._my_address

  def update_ip(self, hostname):
    ip_setter = urllib2.urlopen(
      IP_UPDATE_URL % (self.app.config.get('base', 'username'),
                       self.app.config.get('base', 'password'), hostname),)
    response = ip_setter.read()
    self.app.log.debug('Update result: %r' % response)
    ip_setter.close()

  @controller.expose(hide=True, aliases=['run'])
  def default(self):
    'Detect local ip address and update DNS if required'
    host_config = self.app.config.get('base', 'hostname')
    hosts = host_config.split(',')
    for hostname in hosts:
      registered_ip = socket.gethostbyname(hostname)
      if registered_ip != self.detect_ip():
        self.update_ip(hostname)

def run():
  dnsupdater = foundation.CementApp(
    'dnsupdater', base_controller=DNSUpdateController)
  try:
    dnsupdater.setup()
    dnsupdater.run()
  finally:
    dnsupdater.close()
