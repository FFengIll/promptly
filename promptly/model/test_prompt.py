from .prompt import Prompt, Message, CommitItem


def test_prompt_model():
    p = Prompt(name="", messages=[])
    print(p.dict())


def test_model():
    res = Prompt.parse_obj(dict(name="", messages=[]))
    print(res)


def test_json():
    for i in range(5):
        m = Message(role="1", content="123")
        print(m.json())


def test_commit():
    for i in range(5):
        c = CommitItem()
        print(c.md5)
