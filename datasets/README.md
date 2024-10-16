# Datasets

Datasets of 8 categories are available. These are chosen to demonstrate the generalizability of the system. 

## Dataset Specification

Here are the datasets used and the sizes of each dataset after processing. Datasets are formatted and customized as required and some are improved with external knowledge.

| Category | Base Dataset                                                                          | Size   | Processing                                                                                                               |
|----------|---------------------------------------------------------------------------------------|--------|--------------------------------------------------------------------------------------------------------------------------|
| Book     | [Amazon books](https://www.kaggle.com/datasets/ashwinshetgaonkar/amazonbooks)         | 1029   | Add book descriptions with [Google Book API](https://developers.google.com/books).                                       | 
| Game     | [Steam Video Games](https://www.kaggle.com/datasets/tamber/steam-video-games)         | 200000 | Formatted to have user-wise data in played and downloaded format.                                                        |
| House    | [kc_house_data](https://www.kaggle.com/datasets/shivachandel/kc-house-data)           | 21613  | -                                                                                                                        |
| Laptop   | Custom ([gathered](https://noteb.com/?public/api.php))                                | 630    | Processed to contain the necessary details in a structured way.                                                          |
| Movie    | [MovieLens](https://grouplens.org/datasets/movielens/)                                | 6705   | Names were taken from the dataset and created the dataset by gathering dataset from [OMDB API](http://www.omdbapi.com/). |
| News     | [News Category Dataset](https://www.kaggle.com/datasets/rmisra/news-category-dataset) | 210294 | -                                                                                                                        |
| Music    | [Spotify dataset](https://www.kaggle.com/datasets/vatsalmavani/spotify-dataset)       | 170653 | -                                                                                                                        |
| Vehicle  | Custom ([scraped](https://www.usedcars.com/))                                         | 2488   | Data is formatted and structured as required.                                                                            |

***

Find datasets [here](https://drive.google.com/drive/folders/1S9R76Hog0sK6cqWlwWIFauwS587-ianM?usp=sharing).
