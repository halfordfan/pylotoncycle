#!/usr/bin/env python3

# endpoint info derived from
# https://github.com/philosowaffle/postman_collections/blob/master/PelotonCycle/

# import pprint
import requests


class PylotonCycle:
    def __init__(self, username, password):
        self.base_url = 'https://api.onepeloton.com'
        self.s = requests.Session()
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'pyloton'
        }

        self.userid = None
        self.login(username, password)

    def login(self, username, password):
        auth_login_url = '%s/auth/login' % self.base_url
        auth_payload = {
            'username_or_email': username,
            'password': password
        }
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'pyloton'
        }
        resp = self.s.post(
            auth_login_url, json=auth_payload, headers=headers).json()
        self.id = resp['user_id']
        self.total_workouts = resp['user_data']['total_workouts']
        # pprint.pprint(resp.json())

    def GetMe(self):
        url = '%s/api/me' % self.base_url
        resp = self.s.get(url).json()
        self.username = resp['username']
        self.id = resp['id']
        self.total_workouts = resp['total_workouts']
        return resp

    def GetUrl(self, url):
        resp = self.s.get(url).json()
        return resp

    def GetWorkoutList(self, num_workouts=None):
        if num_workouts is None:
            num_workouts = self.total_workouts

        limit = 100
        pages = num_workouts // limit
        rem = num_workouts % limit

        base_workout_url = \
            '%s/api/user/%s/workouts?sort_by=-created' % (
                self.base_url, self.id)

        workout_list = []
        current_page = 0
        for i in range(0, pages):
            url = '%s&page=%s&limit=%s' % (
                base_workout_url, current_page, limit)
            resp = self.s.get(url).json()
            workout_list.extend(resp['data'])
            current_page += 1

        if rem != 0:
            url = '%s&page=%s&limit=%s' % (base_workout_url, current_page, rem)
            resp = self.s.get(url).json()
            workout_list.extend(resp['data'])

        return workout_list

    def GetRecentWorkoutSummaries(self, num_workouts=None):
        workout_list = self.GetWorkoutList(num_workouts)
        workout_detailed_list = []
        for i in workout_list:
            workout_id = i['6a0520b113294a3d80b67891c4939d58']
            resp = self.GetWorkoutSummaryById(workout_id)
            workout_detailed_list.append(resp)
        return workout_detailed_list

    def GetWorkoutSummaryById(self, workout_id):
        url = '%s/api/workout/%s/summary' % (self.base_url, workout_id)
        resp = self.GetUrl(url)
        return resp

    def GetWorkoutMetricsById(self, workout_id):
        url = '%s/api/workout/%s/performance_graph' % (
            self.base_url, workout_id)
        resp = self.GetUrl(url)
        return resp

    def GetWorkoutById(self, workout_id):
        url = '%s/api/workout/%s' % (self.base_url, workout_id)
        resp = self.GetUrl(url)
        return resp

    def GetWorkoutInfo(self, workout_id):
        workout_dict = self.GetWorkoutById(workout_id)
        workout_dict['overall_summary'] = \
            self.GetWorkoutSummaryById(workout_id)
        return workout_dict

    def ParseMetricsData(self, metrics_data):
        # TODO
        pass
        # ride_metrics_dict = {}
        # ride_metrics = metrics_data['metrics']
        # metrics_chunks = metrics_data['seconds_since_pedaling_start']
        # number_of_chunks = len(metrics_chunks)
        # for i in range(0, number_of_chunks):
        #     ride_metrics_dict[i] =


if __name__ == '__main__':
    username = 'My_Peloton_User_or_Email'
    password = 'My_Peloton_Password'
    conn = PylotonCycle(username, password)