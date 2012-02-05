import urllib
from xml.dom import minidom

GEO_IP_LOOKUP_URL = 'http://api.hostip.info/?ip=%s'
GML_NS = 'http://www.opengis.net/gml'

def geo_ip_lookup(ip_address):
  """
  Look up the geo information based on the IP address passed in
  """
  dom = minidom.parse(urllib.urlopen(GEO_IP_LOOKUP_URL % ip_address))
  elem = dom.getElementsByTagName('Hostip')[0]
  location = elem.getElementsByTagNameNS(GML_NS, 'name')[0].firstChild.data.partition(',')

  try:
    latlong = elem.getElementsByTagNameNS(GML_NS, 'coordinates')[0].firstChild.data.partition(',')
  except:
    # lat/long isnt always returned
    latlong = None

  return {
    'country_code': elem.getElementsByTagName('countryAbbrev')[0].firstChild.data,
    'country_name': elem.getElementsByTagName('countryName')[0].firstChild.data,
    'locality': location[0].strip(),
    'region': location[2].strip(),
    'longitude': latlong[0].strip() if latlong else '',
    'latitude': latlong[2].strip() if latlong else ''
  }

print geo_ip_lookup('65.34.176.69')
