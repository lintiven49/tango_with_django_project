import requests
from requests.auth import HTTPBasicAuth
from requests.utils import quote


def run_query(search_items):
    root_url = "https://api.datamarket.azure.com/Bing/Search/v1/"
    source = "Web"

    result_per_page = 10
    offset = 0

    query = "'{}'".format(search_items)
    query = quote(query)
    print query
    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url,
        source,
        result_per_page,
        offset,
        query
    )

    bing_api_key = 'JpinGg9SptwQqelPoe116HeKeBUQy6t94D8c7Rxx8ng'
    auth = HTTPBasicAuth('', bing_api_key)
    results = []
    try:
        r = requests.get(search_url, auth=auth)
    except requests.HTTPError, e:
        print 'error occured', e
    else:
        json_response = r.json()
        for result in json_response['d']['results']:
            results.append({
                'title': result['Title'],
                'link': result['Url'],
                'summary': result['Description']})
    return results


if __name__ == '__main__':
    print run_query("test")

