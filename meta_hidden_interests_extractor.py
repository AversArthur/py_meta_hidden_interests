import requests
import os


META_API_KEY = os.environ.get('META_API_KEY')

if not META_API_KEY:
    raise ValueError("No META_API_KEY environment variable set")


def get_hidden_interests(search_key: str) -> list[dict] | str:
    result = []
    url = f'https://graph.facebook.com/search?type=adinterest&q=[{search_key}]&limit=10000&locale=en_US&access_token={META_API_KEY}'

    try:
        response = requests.get(url).json()['data']

        for item in response:
            result.append({
                'id': item['id'],
                'name': item['name'],
                'audience': item.get('audience_size_upper_bound', 'N/A'),
                'path': item.get('path', 'N/A'),
                'topic': item.get('topic', 'N/A'),
            })
        return result
    except Exception as e:
        return 'Error: ' + str(e)


if __name__ == '__main__':
    search_key = input('Enter search key: ')
    result = get_hidden_interests(search_key)
    print(result)
