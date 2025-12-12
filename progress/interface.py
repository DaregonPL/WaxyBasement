from progress.core import Session, init_db
from progress.tables import User
import json


def add_user(user_id, name, user_data):
    new_user = User(
        id=user_id,
        name=name,
        scene=user_data['pos'][0],
        page=user_data['pos'][1],
        player_meta=json.dumps(user_data['meta']),
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
            "meta": json.loads(user_data.player_meta),
            "inventory": json.loads(user_data.inventory)
        }
    return user_data


def update_user(user_id, user_data):
    with Session() as session:
        user_object = session.get(User, user_id)
        user_object.scene = user_data['pos'][0]
        user_object.page = user_data['pos'][1]
        user_object.player_meta = json.dumps(user_data['meta'])
        user_object.inventory = json.dumps(user_data['inventory'])
        session.commit()
        #print("User[{}] updated to {}".format(user_id, get_user(user_id, True)))


def delete_user(user_id):
    with Session() as session:
        session.delete(user_id)


def run():
    init_db()


if __name__ == "__main__":
    run()
    user = get_user(0, True)
    print(user)
    print(get_user(1))
    update_user(0, {"pos": [user["pos"][0], user["pos"][1] + 1], "inventory":user["inventory"], "meta": user["meta"]})
