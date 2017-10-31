import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

WEBSITE_ADDRESS = 'https://www.reformagkh.ru'


def get_soup(url):
    '''
    Gets html page and parses it.

    Args:
        url: str

    Returns:
        BeautifulSoup object
    '''
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}
    html = requests.get(url, headers=headers).text
    return BeautifulSoup(html, 'html.parser')


class House:
    '''
    A class designed for operations on particular house
    from ReformaGKH database.

    Attributes:
        address: str, house's geographical address
        _code: str, number code of the house
        url: str, url of house's info page
        _soup: BeautifulSoup object, parsed webpage
        pass_dict: dict of pandas.DataFrame and pandas.Series,
                   passport info of the house
    '''

    def __init__(self, address, url):
        self.address = address
        self._code = re.search('view\/(.*)', url).group(1)
        self.url = WEBSITE_ADDRESS + url
        self._soup = get_soup(self.url)
        self.pass_dict = self.get_passport()

    def __repr__(self):
        return self.address + ' ' + self.url

    def get_passport(self):
        '''
        Creates a dict with house's passport info.

        Returns:
            dict
        '''
        return {'common_info': self._get_common_info(),
                'constructive_elements': self._get_constructive(),
                'engineering_systems': self._get_engineering(),
                'elevators': self._get_elevators(),
                'metering': self._get_metering()}

    def passport_to_csv(self):
        '''
        Creates csv files for every section of house's passport.
        '''
        for info in self.pass_dict:
            filename = '%s_%s.csv' % (self._code, info)
            self.pass_dict[info].to_csv(filename)

    def _get_common_info(self):
        '''
        Creates a dictionary with house's common info.

        Returns:
            pandas.Series object
        '''
        common_info = pd.Series()
        subtab = self._soup.find(id='tab1-subtab1')
        self._get_table_info(subtab, common_info)
        return common_info

    def _get_constructive(self):
        '''
        Creates a dictionary with house's constructive elements' info.

        Returns:
            pandas.Series object
        '''
        constructive_info = pd.Series()
        subtab = self._soup.find(id='tab1-subtab2')
        self._get_table_info(subtab, constructive_info)
        return constructive_info

    def _get_engineering(self):
        '''
        Creates a dictionary with house's engineering systems info.

        Returns:
            pandas.Series object
        '''
        engineering_info = pd.Series()
        subtab = self._soup.find(id='tab1-subtab3')
        self._get_table_info(subtab, engineering_info)
        return engineering_info

    def _get_elevators(self):
        '''
        Creates a table with house's elevators info.

        Returns:
            pandas.DataFrame object
        '''
        subtab = self._soup.find(id='tab1-subtab4')
        elevators_info = self._get_grid_info(subtab)
        elevators_info.to_csv('elevtors.csv')
        return elevators_info

    def _get_metering(self):
        '''
        Creates a table with house's metering info.

        Returns:
            pandas.DataFrame object
        '''
        subtab = self._soup.find(id='tab1-subtab5')
        metering_info = self._get_grid_info(subtab)
        metering_info.to_csv('metering.csv')
        return metering_info

    def _get_grid_info(self, soup):
        '''
        Creates a table out of grid layout.

        Args:
            soup: BeautifulSoup object

        Returns:
            pandas.DataFrame object
        '''
        keys = soup.find('tr').extract().find_all('th')
        labels = [key.get_text(strip=True) for key in keys]
        values = []
        while soup.tbody:
            grid = soup.tbody.extract()
            vals = []
            for value in grid.tr.extract().find_all('td'):
                val = value.get_text(strip=True)
                if value.has_attr('colspan'):
                    vals += [val] * int(value['colspan'])
                else:
                    vals.append(val)
            values.append(vals)
        info = pd.DataFrame(values, columns=labels)
        return info

    def _get_table_grid_info(self, soup, dictionary):
        '''
        Adds values to a dictionary
        from grid layout stored in col_list layout.

        Args:
            soup: BeautifulSoup object
            dictionary: pandas.Series object
        '''
        while soup.find(class_='grid'):
            grid = soup.find(class_='grid').extract()
            keys_ = grid.tr.extract().find_all('th')
            keys = [key.get_text(strip=True) for key in keys_]
            values = []
            for value in grid.tr.extract().find_all('td'):
                val = value.get_text(strip=True)
                if value.has_attr('colspan'):
                    values += [val] * int(value['colspan'])
                else:
                    values.append(val)
            for key, value in zip(keys, values):
                dictionary[key] = value

    def _get_table_info(self, soup, dictionary):
        '''
        Adds values to a dictionary from col_list layout.

        Args:
            soup: BeautifulSoup object
            dictionary: pandas.Series object
        '''
        while soup.find(class_='col_list'):
            subtab = soup.find(class_='col_list').extract()
            while subtab.tr:
                tr_ = subtab.tr.extract()
                if tr_.has_attr('class'):
                    tr_key = tr_.get_text(strip=True)
                    tr_value = subtab.tr.extract().get_text(strip=True)
                    dictionary[tr_key] = tr_value
                else:
                    self._get_table_info(tr_, dictionary)
        self._get_table_grid_info(soup, dictionary)


class ReformaGKH:
    '''
    A class designed for operations on ReformaGKH website.
    '''

    def get_house(self, address):
        '''
        Finds a particular house on the website and creates a House object.

        Args:
            address: str, house's geographical address

        Returns:
            House object
        '''
        houses = self.get_possible_houses(address)
        house = houses.popitem()
        return House(house[0], house[1])

    def get_possible_houses(self, address):
        '''
        Finds houses (not more than a 100) which fit given address.

        Args:
            address: str, house's geographical address

        Returns:
            dict, keys - addresses, values - urls
        '''
        QUERY = '/search/houses?mh=on&limit=100&query='
        url = WEBSITE_ADDRESS + QUERY + address
        soup = get_soup(url)
        addresses_w_links = soup.tbody.find_all('a')
        links = [link.get('href') for link in addresses_w_links]
        addresses = [link.string for link in addresses_w_links]
        houses = {house: link for house, link in zip(addresses, links)}
        return houses


if __name__ == '__main__':
    h = ReformaGKH().get_house('Петербург Софийская 34 2')
    h.passport_to_csv()
