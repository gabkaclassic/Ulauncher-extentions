# -*- coding: utf-8 -*-
import requests
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent

class IPInfoExtension(Extension):
    def __init__(self):
        super(IPInfoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        items = []

        try:
            response = requests.get('https://ipinfo.io/json')
            data = response.json()
            
            info = '\n'.join([ f'{field}: {value or "Unknown"}' for field, value in data.items() ])
            items.append(
                ExtensionResultItem(
                    icon='images/icon.png',
                    name=info,
                    description="This is the info corresponding to your IP address.",
                    highlightable=False,
                    on_enter=HideWindowAction(),
                )
            )
        except Exception as e:
            items.append(
                ExtensionResultItem(
                    icon='images/icon.png',
                    name="Error",
                    description=f"Failed to get country information: {e}",
                    highlightable=False,
                    on_enter=HideWindowAction(),
                )
            )

        return RenderResultListAction(items)

if __name__ == '__main__':
    IPInfoExtension().run()

