import socket
import urllib2

from cement.core import controller, foundation, handler

IP_DETECT_URL = 'http://rgh-go-sandpit.appspot.com/myip/'
IP_UPDATE_URL = (
  'http://svc.joker.com/nic/update?username=%s&password=%s&hostname=%s')

class DNSUpdateController(controller.CementBaseController):
  class Meta:
    label = 'base'
    description = 'DNS Updater'
    config_defaults = {}

  def detect_ip(self):
    ip_lookup = urllib2.urlopen(IP_DETECT_URL)
    my_address = ip_lookup.read()
    self.app.log.debug('Detected IP address: %s' % my_address)
    ip_lookup.close()
    return my_address

  def update_ip(self):
    ip_setter = urllib2.urlopen(
      IP_UPDATE_URL % (self.app.config.get('base', 'username'),
                       self.app.config.get('base', 'password'),
                       self.app.config.get('base', 'hostname'),))
    response = ip_setter.read()
    self.app.log.debug('Update result: %r' % response)
    ip_setter.close()

  @controller.expose(hide=True, aliases=['run'])
  def default(self):
    'Detect local ip address and update DNS if required'
    registered_ip = socket.gethostbyname(
      self.app.config.get('base', 'hostname'))
    if registered_ip != self.detect_ip():
      self.update_ip()

def run():
  dnsupdater = foundation.CementApp(
    'dnsupdater', base_controller=DNSUpdateController)
  try:
    dnsupdater.setup()
    dnsupdater.run()
  finally:
    dnsupdater.close()
