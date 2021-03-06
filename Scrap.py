import requests
from bs4 import BeautifulSoup
import json
import os


# FUNCTION TO GRAB PAGE SOURCE OF THE POINTED URL
def fetchUrlContent(url_extension):

    # GRABBING CONTENT FROM URL
    plainContent = requests.get(base_url + url_extension)

    # CONVERTING PLAIN CONTENT TO HTML CONTENT
    htmlContent = plainContent.content

    # PARSING HTML CONTENT INTO SOUP
    soup = BeautifulSoup(htmlContent, 'html.parser')

    # RETURNING WHOLE CONTENT
    return soup


# FUNCTION TO FIND INFORMATION OF ELEMENTS OF EACH GROUP
def findElementsInfo(group):

    # URL EXTENSION TO NAVIGATE IN GROUPS
    route_to_group = "/forums/index-" + str(group)

    # CALLING FUNCTION TO GRAB PAGE CONTENT
    soup = fetchUrlContent(route_to_group)

    # GETTING LINKS OF GROUPS
    get_anchors_table = soup.find('table', class_='table')

    # COUNTER INCREMENT
    i = 0

    # GENERATING LIST OF ELEMENTS OF EACH GROUP
    anchorsList = []

    # LOOPING THROUGH ALL ANCHOR TAGS TO FETCH INFORMATION
    for anchor in get_anchors_table.find_all('a'):

        # COUNTER INCREMENT
        i += 1

        # GETTING LINKS OF EACH ELEMENT OF GROUP
        route_to_element = anchor.get("href")

        # NAVIGATING TO THE ABOVE FETCHED LINK TO GRAB PAGE COUNT INFORMATION (RE-CALLING fetchUrlContent FUNCTION)
        # BECAUSE THE PAGES INFORMATION IS IN NESTED PAGE
        soup = fetchUrlContent(route_to_element)

        # GETTING HTML ELEMENT THAT CONTAIN PAGES COUNT OF DISCUSSION PAGES
        get_pages_count = soup.find('select', attrs={"name": "page"})

        # IF WE GOT THE ELEMENT ABOVE JUST EXTRACT THE PAGE COUNT AND GRAB THE DISCUSSION LINK
        if get_pages_count:

            # EXTRACTING PAGE COUNT FROM HTML ELEMENT
            get_pages_count.find('option')
            page_count = get_pages_count.text
            page_count = page_count.rsplit('/')[-1]
            page_count = page_count.replace('\n', '')

            # GETTING ELEMENT THAT CONTAIN DISCUSSION LINK OF DEMANDED DISEASE
            link_to_discussion = soup.find('a', attrs={"class": "reply__control reply-ctrl-last link"})

            # EXTRACTING LINK FROM THE ABOVE ELEMENT AND SET IT INTO A VARIABLE
            link_to_discussion = link_to_discussion.get("href")

        # IF WE DIDN'T GOT THE ELEMENT ABOVE JUST SET THE PAGE COUNT AND DISCUSSION LINK MANUALLY
        else:

            # IF THERE IS NO PAGE COUNT THEN DEFINITELY THERE IS ONE PAGE
            page_count = "1"

            # EXTRACTING LINK FROM THE ABOVE ELEMENT AND SET IT INTO A VARIABLE
            link_to_discussion = base_url + route_to_element

        # CREATING DICTIONARY OF EACH GROUP ELEMENT SEPARATELY
        data = {
                 'id': i,
                 'title': anchor.text,
                 'link': link_to_discussion,
                 'pages': page_count
                }

        # APPENDING DICTIONARY TO LIST OF ELEMENTS
        anchorsList.append(data)

    # MAKE DIRECTORY OF EACH GROUP IF DOES'NT EXIST
    new_dir = 'group_' + group
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    # CREATING PATH WHERE TO SAVE DATASET
    file_path = new_dir + '/group_' + group + '_diseases_dataset.json'

    # WRITING JSON FILE OF EACH GROUP TO THE RESPECTIVE DIRECTORY
    with open(file_path, 'w') as f:
        json_formatted_str = json.dumps(anchorsList, indent=4)
        f.write(json_formatted_str)

    print("")
    print("Task Completed Successfully!")
    print("For results please navigate to this directory. [/" + file_path + "]")


# BASE URL OF MAIN SITE
base_url = "https://patient.info"

# ASKING USER WHERE TO BROWSE
group = input("Enter alphabet of group you want to search: ")

# START SCRAPING
findElementsInfo(group.lower())
