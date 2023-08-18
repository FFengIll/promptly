import datetime

from sqlmodel import Session, select

from promptly.dao.mongo import Profile, client
from promptly.dao.sql import Message, create_db_and_tables, engine


def test_sql():
    create_db_and_tables()
    sess = Session(engine)

    q = select(Message).where(Message.profile_id == 1)
    res = sess.exec(q)
    for i in res:
        print(i)


def test_mongo():
    db = client.test_db

    posts = db.posts

    post = {
        "author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
    }
    post_id = posts.insert_one(post).inserted_id

    print(post_id)
