"""
Xpedite configuration

This module provides the default values for Xpedite config parameters
The default values can be overridden using a Xpedite plugin

Author: Manikandan Dhamodharan, Morgan Stanley
"""

import os

class Config(object):
  """Xpedite config options"""

  def __init__(self, config):
    self.logDir = config.get('logDir', os.path.join('/var/tmp', os.getenv('USER'), 'xpedite'))
    self.uarchSpecPath = config.get('uarchSpecPath', '/var/tmp/xpedite')
    self.uarchSpecRepoUrl = config.get('uarchSpecRepoUrl', 'https://download.01.org/perfmon/')
    self.manifestFileName = config.get('manifestFileName', 'mapfile.csv')
    self.topdownRatiosRepoUrl = config.get(
      'topdownRatiosRepoUrl', 'https://raw.githubusercontent.com/andikleen/pmu-tools/master/'
    )

  def __repr__(self):
    cfgStr = 'Xpedite Configurations'
    for k, val in vars(self).items():
      cfgStr += '\n\t{} - {}'.format(k, val)
    return cfgStr
