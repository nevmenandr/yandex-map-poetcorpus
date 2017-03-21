#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 21.03.2017 01:44:45 MSK

import codecs
import urllib2
import urllib
import re

def retriever(place):
    url = u'https://ru.wikipedia.org/wiki/' + place
    page = urllib.urlopen(url.encode("UTF-8")).read()
    res = re.search(u'href="//(tools.+?)">', page)
    link = res.group(1)
    link = link.replace('&amp;', '&')
    link = 'https://' + link 
    p = urllib2.urlopen(link)
    page = p.read().decode('utf-8')
    p.close()
    resl = re.search(u'span class="latitude" title="Широта">(.+?)</span>', page)
    lat = resl.group(1)
    resl = re.search(u'span class="longitude" title="Долгота">(.+?)</span>', page)
    lon = resl.group(1)
    latlon = lon + ',' + lat
    print (latlon)
    string = u'"' + place + u'"\t' + latlon + '\n'
    return string

def main():
    f = codecs.open('locations.tsv', 'r', 'utf-8')
    fe = codecs.open('not-found.tsv', 'w', 'utf-8')
    fw = codecs.open('places_coordinates.tsv', 'w', 'utf-8')
    
    places_found = []
    
    for line in f:
        fields = line.split('\t')
        if len(fields[1]) > 0:
            loc = fields[1]
        else:
            loc = fields[0]
        if u'IN:' in loc:
            loc = re.sub(u'.*?IN:', u'', loc)
        if u'НЕ ЛОКАЦИЯ' in loc or u'DER' in loc or u'CHECK' in loc or u'UNKNOWN' in loc:
            continue
        loc = loc.strip()
        if loc == u'Петербург':
            loc = u'Санкт-Петербург'
        print loc
        if loc in places_found:
            continue
        places_found.append(loc)
        try:
            fw.write(retriever(loc))
        except:
            fe.write(loc + '\n')
    f.close()
    fw.close()
    fe.close()

    return 0


if __name__ == '__main__':
    main()

