
xml = """<HostipLookupResultSet xmlns:gml="http://www.opengis.net/gml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.0.1" xsi:noNamespaceSchemaLocation="http://www.hostip.info/api/hostip-1.0.1.xsd">
           <gml:description>This is the Hostip Lookup Service</gml:description>
           <gml:name>hostip</gml:name>
           <gml:boundedBy>
             <gml:Null>inapplicable</gml:Null>
           </gml:boundedBy>
           <gml:featureMember>
             <Hostip>
               <ip>12.215.42.19</ip>
               <gml:name>Aurora, TX</gml:name>
               <countryName>UNITED STATES</countryName>
               <countryAbbrev>US</countryAbbrev>
               <!-- Co-ordinates are available as lng,lat -->
               <ipLocation>
                 <gml:pointProperty>
                   <gml:Point srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">
                     <gml:coordinates>-97.5159,33.0582</gml:coordinates>
                   </gml:Point>
                 </gml:pointProperty>
               </ipLocation>
             </Hostip>
           </gml:featureMember>
        </HostipLookupResultSet>"""

# QUIZ - implement the get_coords(xml) function that takes in an xml string
# and returns a tuple of (lat, lon) if there are coordinates in the xml.
# Remember that you should use minidom to do this.
# Also, notice that the coordinates in the xml string are in the format:
# (lon,lat), so you will have to switch them around.

from xml.dom import minidom

def get_coords(xml):
    d = minidom.parseString(xml)
    n = None
    for node in d.getElementsByTagName("gml:coordinates"):
        n = node.toxml()
    wanted = ['.',',','-']
    new_node = ''
    for stuff in n:
        if stuff in wanted or stuff.isdigit():
            new_node = new_node + stuff
    node_list = new_node.split(',')

    return node_list[1], node_list[0]

def test_coords(xml):
    g = minidom.parseString(xml)
    e = g.getElementsByTagName("gml:coordinates")
    if e:
        lon, lat = e[0].childNodes[0].nodeValue.split(',')
        return lon, e[0].childNodes[0].nodeValue.split(',')

def return_list_test(blah):
    one, two = blah
    return two


print get_coords(xml)
print test_coords(xml)
print return_list_test(['coriander', 'vorkosigan'])


