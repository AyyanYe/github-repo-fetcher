import requests

username = "AyyanYe"
url = f"https://api.github.com/users/{username}/repos?per_page=100"

response = requests.get(url)
if response.status_code == 200:
    repos = response.json()
    for repo in repos:
        print(f"Repository Name: {repo['name']}")
        print(f"Description: {repo['description']}")
        print(f"URL: {repo['html_url']}\n")
else:
    print(f"Failed to fetch repositories: {response.status_code}")