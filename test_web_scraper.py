import web_scraper
from pandas.testing import assert_frame_equal
import re
import pandas as pd


def test_scraper():
    names, prices, watchers = web_scraper.scraper('https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=toilet%20paper')
    for price in prices:
        assert bool(re.match(r'^[^0-9 to.]+[0-9,.]+( to )?([^0-9 to.][0-9,.]+)?$', price))
    for watcher in watchers:
        assert bool(re.match(r'^[0-9]+ (watchers|sold)$', watcher))


def test_data_cleaning():
    test_names = ['Banana', 'Apple', 'Oranges']
    test_prices = ['IDR3,289.35', 'IDR5,691.22 to IDR 10,399.22', 'IDR15,301.55']
    test_watchers = ['150 sold', '55 watchers', '0 watchers']
    test_df = pd.DataFrame({'Name': ['Banana', 'Apple', 'Oranges'], 'Lower Price': [3289.35, 5691.22, 15301.55], 'Upper Price': [3289.35, 10399.22, 15301.55], 'Watchers': [0, 55, 0], 'Sold': [150, 0, 0]})
    assert_frame_equal(test_df, web_scraper.data_cleaning(test_names, test_prices, test_watchers))


def test_data_summary():
    test_data_frame = pd.DataFrame({'Name': ['Banana', 'Apple', 'Oranges'], 'Lower Price': [3289.35, 5691.22, 15301.55], 'Upper Price': [3289.35, 10399.22, 15301.55], 'Watchers': [0, 55, 0], 'Sold': [150, 0, 0]})
    assert web_scraper.data_summary(test_data_frame) == '''
    Price Summary:
    Lower Average Price = 8094.04
    Upper Average Price = 9663.373333333333
    Lower Median Price = 5691.22
    Upper Median Price = 10399.22
    
    Watchers Summary:
    Average Watchers = 18.333333333333332
    Standard Deviation = 31.75426480542942
    Zero Watchers = 2/3
    
    Sold Summary:
    Average Number Sold = 50.0
    Standard Deviation = 86.60254037844386
    Zero Sold = 2/3
    '''


def test_name_frequency():
    test_data_frame = pd.DataFrame({'Name': ['Soft, sturdy running shoes', 'Nike Air Max running shoes', 'Soft, sturdy Nike running shoes'], 'Lower Price': [3289.35, 5691.22, 15301.55],
                                    'Upper Price': [3289.35, 10399.22, 15301.55], 'Watchers': [0, 55, 0],
                                    'Sold': [150, 0, 0]})
    test_frequency = pd.DataFrame({'Word': ['Soft', 'sturdy', 'Nike', 'Air', 'Max'], 'Frequency': [2, 2, 2, 1, 1]})
    assert_frame_equal(test_frequency, web_scraper.name_frequency(test_data_frame))



