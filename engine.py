from progress.interface import add_user, get_user, update_user


def check_req(requirement: dict, inventory:dict):
    itemid = requirement["ItemID"]
    cond = requirement['amount']
    if itemid in inventory:
        num = inventory[itemid]
        if cond.startswith("="):
            return num == int(cond[1:])
        if cond.startswith(">"):
            return num > int(cond[1:])
        if cond.startswith("<"):
            return num < int(cond[1:])
        raise Exception('MapReaderError: "{}" is wrong format. Use "=[num]", ">[num]" or "<[num]"')
    else:
        return cond == "=0"

class Engine:
    def __init__(self):
        self.map = None

    def load_map(self, map_data: dict):
        self.map = map_data

    def get_inventory(self, player: int, to_format=False):
        user_data = get_user(player, to_format=True)
        if to_format:
            items_data = self.map["items"]
            inventory = []
            for item, amount in user_data['inventory'].items():
                item_data = {"ItemID": item, "Name": item, "MaxAmount": None}
                for item_data in items_data + [item_data]:
                    if item_data["ItemID"] == item:
                        break
                inventory.append((item_data["Name"], amount))
            return inventory
        return user_data['inventory']

    def get_meta(self, player:int):
        user_data = get_user(player, to_format=True)
        return user_data['meta']

    def update_inventory(self, player: int, inventory: dict):
        user_data = get_user(player, to_format=True)
        user_data['inventory'] = inventory
        update_user(player, user_data)

    def update_mep(self, player: int, meta: dict):
        user_data = get_user(player, to_format=True)
        user_data['meta'] = meta
        update_user(player, user_data)

    def available_actions(self, player: int):
        progress = get_user(player, True)
        scene, scene_prog = progress['pos']
        text = self.map['scenes'][scene]['text']
        actions = []
        if scene_prog > 0:
            actions.append(('system', 'prev'))
        if scene_prog < len(text) - 1:
            actions.append(('system', 'next'))
        if scene_prog == len(text) - 1:
            inv = self.get_inventory(player)
            for link in self.map['scenes'][scene]['links']:
                print(link)
                if "check_inv" in link and not all([check_req(req, inv) for req in link["check_inv"]]):
                    print('rejected')
                    continue
                actions.append(('user', link['text']))
        return actions

    def process(self, player: int, action: str):
        progress = get_user(player, True)
        if not progress:
            add_user(player, "NONAME", self.map["new_player"])
            return self.process(player, action)
        scene, scene_prog = progress['pos']
        if not action:
            pass
        elif action[0] == 'absolute_navigation':
            if action[1] == 'scene_top':
                progress['pos'][1] = 0
            update_user(player, progress)
        elif action[0] == 'system':
            if action[1] == 'next':
                progress['pos'][1] += 1
            if action[1] == 'prev':
                progress['pos'][1] -= 1
            update_user(player, progress)
        elif action[0] == 'user':
            links = self.map['scenes'][scene]['links']
            found = None
            for link in links:
                if action[1] == link['text']:
                    found = link['scene']
                    break
            if not found:
                return None
            progress['pos'] = [found, 0]
            update_user(player, progress)

        return {
            "text": self.map['scenes'][progress['pos'][0]]['text'][progress['pos'][1]],
            "actions": self.available_actions(player)
        }