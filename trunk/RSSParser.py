#! /usr/bin/env python

from google.appengine.api import urlfetch
from xml.dom import minidom, Node

class RSSItem:
	"""This is an RSS item, it contain all the RSS info like Tile and Description"""
	def __init__(self,title="",description=""):
		self.title = title
		self.description = description

class RSSReader:
	"""This class is an RSS reader, it should have a better docstring"""
	
	def __init__(self,RSSUrl):
		"""Initialize the class"""
		self.RSSUrl = RSSUrl;
		self.xmldoc = self.GetXMLDocument(RSSUrl)
		if (not self.xmldoc):
			print "Error Getting XML Document!"
		
	def GetXMLDocument(self,RSSUrl):
		"""This function reads in a RSS URL and then"""
		"""returns the XML documentn on success"""
		xmldoc = None		
		result = urlfetch.fetch(RSSUrl)
		if result.status_code == 200:
			xmldoc = minidom.parseString(result.content)
		else	:
			print "Error Getting URL"
		return xmldoc
	
	def GetItemText(self,xml_node):
		"""Get the text from an xml item"""
		text = ""
		for text_node in xml_node.childNodes:
			if (text_node.nodeType == Node.TEXT_NODE):
				text += text_node.nodeValue
		return text
	
	def GetChildText(self, xml_node, child_name):
		"""Get a child node from the xml node"""
		if (not xml_node):
			print "Error GetChildNode: No xml_node"
			return ""
		for item_node in xml_node.childNodes:
			if (item_node.nodeName==child_name):
				return self.GetItemText(item_node)
		"""Return Nothing"""
		return ""
	
	def CreateRSSItem(self,item_node):
		"""Create an RSS item and return it"""
		title = self.GetChildText(item_node,"title")
		description = self.GetChildText(item_node,"description")
		return RSSItem(title,description)
	
	def GetItems(self):
		"""Generator to get items"""
		for item_node in self.xmldoc.documentElement.childNodes:
			if (item_node.nodeName == "item"):
				"""Allright we have an item"""
				rss_item = self.CreateRSSItem(item_node)
				yield rss_item
			elif(item_node.nodeName == "channel"):
				for item_node_into_channel in item_node.childNodes:               
					if (item_node_into_channel.nodeName == "item"):
						rss_item = self.CreateRSSItem(item_node_into_channel)
						yield rss_item					
