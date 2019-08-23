#!/usr/bin/env python2.7
"""
Package to support loading and lookup of cpu micro architectural specifications

This package provides logic to
  1. Download micro architecture specifications for intel processors
  2. Logic to build a specification database for known micro architectures

Author: Manikandan Dhamodharan, Morgan Stanley
"""

import os
import csv

UARCH_SPEC_PKG_NAME = 'xpedite_uarch_spec'

class UarchSpec(object):
  """Stores location of pmu event specs for a cpu micro architecture"""

  def __init__(self, cpuId, name):
    self.cpuId = cpuId
    self.name = name.strip()
    self.coreEventsDbFile = None
    self.uncoreEventsDbFile = None

  def topdownRatios(self):
    """Imports topdown hierarchy for a cpu micro architecture"""
    ratiosModule = '{}.{}'.format(UARCH_SPEC_PKG_NAME, self.name)
    import importlib
    try:
      return importlib.import_module(ratiosModule)
    except ImportError as ex:
      raise Exception('xpedite currently doesn\'t support topdown methodology for {} uarch - {}'.format(self.name, ex))

  def __repr__(self):
    return 'uarch spec cpu gen - {} | id {}'.format(self.name, self.cpuId)

class UarchSpecDb(object):
  """A database of micro architecture specifications for all known cpu models"""

  mapHdrFamily = 'Family-model'
  mapHdrVersion = 'Version'
  mapHdrFilename = 'Filename'
  mapHdrEventType = 'EventType'

  def __init__(self, manifestPath):
    from collections import OrderedDict
    self.uarchSpecMap = OrderedDict()
    uarchSpecDirPath = os.path.dirname(os.path.abspath(manifestPath))
    with open(manifestPath) as fileHandle:
      reader = csv.DictReader(fileHandle)
      for row in reader:
        cpuId = row[UarchSpecDb.mapHdrFamily].strip()
        eventsDbFile = row[UarchSpecDb.mapHdrFilename].strip()
        if cpuId not in self.uarchSpecMap:
          name = os.path.basename(os.path.dirname(eventsDbFile))
          self.uarchSpecMap.update({cpuId : UarchSpec(cpuId, name)})
        uarchSpec = self.uarchSpecMap[cpuId]

        eventType = row[UarchSpecDb.mapHdrEventType].strip()
        eventsDbFile = uarchSpecDirPath + eventsDbFile
        if eventType == 'core':
          uarchSpec.coreEventsDbFile = eventsDbFile
        elif eventType == 'core':
          uarchSpec.uncoreEventsDbFile = eventsDbFile

  def __len__(self):
    return len(self.uarchSpecMap)

  def __getitem__(self, cpuId):
    return self.uarchSpecMap[cpuId] if cpuId in self.uarchSpecMap else None

  def items(self):
    """Returns an iterable for events in this database"""
    return self.uarchSpecMap.items()

  def __repr__(self):
    repStr = 'UarchSpecDb ({}) entries'.format(len(self.uarchSpecMap))
    for cpuId, uarchSpec in self.uarchSpecMap.items():
      repStr += '\n\t{}\t{}'.format(cpuId, uarchSpec)
    return repStr

  def spec(self, cpuId):
    """Returns micro architecture specs for a given cpu model"""
    return self[cpuId]
