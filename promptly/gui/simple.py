import json
from typing import List

# import PySimpleGUIWeb as sg
import loguru
import pandas as pd
import PySimpleGUI as sg

from gui.helper import EventLoop
from promptly.server import llm
from promptly.model.event import UpdateEvent
from promptly.model.prompt import Profile, ProfileManager

log = loguru.logger

roles = ["system", "user", "assistant"]
sg.set_options(font=("Helvetica", 25))
window_size = (1000, 800)

debug = False

manager = ProfileManager("profile")
# manager = ProfileManager('database.pickle.db')
df = pd.read_csv("profile/history.csv")


def test_pd():
    global df
    df.loc[len(df.index)] = [1, 2]
    print(df)


def fetch_profile(name):
    if debug:
        return [
            dict(
                key=1,
                role="system",
                content="Act as ChatX",
                history=["123", "123", "123"],
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


def make_chat_request(nodes):
    messages = []
    for n in nodes:
        n: InputNode

        role = n.role
        content = n.content
        enable = n.enable

        if enable:
            messages.append(dict(role=role, content=content))

    print(messages)
    return messages


def load_window():
    global manager
    lst = manager.keys()

    name = sg.Input(tooltip="Name")

    dd = sg.DropDown(lst, expand_x=True, default_value=lst[0] if len(lst) else "")

    layout = [
        [
            dd,
            sg.Button("Load", key="key_load"),
            sg.Button("Export", key="key_load"),
        ],
        [
            name,
            sg.Button("New", key="key_new"),
            sg.Button("Refresh", key="key_refresh"),
        ],
    ]

    window = sg.Window("Prompt UI Load", layout=layout)
    while 1:
        # manager.refresh()

        event, values = window.read()  # Part 4 - Event loop or Window.read call
        if event == sg.WINDOW_CLOSED:
            break

        elif event == "key_new":
            # manager.add(name.get())
            lst = manager.keys()
            dd.update(value=name.get(), values=lst)
            window.refresh()

        elif event == "key_load":
            log.info(values)
            log.info(event)

            key = values[0]
            data = fetch_profile(key)
            subwindow = ChatWindow(key, data)
            subwindow.activate()

        elif event == "key_refresh":
            manager.save()
            manager = ProfileManager("profile")
            lst = manager.keys()
            dd.update(value=name.get(), values=lst)
            window.refresh()


def make_update_event(nodes: List["InputNode"], res):
    events = []
    history = []

    for n in nodes:
        role = n.role
        content = n.content

        if n.enable:
            events.append(UpdateEvent(id=n.id, value=content))
            history.append(dict(role=role, content=content))

    print(events)
    history.append(dict(role="assistant", content=res))

    return events, json.dumps(history, ensure_ascii=False)


class InputNode:
    def __init__(
        self, loop: EventLoop, id, role="system", content="", history=None, **kwargs
    ):
        if not history:
            history = [content]

        dd = sg.DropDown(
            history,
            enable_events=True,
            default_value=content,
            expand_x=True,
            size=(20, 5),
        )

        dd.Key = loop.generate_key()
        text = sg.Multiline(size=(0, 4), expand_x=True, default_text=content)
        role = sg.DropDown(roles, default_value=role)
        cb_enable = sg.Checkbox("enable", default=True)
        text_id = sg.Text(id)
        layout = [
            [
                text_id,
                role,
                dd,
                cb_enable,
            ],
            [text],
        ]

        def update_text(event, values):
            value = values[event]
            text.update(value)
            log.info("update")

        loop.on(dd.key, update_text)
        self.input_id = text_id
        self.input_content = text
        self.dd_role = role
        self.cb_enable = cb_enable
        self.frame = sg.Frame(title="", layout=layout)

    @property
    def id(self):
        return self.input_id.get()

    @property
    def content(self):
        return self.input_content.get()

    @property
    def enable(self):
        return self.cb_enable.get()

    @property
    def role(self):
        return self.dd_role.get()

    def element(self):
        return self.frame


class ChatWindow(EventLoop):
    def __init__(self, key, data):
        super().__init__()
        self.key = key
        self.data = data
        self.window: sg.Window = sg.Window(
            "Prompt UI", resizable=True
        )  # Part 3 - Window Defintion

    def make_node(self, id, role="system", content="", history=None, **kwargs):
        return InputNode(self, id, role, content, history)

    def activate(self):
        key = self.key
        data = self.data

        profile = manager.get(key)

        nodes = [self.make_node(**i) for i in data]
        response_component = sg.Multiline(size=(40, 8))

        # Define the window's contents
        btn_chat = sg.Button("Chat", key="key_chat")
        btn_refresh = sg.Button("Refresh", key="key_refresh")
        left = [[i.element()] for i in nodes]
        view_history = sg.Listbox(
            values=profile.history, enable_events=True, size=(40, 10), key="key_history"
        )
        text_history = sg.Multiline(size=(0, 10), expand_x=True)

        layout = [
            [
                sg.Column(left),
                sg.VSeperator(),
                sg.Column([[btn_chat], [response_component]])
                # sg.Column([[view_history], [text_history]]),
            ]
        ]

        # Create the window
        window = self.window
        window.layout(layout)
        window.maximized = True
        window.refresh()

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
            try:
                response = api.chat(request)
            except Exception as e:
                log.exception(e)
                return
            text = response["data"]["choices"][0]["message"]
            response_component.update(text)

            update_events, history = make_update_event(nodes, text)
            manager.update(key, update_events)

            save_history(nodes, text)

        self.on(btn_chat, event_chat)
        # self.on(view_history, event_history)
        self.run(window)

        manager.save()


def save_history(nodes, text):
    global df
    df.loc[len(df.index)] = ["", ""]
    for n in nodes:
        if n.enable:
            df.loc[len(df.index)] = [n.role, n.content]

    df.loc[len(df.index)] = ["", text]
    df.to_csv("profile/history.csv", index=False)


def main():
    load_window()
    manager.save()
    # data = fetch_data()
    # window = chat_window(data)


if __name__ == "__main__":
    main()
