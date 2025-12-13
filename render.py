from engine import Engine
from progress.interface import run as init_db
from os import path
from os import mkdir
import json


class ConsoleRenderer:
    def __init__(self,  player_id):
        self.player = player_id
        self.engine = None

    def run(self, map_path):
        with open(map_path, encoding='utf-8') as f:
            map_data = json.load(f)
        self.engine = Engine()
        self.engine.load_map(map_data)
        init_db()
        data = self.engine.process(self.player, '')
        fwd: bool = True
        print("type \".\" to change chronology, \"inv\" to show inventory or \"..\" to get in the start of scene")
        while True:
            actions = data['actions']
            action = ''
            usr = [act for act in actions if act[0] == 'user']
            if usr:
                print("Type number or \".\"" if ('system', 'prev') in actions else "Type number")
                for i in range(0, len(usr)):
                    print('{}. {}'.format(i + 1, usr[i][1]))
                ans = input(data['text'])
                if ans == 'inv':
                    for slot in self.engine.get_inventory(self.player, True):
                        print(f' |{slot[0]}: {slot[1]}')
                    continue
                if ans == '..':
                    action = ('absolute_navigation', 'scene_top')
                elif ans == '.' and ('system', 'prev') in actions:
                    action = ('system', 'prev')
                    fwd = False
                    print('Chronology: INVERTED')
                elif ans.isdigit() and int(ans) in range(1, len(usr) + 1):
                    action = usr[int(ans) - 1]
                else:
                    continue
            elif len(actions) == 1 and actions[0][0] == 'absolute_navigation':
                input(data['text'])
                action = actions[0]
            else:
                ans = input(data['text'])
                if ans == 'inv':
                    for slot in self.engine.get_inventory(self.player, True):
                        print(f' |{slot[0]}: {slot[1]}')
                    continue
                if ans == '.':
                    fwd = not fwd
                    print('Chronology: {}'.format("STRAIGHT" if fwd else "INVERTED"))
                if ('system', 'prev') not in actions:
                    if not fwd:
                        print('Chronology: STRAIGHT')
                    fwd = True

                action = ('system', 'prev' if not fwd else 'next')
                if ans == '..':
                    action = ('absolute_navigation', 'scene_top')
                if ('system', 'next') not in actions:
                    action = ()
                    for action in actions + [action]:
                        if action[0] == 'absolute_navigation':
                            break
                    if not action:
                        raise Exception(f'RendererError: cannot display actions: {actions}')
            data = self.engine.process(self.player, action)


if __name__ == '__main__':
    map_dir: str = "maps_data"
    map_name = "WBv0test"
    if not path.exists(map_dir):
        mkdir(map_dir)
        with open(path.join(map_dir, map_name + '.json'), 'w') as f:
            json.dump({}, f)
        raise Exception('map_dir created')

    render = ConsoleRenderer(0)
    render.run(path.join(map_dir, map_name + '.json'))