from pydantic import  BaseModel
class Event(BaseModel):
    """
    For event:
    each event maybe trigger by UI component with or without args.
    all args must come from the components like text / select and so on.
    we call the event `Update Event`.

    then the event may come with an action, we call `Action Event`.
    this event means to do some actions (e.g. send a requests to server).

    after all above, there must comes a `Response Event`.
    this event will send from backend server to front, with more events should be used to update UI.

    of course, the event can work in duplex mode.
    """

    pass


class UpdateEvent(Event):
    node: str = ""
    id: int
    key: str
    value: str | int | float



class ActionEvent(Event):
    name: str
    node: str