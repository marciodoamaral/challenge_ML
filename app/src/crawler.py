from bs4 import BeautifulSoup
import requests
import re


# function to return the links inside URL
def search_links(id_base_set, url, depth, list_url):
    parent_url = url

    # if reach the last level
    if depth < 0:
        return None
    else:
        try:
            # make a request to specific site
            request_page = requests.get(url)

            if request_page.status_code == 200:

                # convert the request to text and parse it
                soup = BeautifulSoup(request_page.text, "html.parser")

                # make a loop to get all links in the URL
                for obj in soup.find_all("a", attrs={'href': re.compile("^(http|https)")}):
                    dict_href = {}
                    href_address = str(obj.attrs['href']).replace("<", "")

                    if href_address not in list_url:
                        dict_href = {"id_base_set": id_base_set, "parent_url": parent_url, "url": href_address, "level": depth}
                        list_url.append(dict_href)
                        # calling it self
                        search_links(id_base_set, href_address, depth - 1, list_url)
        except:
            pass

    return list_url
