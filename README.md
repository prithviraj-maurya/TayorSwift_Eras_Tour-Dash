# The Eras Tour: Visualizing the Impact of Taylor Swift's Live Shows

### Motivation:

Taylor Swift’s “Eras Tour” has had an incredibly impactful summer, with the Federal Reserve estimating a nearly $5 billion dollar boost to the economy. We chose to investigate this phenomenon in order to explore the following objectives:

- Global Reach: Visualizing the expansive network of shows across the world and understanding the impact on the community.
- Encoding the magic of live shows: Understanding how Taylor Swift's music captivates live audiences by using Spotify’s audio features (eg: danceability, loudness, tempo) to visualize the changes over the duration of a show.
- Data-driven lessons: Learn how data can inform music, engagement, and performance by correlating track popularity with live occurrences.


### Data Sources

We will construct our own datasets using a combination of two free APIs:
1. Setlist.fm API: Data on setlist and location of a particular artist’s show
This data source will provide us with the necessary information regarding where her shows took place and what songs she played at each show.
2. Spotify API: Data on artist or song such as popularity, genre, audio features
Using the above data, we can map each performed song to their associated metrics on Spotify such as the ones shown on the right.
3. Kaggle: Taylor Concert Tour its impact on attendance and economy, Taylor Swift Era Tour Dataset

Visualization Type: Maps, Bar Charts, Radar plot
Tech Stack: D3.js, Plotly, Pandas
Data Source: Taylor Swift Eras Tour Data, 900+ Fans Surveyed about ticket prices
Observable notebook: https://observablehq.com/@prithviraj/taylor-swift-the-eras-tour 

Introduction
The Global Reach project delves into the dynamic landscape of Taylor Swift's Eras Tour, employing advanced data visualization techniques to bring to life the extensive network of shows worldwide. Leveraging technologies like D3.js, Plotly, and Pandas, the project extracts insights from the tour data, exploring not only the geographical expanse but also understanding its economic implications.

Data Collection
The data for the project was meticulously collected by scraping a blog post detailing the countries, cities, stadiums, dates, and the number of shows for Taylor Swift's Eras Tour in 2024. This information was compiled into a structured CSV file, serving as the foundation for developing insightful visualizations.


Visualization 1: Categorized Map of Touring Countries
The first visualization presents a comprehensive map of all countries included in the Eras Tour. Utilizing Plotly's geo capabilities, the coordinates of countries were projected onto the map. The equirectangular projection was employed for its ability to preserve relative sizes, ensuring an accurate depiction of the geographical distribution.

![tour_countries.png](tour_countries.png)

Visualization 2: Animated Tour Arcs on a Globe
The second visualization introduces an animated map, showcasing arcs that connect countries based on the chronological order of tour dates. Drawing inspiration from the D3 documentation, a canvas-based globe was constructed, dynamically moving to represent the changing coordinates of countries over time. We started by an empty globe on canvas then showing the country boundaries, then by putting arcs from one country to another. Coloring the current country and then adding the animation effect by rotating the globe.

![tour_countries_animated.gif](tour_countries_animated.gif)

### A Glimpse of the Dashboard
![dashboard_snapshot.gif](dashboard_snapshot.gif)
   

### References:

1. [CBS News - Eras Tour Boosting Economy](https://www.cbsnews.com/news/taylor-swift-eras-tour-boosted-economy-tourism-federal-reserve-how-much-money-made/)
2. [Tableau Dashboard - Spotify Top Tracks](https://www.tableau.com/community/music/spotify-top-tracks)
3. [Tableau Dashboard - The Cure Band analysis](https://www.tableau.com/community/music/the-cure)
4. [Tableau Dashboard - Heavy Metal Band analysis](https://www.tableau.com/community/music/heavy-metal)
5. [Setlist API Documentation](https://api.setlist.fm/docs/1.0/ui/index.html)
6. [Spotify API Documentation](https://developer.spotify.com/documentation/web-api)
7. [Kaggle Dataset - Taylor Concert Tour Impact on Attendance](https://www.kaggle.com/datasets/gayu14/taylor-concert-tours-impact-on-attendance-and/data)
8. [What are the Eras](https://www.lsureveille.com/entertainment/what-are-the-eras-on-taylor-swifts-the-eras-tour/article_1ac1587a-cdc6-11ed-8c34-0fdc3d371c29.html)
9. [Eras Tour Money & Economy](https://time.com/6307420/taylor-swift-eras-tour-money-economy/)
