from bs4 import BeautifulSoup
import re
import sys
import requests
import pandas as pd
from pandas import Series
import matplotlib.pyplot as plt


def scraper(link):
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'html.parser')
    item_list = soup.find('div', class_='srp-river-results clearfix')
    items = item_list.find_all('li', class_='s-item s-item__pl-on-bottom')
    name_data = []
    price_data = []
    watchers_data = []
    i = 0
    for item in items:
        i += 1
        item_name = item.find('span', role='heading').text
        name_data.append(item_name)
        item_price = item.find('span', class_='s-item__price').text
        price_data.append(item_price)

        #filters for span whose class name is EXACTLY "BOLD"
        item_watchers_list = item.select('span[class="BOLD"]')

        #removes span element not containing watchers or sold number
        pattern = re.compile(r'\d+(\+)? (watchers|sold).+')
        item_watchers = list(filter(lambda s: pattern.search(str(s)), item_watchers_list))

        # if no watchers
        if len(item_watchers) == 0:
            watchers_data.append("0 watchers")
        else:
            watchers_data.append(item_watchers[0].text)

    return name_data, price_data, watchers_data


def data_cleaning(names, prices, watchers):
    formatted_prices = []
    lower_price = []
    upper_price = []
    watchers_number = []
    sold_number = []
    for i in range(len(names)):
        remove_commas = watchers[i].replace(',', '')
        match_watchers = re.match(r'(\d+)(\+)? (sold|watchers)', remove_commas)
        formatted_watchers = match_watchers.group(1)
        #removes currency prefix
        formatted_prices.append(re.sub(r'[^0-9 to.]', '', prices[i]))
        if 'to' in prices[i]:
            lower_price.append(formatted_prices[i].split(' to ')[0])
            upper_price.append(formatted_prices[i].split(' to ')[1])
        else:
            lower_price.append(formatted_prices[i])
            upper_price.append(formatted_prices[i])
        if not 'watchers' in watchers[i]:
            watchers_number.append('0')
        else:
            watchers_number.append(formatted_watchers)
        if not 'sold' in watchers[i]:
            sold_number.append('0')
        else:
            sold_number.append(formatted_watchers)

    df = pd.DataFrame(
        {'Name': names, 'Lower Price': lower_price, 'Upper Price': upper_price, 'Watchers': watchers_number,
         'Sold': sold_number})
    df['Lower Price'] = pd.to_numeric(df['Lower Price'])
    df['Upper Price'] = pd.to_numeric(df['Upper Price'])
    df['Sold'] = pd.to_numeric(df['Sold'])
    df['Watchers'] = pd.to_numeric(df['Watchers'])
    return df


def data_summary(df):
    count = len(df)
    lower_mean_price = df['Lower Price'].mean()
    upper_mean_price = df['Upper Price'].mean()
    lower_median_price = df['Lower Price'].median()
    upper_median_price = df['Upper Price'].median()
    mean_watchers = df['Watchers'].mean()
    std_watchers = df['Watchers'].std()
    zero_watchers = len(df[df['Watchers'] == 0])
    mean_sold = df['Sold'].mean()
    std_sold = df['Sold'].std()
    zero_sold = len(df[df['Sold'] == 0])
    return f'''
    Price Summary:
    Lower Average Price = {lower_mean_price}
    Upper Average Price = {upper_mean_price}
    Lower Median Price = {lower_median_price}
    Upper Median Price = {upper_median_price}
    
    Watchers Summary:
    Average Watchers = {mean_watchers}
    Standard Deviation = {std_watchers}
    Zero Watchers = {zero_watchers}/{count}
    
    Sold Summary:
    Average Number Sold = {mean_sold}
    Standard Deviation = {std_sold}
    Zero Sold = {zero_sold}/{count}
    '''


