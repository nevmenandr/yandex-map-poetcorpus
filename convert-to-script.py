#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 21.03.2017 05:20:18 MSK

import codecs
import urllib2


head = u'''
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Задать подкорпус с помощью карты.</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <script src="http://api-maps.yandex.ru/2.0-stable/?load=package.standard&amp;lang=ru-RU"></script>
</head>
<body>
<h1>Задать подкорпус с помощью карты.</h1>
<script>
ymaps.ready(init);
var map;

function init() {
	map = new ymaps.Map ("map", {
//		center: [55.76, 37.64], 
		center: [54.702462,37.612741], 

		zoom: 3
	});
	map.behaviors.enable("scrollZoom");
	map.controls
		.add('zoomControl', { left: 10, top: 100 })
		.add('mapTools', { left: 10, top: 10 })
		.add('typeSelector');

	var objects = ['''

foot = u'''];
	

	var collection = new ymaps.GeoObjectCollection();



	for (var i = 0; i < objects.length; i++) {
    	collection.add(new ymaps.Placemark(
    		objects[i].coords, 
    		{ balloonContent: "<a href='http://search2.ruscorpora.ru/search.xml?env=alpha&text=meta&mode=poetic&sort=gr_tagging&lang=ru&doc_te_header=&doc_t_cyclus=&doc_t_liber=&doc_te_author=&doc_sex=&doc_g_birthday=&doc_l_birthday=&doc_te_original=&doc_g_created=&doc_l_created=&doc_location=&doc_location_normalized="+objects[i].url+"&doc_g_verses=&doc_l_verses=&doc_genre_fi=&doc_language=&doc_meter=&doc_feet=&doc_clausula=&doc_strophe=&doc_gr_strophe=&doc_rhyme=&doc_formula=&doc_extra=&doc_g_crevision=&doc_l_crevision='><div style='padding:10px; width:400px;'><h3 style='margin-top:0px;'>"+objects[i].name+"</h3><p>"+objects[i].description+"</p></div></a>" },
    		{ iconImageHref: "http://nevmenandr.net/pages/label1.png", iconImageSize: [30, 32] } ));
	}

	map.geoObjects.add(collection);
}
</script>
<div id="map" style="width:1000px; height:600px;"></div> 
</body>
</html>'''

def script_former(dic_coord):
    f = codecs.open('poetry_map.html', 'w', 'utf-8')
    f.write(head)
    entries = []
    for place in sorted(dic_coord):
        entries.append(u"{coords: [" + dic_coord[place]['latlon'] + u"], name: '" + place + u"', description: 'Задать подкорпус', url:'" + dic_coord[place]['percent'] + u"'}")
    f.write(','.join(entries))
    f.write(foot)
    f.close()
        
    
def invert(coords):
    lat, lon = coords.split(',')
    coords = lon + ',' + lat
    return coords

def main():
    coordinates = ['hand-found', 'places_coordinates']
    dic_coord = {}
    for fl in coordinates:
        f = codecs.open(fl + '.tsv', 'r', 'utf-8')
        for line in f:
            if '\t' not in line:
                continue
            line = line.strip()
            place, coords = line.split('\t')
            place = place.replace('"', '')
            coords = invert(coords)
            dic_coord[place] = {'latlon': coords, 'percent': urllib2.quote(place.encode("cp1251"))}
            
    script_former(dic_coord)
    
    
    return 0

if __name__ == '__main__':
    main()

