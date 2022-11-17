"""
Autorzy:
    Damian Kijańczuk s20154
    Szymon Ciemny    s21355

Przygotowanie środowiska:
    Oprócz języka Python, potrzebne takze będzie:
    - numpy
    - pandas
    - sklearn

Uruchomienie oraz instrukcja:
    5 polecanych
    'python3 main.py --name "Damian Kijańczuk" --file "ratings.json"'
    'python3 main.py --name "Szymon Ciemny" --file "ratings.json"'
    5 niepolecanych 
    'python3 main.py --name "Damian Kijańczuk" --file "ratings.json" --amount -5

"""

import argparse
import json
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Parser for handling argumnts
def build_arg_parser():
    parser = argparse.ArgumentParser(description='Compute similarity score')
    parser.add_argument('--name', dest='name', required=True,
            help='Name of the student/teacher')
    parser.add_argument("--file", dest="file", required=True,
            help='Name of file with data')
    parser.add_argument("--amount", dest="amount", default=5, type=int,
        help='Amount of recommendations you want.')
    parser.add_argument("--neighbours", dest="neighbours", default=3,
        help='Amount of neighbours for the algorythmm.')
    return parser
args = build_arg_parser().parse_args()


# Open file and prepare it for processing
# All cells without value get 0
with open(args.file, 'r') as f:
    data = json.loads(f.read())
df = pd.DataFrame.from_dict(data)
df = df.fillna(0)

# Calculate cosine similarity for all values
knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(df.values)
distances, indices = knn.kneighbors(
    df.values, n_neighbors=args.neighbours)

USER_INDEX = df.columns.tolist().index(args.name) # Index of args.name in dataframe
tmpDf = df.copy() # Temporary dataframe for calculations
# m - the row number of movie in df
# t - movie_title
for m, t in enumerate(df.index):
    # If movie doesn't have rating provided by USER
    if df.iloc[m, USER_INDEX] == 0:
        sim_movies = indices[m].tolist() # Similar movies
        movie_distances = distances[m].tolist() # Distance of movies in plot

        # If there are similar movies found
        if m in sim_movies:
            # Leave only distances from list ex. [3 8 5] -> [8 5]
            id_movie = sim_movies.index(m)
            sim_movies.remove(m)
            movie_distances.pop(id_movie)
        # If ther are no other rating of this movie
        else:
            sim_movies = sim_movies[:args.neighbours-1]
            movie_distances = movie_distances[:args.neighbours-1]

        # Calculate similarity 
        movie_similarity = [1-x for x in movie_distances]
        movie_similarity_copy = movie_similarity.copy()
        nominator = 0

        # For each similiar movie found
        for s in range(0, len(movie_similarity)):
            # If it doesnt have rating
            if df.iloc[sim_movies[s], USER_INDEX] == 0:
                # Ignore the rating and the similarity in calculating the predicted rating
                if len(movie_similarity_copy) == (args.neighbours - 1):
                    movie_similarity_copy.pop(s)
                # Calculate predicted rating
                else:
                    movie_similarity_copy.pop(
                        s-(len(movie_similarity)-len(movie_similarity_copy)))
            # Use the rating and similarity in the calculation
            else:
                nominator = nominator + movie_similarity[s]*df.iloc[sim_movies[s], USER_INDEX]

        # Are there any ratings?
        if len(movie_similarity_copy) > 0:
            # Are those ratings meaningfull?
            if sum(movie_similarity_copy) > 0:
                tmpDf.iloc[m, USER_INDEX] = nominator/sum(movie_similarity_copy)
            else:
                tmpDf.iloc[m, USER_INDEX] = 0
        else:
            tmpDf.iloc[m, USER_INDEX] = 0



# List movies watched by user
print('The list of the movies', args.name,'watched')
for i, movie in enumerate( df[df[args.name] > 0][args.name].index.tolist() ):
    print ("{:<3}| {:<40}".format(i+1,movie))

if args.amount > 0:
    # Prepare list of recomended movies
    recommended_movies = []
    for m in df[df[args.name] == 0].index.tolist():
        index_df = df.index.tolist().index(m)
        predicted_rating = tmpDf.iloc[index_df, tmpDf.columns.tolist().index(args.name)]
        recommended_movies.append((m, predicted_rating))
    recommended_movies = sorted(recommended_movies, key=lambda x: x[1], reverse=True)

    # Print recomendations
    print('The list of the Recommended Movies')
    for i, movie in enumerate(recommended_movies[:args.amount]):
        print ("{:<3}| {:<40} {:<4}".format(i+1,movie[0], movie[1]))

elif args.amount < 0:
    # Prepare list of NOT recomended movies
    recommended_movies = []
    for m in df[df[args.name] == 0].index.tolist():
        index_df = df.index.tolist().index(m)
        predicted_rating = tmpDf.iloc[index_df, tmpDf.columns.tolist().index(args.name)]
        recommended_movies.append((m, predicted_rating))
    recommended_movies = sorted(recommended_movies, key=lambda x: x[1], reverse=True)

    # Print recomendations
    print('The list of the NOT Recommended Movies')
    for i, movie in enumerate(recommended_movies[args.amount:]):
        print ("{:<3}| {:<40} {:<4}".format(-5+i,movie[0], movie[1]))




