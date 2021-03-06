import socket
import urllib2

from cement.core import controller, foundation, handler

IP_DETECT_URL = 'http://%s/myip/'
IP_DETECT_HOST = 'rgh-go-sandpit.appspot.com'

IP_UPDATE_URL = (
  'http://svc.joker.com/nic/update?username=%s&password=%s&hostname=%s')

class DNSUpdateController(controller.CementBaseController):
  class Meta:
    label = 'base'
    description = 'DNS Updater'
    config_defaults = {}

  def detect_ip(self):
    address = socket.gethostbyname(IP_DETECT_HOST)
    request = urllib2.Request(IP_DETECT_URL % (address, ),
                              headers={'Host': IP_DETECT_HOST})
    address = urllib2.urlopen(request).read().strip()
    self.app.log.debug('Detected IP address: %s' % (address,))
    return address

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
    self.app.log.debug('Detected hosts: %r' % hosts)
    for hostname in hosts:
      self.app.log.debug('Detecting IP info for host %r' % hostname) 
      try:
        registered_ip = socket.gethostbyname(hostname)
      except socket.error:
        registered_ip = None
      current_ip = self.detect_ip()
      self.app.log.debug('IP info for host %r (%r->%r)' % (
          hostname, registered_ip, current_ip))
      if registered_ip != current_ip:
        self.app.log.info('Processing IP change for host %r' % hostname)
        self.update_ip(hostname)

def run():
  dnsupdater = foundation.CementApp(
    'dnsupdater', base_controller=DNSUpdateController)
  try:
    dnsupdater.setup()
    dnsupdater.run()
  except Exception as err:
    print repr(err)
    raise
  finally:
    dnsupdater.close()
