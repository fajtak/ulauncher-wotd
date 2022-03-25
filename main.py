import requests
from bs4 import BeautifulSoup as soup

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

def gen_url(link):
	base_url = "https://www.helpforenglish.cz"
	return base_url + str(link)

class WotDExtension(Extension):

	def __init__(self):
		super(WotDExtension, self).__init__()
		self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):

	def on_event(self, event, extension):
		items = []
		url = "https://www.helpforenglish.cz"

		page = requests.get(url)
		page_soup = soup(page.content,"html.parser")

		word_of_the_day = page_soup.find("div","word-of-the-day-word")
		word_of_the_day_czech = page_soup.find("a","word-of-the-day")
		# print(word_of_the_day.text)
		# # print(word_of_the_day_czech)
		# print(word_of_the_day_czech.contents[4])

		items.append(ExtensionResultItem(icon='images/icon.png',
											name='%s' % (word_of_the_day.text),
											description='%s' % (str(word_of_the_day_czech.contents[4])),
											on_enter=OpenUrlAction(gen_url(word_of_the_day_czech["href"]))))

		return RenderResultListAction(items)

if __name__ == '__main__':
	WotDExtension().run()