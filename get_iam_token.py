#!/usr/bin/python3

import json
from os import system
import datetime


class IAMtoken(object):
    def __init__(self):
        self.full_token = self.load_iam_token()
        self.iam_token = self.check_iam_token(self.full_token)
        if not self.full_token or not self.iam_token:
            self.create_new_iam_token()
            self.full_token = self.load_iam_token()
            self.iam_token = self.full_token['iamToken']

    @staticmethod
    def load_iam_token(filename='iam.token'):
        try:
            with open(filename, 'r') as file:
                full_token = json.load(file)
                return full_token
        except FileNotFoundError:
            return False

    @staticmethod
    def create_new_iam_token():
        system('./token.sh')

    @staticmethod
    def check_iam_token(full_token):
        if not full_token:
            return False
        iam_token = full_token['iamToken']
        now = datetime.datetime.now()
        date_time = full_token['expiresAt'].split('T')
        date = date_time[0].split('-')
        time = date_time[1].split(':')
        time.pop()
        time = time[0].split(':')
        year_token = int(date[0])
        month_token = int(date[1])
        day_token = int(date[2])
        hour_token = int(time[0])
        if (now.year == year_token) and (now.month == month_token):
            if now.day < day_token:
                return  iam_token
            elif (now.day == day_token) and (now.hour < hour_token):
                return iam_token
        else:
            return False

    def give(self):
        return self.iam_token


if __name__ == '__main__':
    token = IAMtoken()
    print(token.give())
