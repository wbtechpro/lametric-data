import requests
import json
from datetime import datetime
from functools import lru_cache

import settings


class BaseFinologBiz:
    FINOLOG_API_BIZ_URL = 'https://api.finolog.ru/v1/biz/'

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        return 'Finolog biz object with id {}'.format(self.biz_id)

    def __repr__(self):
        return self.__str__()

    def get_biz_accounts_API_url(self) -> str:
        """ Return link https://api.finolog.ru/v1/biz/{biz_id}/account """
        if hasattr(self, 'account_ids'):
            return '{}{}/account/{}'.format(self.FINOLOG_API_BIZ_URL, self.biz_id, self.account_ids)
        return '{}{}/account'.format(self.FINOLOG_API_BIZ_URL, self.biz_id)

    def get_biz_transactions_API_url(self) -> str:
        """ Return link https://api.finolog.ru/v1/biz/{biz_id}/tramsaction """
        return '{}{}/transaction'.format(self.FINOLOG_API_BIZ_URL, self.biz_id)

    def get_accounts_response(self):
        return requests.get(self.get_biz_accounts_API_url(), headers={'Api-Token': settings.FINOLOG_API_KEY})

    def get_transactions_response(self, **kwargs):
        return requests.get(
            self.get_biz_transactions_API_url(), headers={'Api-Token': settings.FINOLOG_API_KEY}, params=kwargs)


