from progress.core import Session, init_db
from progress.tables import User
import json


def add_user(user_id, name, user_data):
    new_user = User(
        id=user_id,
        name=name,
        scene=user_data['pos'][0],
        page=user_data['pos'][1],
        inventory=json.dumps(user_data['inventory'])
    )
    with Session() as session:
        session.add(new_user)
        session.commit()

def get_user(user_id, to_format=False):
    with Session() as session:
        user_data = session.get(User, user_id)
    if not user_data:
        return None
    if to_format:
        user_data = {
            "pos": [
                user_data.scene,
                user_data.page
            ],
            "inventory": json.loads(user_data.inventory)
        }
    return user_data

def update_user(user_id, user_data):
    user = get_user(user_id)
    user.scene = user_data['pos'][0]
    user.page = user_data['pos'][1]
    user.inventory = json.dumps(user_data['inventory'])
    with Session() as session:
        session.commit()


def run():
    init_db()


if __name__ == "__main__":
    run()
    add_user(0, 'MiniVan', {
        "pos": ["start", 0],
        "inventory": []
    })
    print(get_user(0, True))
    print(get_user(1))
