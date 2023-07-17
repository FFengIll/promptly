import json
from typing import List

import PySimpleGUI as sg  # Part 1 - The import
import loguru

from gui.helper import EventLoop
from prompt.server import api
from prompt.server.event import UpdateEvent
from prompt.server.profile import ProfileManager, Profile

log = loguru.logger

roles = ["system", "user", "assistant"]
sg.set_options(font=("Helvetica", 25))
window_size = (1000, 800)

debug = False

manager = ProfileManager('profile')


def fetch_profile(name):
    if debug:
        return [
            dict(
                key=1, role="system", content="Act as ChatX", history=["123", "123", "123"]
            ),
            dict(key=2, role="user", content="hello", history=["123", "123", "123"]),
        ]

    profile: Profile = manager.get(name)
    if not profile:
        return []

    res = []
    for m in profile.messages:
        item = m.dict()
        res.append(item)

    return res


def fetch_profile_list():
    if debug:
        return ["demo"]

    return manager.list_profile()


def make_node(id, role="system", content="", history=None, **kwargs):
    if history:
        text = sg.DropDown(history, default_value=content, expand_x=True, size=(20, 5))
    else:
        text = sg.DropDown([content], default_value=content, expand_x=True, size=(20, 5))

    node = [
        sg.Text(id),
        sg.DropDown(roles, default_value=role),
        text,
        sg.Checkbox("enable", default=True),
    ]

    return node


def make_chat_request(nodes):
    messages = []
    for _, dd, input, enable in nodes:
        dd: sg.DropDown
        input: sg.Input
        enable: sg.Checkbox

        role = dd.get()
        content = input.get()

        if enable.get():
            messages.append(dict(role=role, content=content))

    print(messages)
    return messages


def load_window(lst: List[str]):
    name = sg.Input(tooltip="Name")

    if not lst:
        lst.append("")

    layout = [
        [
            sg.DropDown(lst, expand_x=True, default_value=lst[0]),
            sg.Button("Load", key="key_load"),
            sg.Button("Export", key="key_load"),
        ],
        [
            name,
            sg.Button("New", key="key_new"),
        ],
    ]

    window = sg.Window("Prompt UI Load", layout=layout, size=window_size)
    while 1:
        event, values = window.read()  # Part 4 - Event loop or Window.read call
        if event == sg.WINDOW_CLOSED:
            break

        elif event == "key_new":
            api.new_profile(name.get())

        elif event == "key_load":
            log.info(values)
            log.info(event)

            key = values[0]
            data = fetch_profile(key)
            chat_window(key, data)


def make_update_event(nodes, res):
    events = []
    history = []

    for id_label, dd, input, enable in nodes:
        id_label: sg.Text
        dd: sg.DropDown
        input: sg.Input

        role = dd.get()
        content = input.get()

        if enable:
            events.append(UpdateEvent(id=id_label.get(), value=content))
            history.append(dict(role=role, content=content))

    print(events)
    history.append(dict(role="assistant", content=res))

    return events, json.dumps(history, ensure_ascii=False)


def chat_window(key, data):
    profile = manager.get(key)

    nodes = [make_node(**i) for i in data]
    response_component = sg.Multiline(size=(0, 8), expand_x=True)

    # Define the window's contents
    btn = sg.Button("Chat", key="key_chat")
    left = [*nodes, [btn], [response_component]]
    view_history = sg.Listbox(values=profile.history, enable_events=True, size=(40, 10), key="key_history")
    text_history = sg.Multiline(size=(0, 10), expand_x=True)

    layout = [
        [
            sg.Column(left),
            sg.VSeperator(),
            sg.Column([[view_history], [text_history]]),
        ]
    ]

    # Create the window
    window = sg.Window(
        "Prompt UI", layout, size=window_size
    )  # Part 3 - Window Defintion

    def event_history(event, values):
        v = values[0]
        print(values)
        cur = window.Element(event).Widget.curselection()
        print()
        v = view_history.get_list_values()[cur[0]]
        v = json.loads(v)[-1]
        v = json.dumps(v, ensure_ascii=False, indent=4)
        text_history.update(v)

    def event_chat(event, values):
        request = make_chat_request(nodes)
        response = api.chat(request)
        text = response["data"]["choices"][0]["message"]
        response_component.update(text)

        update_events, history = make_update_event(nodes, text)
        manager.update(key, update_events)
        manager.history(key, history)

    loop = EventLoop()
    loop.on(btn, event_chat)
    loop.on(view_history, event_history)
    loop.run(window)


def main():
    data = fetch_profile_list()
    load_window(data)

    manager.save()

    # data = fetch_data()
    # window = chat_window(data)


if __name__ == '__main__':
    main()