def name_frequency(df):
    # removes punctuation from Name column
    df['Name'] = df['Name'].apply(lambda x: re.sub(r'[^\w\s]', '', x))
    # finds top 5 most frequent words in product name except search keywords itself
    frequency_count = Series(' '.join(df.Name).split()).value_counts()[2:7]
    df_frequency = pd.DataFrame({'Word': frequency_count.index, 'Frequency': frequency_count.values})
    return df_frequency


def data_visualization(df, df_frequency):
    plt.bar(df_frequency['Word'], df_frequency['Frequency'], color='blue', width=0.5)
    plt.show()
    if df['Lower Price'].equals(df['Upper Price']):
        fig, axs = plt.subplots(1, 3, figsize=(9, 3))
        axs[0].scatter(df['Lower Price'], df['Sold'])
        axs[0].set_title('Items Sold Data')
        axs[0].set_xlabel('Price')
        axs[0].set_ylabel('No. of Sales')
        axs[1].scatter(df['Lower Price'], df['Watchers'])
        axs[1].set_title('Watchers Data')
        axs[1].set_xlabel('Price')
        axs[1].set_ylabel('No. of Watchers')
        axs[2].bar(df_frequency['Word'], df_frequency['Frequency'])
        axs[2].set_title('Word Frequency Data')
        axs[2].set_xlabel('Word')
        axs[2].set_ylabel('Frequency')
        plt.show()
    else:
        fig = plt.figure()
        fig.set_figheight(9)
        fig.set_figwidth(9)
        ax1 = plt.subplot2grid(shape=(3, 2), loc=(0, 0))
        ax2 = plt.subplot2grid(shape=(3, 2), loc=(0, 1))
        ax3 = plt.subplot2grid(shape=(3, 2), loc=(1, 0))
        ax4 = plt.subplot2grid((3, 2), (1, 1))
        ax5 = plt.subplot2grid((3, 2), (2, 0), colspan=2)
        plt.subplots_adjust(left=0.1, bottom=0.15, wspace=0.3, hspace=0.5)
        ax1.scatter(df['Lower Price'], df['Sold'])
        ax1.set_title('Items Sold Data (Lower Price)')
        ax1.set_xlabel('Price')
        ax1.set_ylabel('No. of Sales')
        ax2.scatter(df['Upper Price'], df['Sold'], color='orange')
        ax2.set_title('Items Sold Data (Upper Price)')
        ax2.set_xlabel('Price')
        ax2.set_ylabel('No. of Sales')
        ax3.scatter(df['Lower Price'], df['Watchers'])
        ax3.set_title('Watchers Data (Lower Price)')
        ax3.set_xlabel('Price')
        ax3.set_ylabel('No. of Watchers')
        ax4.scatter(df['Upper Price'], df['Watchers'], color='orange')
        ax4.set_title('Watchers Data (Upper Price)')
        ax4.set_xlabel('Price')
        ax4.set_ylabel('No. of Watchers')
        ax5.bar(df_frequency['Word'], df_frequency['Frequency'])
        ax5.set_title('Word Frequency Data')
        ax5.set_xlabel('Word')
        ax5.set_ylabel('Frequency')
        plt.show()


def main():
    page = input('Please enter the product you would like to search: ')
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=' + page.replace(' ', '%20')
    names, prices, watchers = scraper(url)
    a = 0
    for i in range(len(names)):
        a += 1
        item_name = names[i]
        item_price = prices[i]
        item_watchers = watchers[i]
        print(f'''
        {a}. Name: {item_name}
            Price: {item_price}
            Watchers or sold: {item_watchers}
        ''')
    data_table = data_cleaning(names, prices, watchers)
    summary = input('Would you like a summary of the data?(Y/N) ')
    if summary.lower() == 'y':
        print(data_summary(data_table))
    else:
        sys.exit('Thank you for using the program.')
    visualize = input('Would you like a visualization of the data?(Y/N) ')
    if visualize.lower() == 'y':
        frequency_dataframe = name_frequency(data_table)
        data_visualization(data_table, frequency_dataframe)
    else:
        sys.exit('Thank you for using the program.')


if __name__ == '__main__':
    main()
