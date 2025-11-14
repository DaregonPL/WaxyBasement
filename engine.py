import json


class Engine:
    def __init__(self):
        self.map = None
        self.progress = None

    def load_map(self, map_data: dict):
        self.map = map_data

    def load_progress(self, progress_fp: str):
        self.progress = progress_fp

    def get_progress(self, player: int):
        player = str(player)
        with open(self.progress, encoding='utf-8') as f:
            progress = json.load(f)
        return progress[player] if player in progress else None

    def update_progress(self, player: int, player_progress: dict):
        player = str(player)
        with open(self.progress, encoding='utf-8') as f:
            progress = json.load(f)
        progress[player] = player_progress
        with open(self.progress, encoding='utf-8', mode='w') as f:
            json.dump(progress, f, indent=4, ensure_ascii=False)

    def available_actions(self, player: int):
        progress = self.get_progress(player)
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
        progress = self.get_progress(player)
        if not progress:
            self.update_progress(player, self.map["new_player"])
            return self.process(player, action)
        scene, scene_prog = progress['pos']
        if not action:
            return {
                "text": self.map['scenes'][scene]['text'][scene_prog],
                "actions": self.available_actions(player)
            }
        if action[0] == 'system':
            if action[1] == 'next':
                progress['pos'][1] += 1
            if action[1] == 'prev':
                progress['pos'][1] -= 1
            self.update_progress(player, progress)
        if action[0] == 'user':
            links = self.map['scenes'][scene]['links']
            found = None
            for link in links:
                if action[1] == link['text']:
                    found = link['scene']
                    break
            if not found:
                return None
            progress['pos'] = [found, 0]
            self.update_progress(player, progress)

        return {
            "text": self.map['scenes'][progress['pos'][0]]['text'][progress['pos'][1]],
            "actions": self.available_actions(player)
        }