class FinologBiz(BaseFinologBiz):
    """
    Class represents finolog.ru business instance.
    Methods of class allow to build lametric frames form finolog API's requests.

    Frames for each business:
    1. Summary - sum from all accounts of biz;
    2. Income goal - goal frame with income's sum on current year;
    3. Income chart - chart frame with income by month;
    4. Goal income chart - chart frame with goal income by months with progress bar;
    5. Current month - current month income with progress bar;
    6. Current month goal - current month goal income with progress bar.
    """

    MONTHS_NUMBERS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)

    def get_summary_frame(self):
        """ Example {"icon": "794", "text": "Hello!"} """
        text = '{}{}'.format(round(self._get_account_summary()), self.unit)
        return dict(icon=self.icon, text=text, duration=self.duration)

    def get_income_goal_frame(self):
        """ Example  {"icon": "22835", "goalData": {"start": 0, "current": 6000, "end": 10000, "unit": "MI"}} """
        current = round(self._get_income_transactions_sum_in_current_year())
        result = {"icon": self.icon, "duration": self.duration, "goalData": {
            "start": self.goal_start, "current": current, "end": self.goal_end, "unit": self.unit}}
        return result

    def get_income_chart_frame(self):
        """ Example {"chartData": [1, 10, 15, 20, 6, 9, 11, 16, 22, 24]} """
        chartData = []
        values = self._get_income_transactions_sum_by_month_in_current_year()
        for month in self.MONTHS_NUMBERS:
            chartData.append(round(values[month]))
        return {'chartData': chartData}

    def get_goal_income_chart_frame(self):
        """ Example {"chartData": [1, 10, 15, 20, 6, 9, 11, 16, 22, 24]} """
        chartData = []
        values = self._get_goal_income_by_month_in_current_year()
        for month in self.MONTHS_NUMBERS:
            chartData.append(round(values[month]))
        return {'chartData': chartData}

    def get_current_month_transaction_sum(self):
        """ Example  {"icon": "22835", "goalData": {"start": 0, "current": 6000, "end": 10000, "unit": "MI"}} """
        current_month = round(self._get_current_month_transactions_sum())
        result = {"icon": self.icon, "duration": self.duration, "goalData": {
            "start": self.goal_start, "current": current_month, "end": self.goal_end // 12, "unit": self.unit}}
        return result

    def get_current_month_goal_income(self):
        """ Example  {"icon": "22835", "goalData": {"start": 0, "current": 6000, "end": 10000, "unit": "MI"}} """
        current_month_goal = round(self._get_current_month_goal_income())
        result = {"icon": self.icon, "duration": self.duration, "goalData": {
            "start": self.goal_start, "current": current_month_goal, "end": self.goal_end // 12, "unit": self.unit}}
        return result

    def get_lametric_frames(self):
        return self.get_summary_frame(), self.get_income_goal_frame(), self.get_income_chart_frame(), \
               self.get_goal_income_chart_frame(), self.get_current_month_transaction_sum(), \
               self.get_current_month_goal_income()

    def _get_account_summary(self) -> int:  # in thousands
        response = self.get_accounts_response().json()
        if hasattr(self, 'account_ids'):
            return response['summary'][0]['balance'] / 1000
        summary = sum(map(lambda x: x['summary'][0]['balance'], filter(lambda x: x['summary'], response)))
        return summary / 1000

    def _get_income_transactions_sum_in_current_year(self) -> int:  # in thousands
        return sum(self._get_income_transactions_sum_by_month_in_current_year().values()) / 1000

    @lru_cache()
    def _get_income_transactions_sum_by_month_in_current_year(self) -> dict:
        transactions_by_month = {month: 0 for month in self.MONTHS_NUMBERS}
        current_year = datetime.today().year

        get_params = dict(status='regular', category_type='in')
        if hasattr(self, 'category_ids'):
            get_params['category_ids'] = self.category_ids
        if hasattr(self, 'account_ids'):
            get_params['account_ids'] = self.account_ids

        for transaction in self.get_transactions_response(**get_params).json():
            value, date = transaction['value'], datetime.strptime(transaction['date'], '%Y-%m-%d %H:%M:%S')
            if date.year == current_year:
                transactions_by_month[date.month] += value
        return transactions_by_month

    @lru_cache()
    def _get_goal_income_by_month_in_current_year(self) -> dict:
        transactions_by_month = {month: 0 for month in self.MONTHS_NUMBERS}
        current_year = datetime.today().year

        get_params = dict(status='planned', category_type='in')
        if hasattr(self, 'category_ids'):
            get_params['category_ids'] = self.category_ids
        if hasattr(self, 'account_ids'):
            get_params['account_ids'] = self.account_ids

        for transaction in self.get_transactions_response(**get_params).json():
            value, date = transaction['value'], datetime.strptime(transaction['date'], '%Y-%m-%d %H:%M:%S')
            if date.year == current_year:
                transactions_by_month[date.month] += value
        return transactions_by_month

    def _get_current_month_transactions_sum(self) -> int: # in thousands
        current_month = datetime.today().month

        get_params = dict(status='regular', category_type='in')
        if hasattr(self, 'category_ids'):
            get_params['category_ids'] = self.category_ids
        if hasattr(self, 'account_ids'):
            get_params['account_ids'] = self.account_ids

        month_transaction_sum = 0

        for transaction in self.get_transactions_response(**get_params).json():
            value, date = transaction['value'], datetime.strptime(transaction['date'], '%Y-%m-%d %H:%M:%S')
            if date.month == current_month:
                month_transaction_sum += value
        return month_transaction_sum / 1000

    def _get_current_month_goal_income(self) -> int: # in thousands
        current_month = datetime.today().month

        get_params = dict(status='planned', category_type='in')
        if hasattr(self, 'category_ids'):
            get_params['category_ids'] = self.category_ids
        if hasattr(self, 'account_ids'):
            get_params['account_ids'] = self.account_ids

        month_transaction_sum = 0

        for transaction in self.get_transactions_response(**get_params).json():
            value, date = transaction['value'], datetime.strptime(transaction['date'], '%Y-%m-%d %H:%M:%S')
            if date.month == current_month:
                month_transaction_sum += value
        return month_transaction_sum / 1000


class FramesCatalog:
    biz_bunch = [FinologBiz(**kwargs) for kwargs in settings.FINOLOG_BIZ_SETTINGS]

    def get_frames_data(self):
        #  unpack nested lists:
        frames = [frame for sublist in [biz.get_lametric_frames() for biz in self.biz_bunch] for frame in sublist]
        return dict(frames=frames)

    def get_frames_json(self):
        frames_data = self.get_frames_data()
        json_data = json.dumps(frames_data)
        return json_data
