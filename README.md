# eBay Web Scraper
  #### Video Demo: https://youtu.be/z-OXfXtVL7Y
## Purpose
Collects product data from eBay product listings page which can then be used for data analysis. Users can use this program to do research on a specific product on eBay.

## Libraries
**Beautiful Soup:** used to collect data from a webpage based on its HTML element.

**requests:** gets the HTML of a webpage from a given link.

**Pandas:** re-formats dataset into a table or dataframe to make it easier to conduct data analysis.

**matplotlib:** takes in a dataset or dataframe and displays charts or graphs.

The libraries can be installed by running
```bash
pip install -r requirements.txt
```

## How to use
First, you would be prompted to input the name of the product you are searching for

![Project Screenshot](https://github.com/Vincent-Ang523/CS50P-Final-Project/assets/99592424/9a65dc7a-677b-4107-ac73-b8e77ebd0c5d)

You can then hit enter once typing the product name and it will show all the products on eBay's first page of the product listings page. They will be in this format

![Project Screenshot1](https://github.com/Vincent-Ang523/CS50P-Final-Project/assets/99592424/35a12640-5d9a-4a2b-82bb-a5b883b5d501)

> [!NOTE]  
> Some of the prices will be given in a range format (e.g. $7.5 to $10.0)

Then, at the bottom, you would be asked if you would like a summary of the data

![Project Screenshot2](https://github.com/Vincent-Ang523/CS50P-Final-Project/assets/99592424/892768d1-e3ce-42ca-bca5-665fce17f815)

If you typed n/N, the program would exit with a message

![Project Screenshot3](https://github.com/Vincent-Ang523/CS50P-Final-Project/assets/99592424/e02f77f3-09ab-4241-9ba3-18f6453233f1)

If you typed y/Y, a summary of the data will be shown with the format

![Project Screenshot4](https://github.com/Vincent-Ang523/CS50P-Final-Project/assets/99592424/245495e4-40b3-48c5-b460-89fbe5703eea)

At the bottom, you would be asked if you would like a visualization of the data

![Project Screenshot5](https://github.com/Vincent-Ang523/CS50P-Final-Project/assets/99592424/52858781-7a8b-431c-b6f9-839452ea73b5)

This works similarly to the data summary prompt.

If you typed y/Y, the program would display a series of graphs in this format

![Project Screenshot6](https://github.com/Vincent-Ang523/CS50P-Final-Project/assets/99592424/fdb29725-36ab-41cf-85dc-60214616fe88)

The first two graphs on the top are scatter plots that compare the sales number on the y-axis to the price on the x-axis

The two graphs below are also scatter plots but instead, they compare the watchers number on the y-axis to the price on the x-axis

> [!NOTE]  
> Because some of the prices are given in price ranges, there are two graphs for each dataset, one with the lower price and one with the upper price.

The graph on the bottom is a bar graph that ranks the five most frequently used words in the product listings' title

> [!NOTE]  
> The graph excludes the search keyterms (e.g. if "toilet paper" is the search term, then "toilet" and "paper" will be excluded)
>
> However, this is done case-sensitively (i.e. in the above example, "Toilet" and "Paper" would **not** be excluded)

Users can use the graph to extrapolate some information. For example, the scatter plots can be used to determine the price ranges that have the most sales or watchers.

The bar graph can also be used to determine which words are most often used in the product's title.

## Functions
Excluding the main() function, there are 5 functions

### scraper(link)
This function takes the URL of the product's listings page and uses the BeautifulSoup library to extract data regarding each listing's title, price, and number of watchers or sales.

The function would then return a set of lists containing the names, prices, and watchers data of all of the listings.

> [!NOTE]  
> The function only takes data from the product listings page instead of each product's own page.
>
> I initially wanted to take data from each product's page as it provided more accurate data regarding the number of watchers or sales. However, when I wrote my code to do this, the program became much slower, taking over a few minutes to fetch all the data. So, I decided against doing this.


### data_cleaning(names, prices, watchers)
This function takes three lists, names, prices, and watchers, and re-formats the data into a table or dataframe using the Pandas library.

First, the function would re-format each element in the watchers list by removing the commas and the "watchers" or "sold" suffix so it can be parsed as a float.
```python
remove_commas = watchers[i].replace(',', '')
match_watchers = re.match(r'(\d+)(\+)? (sold|watchers)', remove_commas)
formatted_watchers = match_watchers.group(1)
```
The function would also re-format each element in the prices list by removing the currency prefix
```python
formatted_prices.append(re.sub(r'[^0-9 to.]', '', prices[i]))
```
The function would then split the prices list into an "upper_price" and "lower_price" list by using a .split function with ' to ' as a separator.
```python
if 'to' in prices[i]:
  lower_price.append(formatted_prices[i].split(' to ')[0])
  upper_price.append(formatted_prices[i].split(' to ')[1])
else:
  lower_price.append(formatted_prices[i])
  upper_price.append(formatted_prices[i])
```
The watchers list would also be split into two lists names "watchers_number" and "sold_number".
```python
if not 'watchers' in watchers[i]:
  watchers_number.append('0')
else:
  watchers_number.append(formatted_watchers)
if not 'sold' in watchers[i]:
  sold_number.append('0')
else:
  sold_number.append(formatted_watchers)
```
The function would then return a dataframe in this format
```python
df = pd.DataFrame(
        {'Name': names, 'Lower Price': lower_price, 'Upper Price': upper_price, 'Watchers': watchers_number,
         'Sold': sold_number})
```

### data_summary(df)
This function takes the dataframe "df" and prints a summary of the data by calculating mean, median, standard deviation, and the number of zeros in the "sold" and "watchers" column.

The function would return a string in the format shown

![Project Screenshot4](https://github.com/Vincent-Ang523/CS50P-Final-Project/assets/99592424/2b8945ad-36fd-497f-807f-b5064ab2535d)

### name_frequency(df):
This function would return a new dataframe that stores the 5 most used words in the product listings' titles. The dataframe would store the words themselves and the frequency of each word. 
```python
# removes punctuation from Name column
df['Name'] = df['Name'].apply(lambda x: re.sub(r'[^\w\s]', '', x))
# finds top 5 most frequent words in product name except search keywords itself
frequency_count = Series(' '.join(df.Name).split()).value_counts()[2:7]
df_frequency = pd.DataFrame({'Word': frequency_count.index, 'Frequency': frequency_count.values})
return df_frequency
```
### data_visualization(df, df_frequency):
This function takes two dataframes as input. The first is the dataframe returned by the data_cleaning function, "df". The second is "df_frequency" returned by the name_frequency function. It would then use the matplotlib library to output a subplot which contains a set of scatter plots and a bar graph. The format of this subplot is shown in the aforementioned "how to use section".
