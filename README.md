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


