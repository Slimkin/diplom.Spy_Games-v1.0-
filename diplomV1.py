import requests
import time
from pprint import pprint

class User:

    def __init__(self, ids, token):
        self.id = ids
        self.token = token

    def reqGet(self, method, params=None, reply=0):
        _params = {'v': 5.103, 'access_token': self.token}
        if params:
            _params.update(params)
        time.sleep(0.4)
        resp = requests.get(
            f'https://api.vk.com/method/{method}', params=_params)
        if resp.status_code != 200:
            return
        if 'error' in resp.json():
            data = resp.json()['error']
            if data['error_code'] == 30 or data['error_code'] == 18:
                return
            if data['error_code'] == 6:
                if reply > 3:
                    return
                time.sleep(2)
                res = self.reqGet(method, params, reply + 1)
                return res.json()
        return resp.json()
    
    def get_id(self):
        try:
            if self.id >= 0:
                user_id = self.id
        except TypeError:
            user_id = self.reqGet('utils.resolveScreenName', params={
                'screen_name': self.id})['response']['object_id']
        return user_id


    def private_groups(self):

        resp_groups = self.reqGet('groups.get', params={'user_id': self.get_id()})
        result = resp_groups['response']
        user_groups_list = set(result['items'])

        resp_friends = self.reqGet('friends.get', params={'user_id': self.get_id()})
        result = resp_friends['response']
        user_friends_list = result['items']

        friends_groups_list = []
        count_frends = len(user_friends_list)
        
        for index, friend in enumerate(user_friends_list):
            print(f' Processing: {index / count_frends * 100:.2f}%', end='\r')
            resp = self.reqGet('groups.get', params={'user_id': friend})
            if resp == None:
                continue
            else:
                result = resp['response']
                friend_groups_list = result['items']
                for group in friend_groups_list:
                    friends_groups_list.append(group)

        sort_group_list = set(friends_groups_list)
        private_user_groups = str(list(user_groups_list.difference(sort_group_list)))
        
        result = self.reqGet('groups.getById', params={'group_ids': private_user_groups.strip('[]')})
        pprint(result['response'])


user = User(
    'eshmargunov', '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008')
user.private_groups()