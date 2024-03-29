import os
import json
import requests
import pandas as pd


def get_all_data_and_group_by_year(endpoint, directory):
    data_by_year = {}
    page = 1
    while True:
        response = requests.get(endpoint, params={'page': page})
        if response.status_code == 200:
            data = response.json()
            for result in data['results']:
                created_year = result['created'][:4]
                if created_year not in data_by_year:
                    data_by_year[created_year] = []
                data_by_year[created_year].append(result)
            if data['next']:
                page += 1
            else:
                break
        else:
            print(f"Failed to retrieve data from {endpoint}")
            return

    for year, results in data_by_year.items():
        filename = f"{directory}/{year}/{endpoint.split('/')[-2]}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)


endpoints = {
    'people': 'https://swapi.dev/api/people/',
    'films': 'https://swapi.dev/api/films/',
    'vehicles': 'https://swapi.dev/api/vehicles/'
}


for endpoint, url in endpoints.items():
    get_all_data_and_group_by_year(url, endpoint)




people_data = pd.read_json('people/2014/people.json')


num_records = len(people_data)

print(f"O número total de registros do endpoint 'people' é: {num_records}")


people_data = pd.read_json('people/2014/people.json')
films_data = pd.read_json('films/2014/films.json')


def extract_films_titles(films_urls):
    films_titles = []
    for film_url in films_urls:
        film_id = film_url.split('/')[-2]
        film_title = films_data[films_data['url'].str.contains(film_id)]['title'].iloc[0]
        films_titles.append(film_title)
    return films_titles


people_films = []
for index, person in people_data.iterrows():
    films_titles = extract_films_titles(person['films'])
    people_films.append({
        'name': person['name'],
        'gender': person['gender'],
        'films': films_titles
    })


with open('people_with_films.json', 'w') as outfile:
    json.dump(people_films, outfile, indent=4)

print("Transformação concluída. Arquivo 'people_with_films.json' salvo com sucesso.")
