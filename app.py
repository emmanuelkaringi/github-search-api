import requests

def create_query(languages, min_stars=50000):
    query = f"stars:>{min_stars} "
    for language in languages:
        query += f"language:{language} "
    return query

def repos(languages, sort="stars", order ="desc"):
    get_repo = "https://api.github.com/search/repositories"
    query = create_query(languages)

    parameters = {"q": query, "sort": sort, "order": order}

    response = requests.get(get_repo, params=parameters)
    status_code = response.status_code

    if status_code == 403:
        raise RuntimeError("Rate limit reached. Wait a minute and try again.")
    if status_code != 200:
        raise RuntimeError(f"An error occured. HTTP Status Code was: {status_code}. ")
    else:
        response_json = response.json()
        records = response_json["items"]
        return records

if __name__ == "__main__":
    languages = ["python"]
    results = repos(languages)

    for result in results:
        language = result["language"]
        stars=result["stargazers_count"]
        name = result["name"]

        print(f"-> {name} is a {language} repo with {stars} stars.")