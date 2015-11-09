#!/usr/bin/env python
#-*- coding:utf-8 -*-

from xml.dom import minidom

def parseXmlFile(fileName):
	xmldoc = minidom.parse(fileName)
	booklist = xmldoc.getElementsByTagName('book')

	for i in booklist:
		for attrName, attrValue in i.attributes.items():
			print("%s = %s" % (attrName, attrValue))
		print i.getElementsByTagName("author")[0].childNodes[0].toxml()
		print i.getElementsByTagName("title")[0].childNodes[0].toxml()
		print i.getElementsByTagName("genre")[0].childNodes[0].toxml()
		print i.getElementsByTagName("price")[0].childNodes[0].toxml()
		print i.getElementsByTagName("publish_date")[0].childNodes[0].toxml()
		print i.getElementsByTagName("description")[0].childNodes[0].toxml()
		print "----------------------------"
		
if __name__ == "__main__":
	parseXmlFile('Books.xml')
