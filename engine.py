import json
from progress.interface import run as init_db, add_user, get_user, update_user


class Engine:
    def __init__(self):
        self.map = None
        self.progress = None

    def load_map(self, map_data: dict):
        self.map = map_data

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
            for link in self.map['scenes'][scene]['links']:
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