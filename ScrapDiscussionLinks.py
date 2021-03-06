import requests
from bs4 import BeautifulSoup
import json
import os


# FUNCTION THAT RETURN DATASET WHICH HAS MOST PROBABILITY TO CONTAIN DEMANDED DISEASE
def datasetFinder(disease):

    # GETTING GROUP FROM THE DISEASE NAME
    group = disease[:1]

    # CREATING PATH TO FILE WHICH CONTAIN USER DEMANDED DISEASE DATA
    disease_dir = 'group_' + group + '/group_' + group + '_diseases_dataset.json'

    # IF THE DIRECTORY OF DEMANDED DISEASE DOESN'T EXIST
    if not os.path.exists(disease_dir):

        # ERROR MESSAGE TO SHOW IF DIRECTORY DOESN'T EXIST
        print("")
        print("Nothing found in our record.\n")
        print('To country this error run this file first. "Scrap.py"')
        print("")

    # IF DEMANDED DISEASE DIRECTORY EXISTS LOAD THE DATASET
    else:

        # LOADING ALL DISEASE DATASET TO FIND DEMANDED DISEASE
        with open(disease_dir, 'r') as f:
            diseases_dataset = json.load(f)

    # RETURNING THE DATASET WHICH CONTAIN THE DISEASE
    return diseases_dataset


# FUNCTION TO RETURN RETURN DATA RELATED TO THE DEMANDED DISEASE
def demandedDiseaseFinder(disease, diseases_dataset):

    # AN EMPTY DICTIONARY TO HOLD THE DATA IF FOUND
    disease_demanded = {}

    # ITERATING THROUGH DATASET TO FIND DEMANDED DISEASE
    for i in diseases_dataset:

        # IF DISEASE USER SEARCHING FOR IS FOUND
        if i['title'].lower() == disease:

            disease_demanded["id"] = i["id"]
            disease_demanded["title"] = i["title"]
            disease_demanded["link"] = i["link"]
            disease_demanded["pages"] = i["pages"]
            break

        # ELSE DISEASE USER SEARCHING FOR ISN'T FOUND THROUGH ERROR
        else:
            pass

    # SHOWING MESSAGE TO USER IF WE FOUND NOTHING
    if not bool(disease_demanded):
        print("")
        print("We found nothing related to you search. [" + disease.title() + "].\n")

    # RETURNING DISEASE DATA IF FOUND
    else:
        return disease_demanded


# FUNCTION THAT FETCH DISCUSSION LINKS OF DEMANDED DISEASE
def scrapdiscussionDisease(disease):

    # CREATING A LIST TO HOLD ALL FETCHED DATA
    discussionHolder = []

    # GETTING COUNT OF DISCUSSION PAGES AND CONVERTING IT TO AN INTEGER
    page_count = int(disease["pages"])

    # GETTING MAIN URL OF DISCUSSION PAGE OF THE DEMANDED DISEASE
    discussion_url = disease["link"]

    # CHECKING IF WE HAVE MULTIPLE DISCUSSION PAGES OR NOT
    if page_count == 1:

        # GRABBING PAGE CONTENT OF DISEASE DISCUSSIONS FROM URL OF DEMANDED DISEASE
        plainContent = requests.get(discussion_url)

        # CONVERTING PLAIN CONTENT TO HTML CONTENT
        htmlContent = plainContent.content

        # PARSING HTML CONTENT INTO SOUP
        soup = BeautifulSoup(htmlContent, 'html.parser')

        # GETTING ELEMENT THAT CONTAINS DISCUSSION INFO OF DEMANDED DISEASE
        get_discussion_link = soup.find_all('a', attrs={"rel": "discussion"})

        # COUNTER INCREMENT
        i = 0

        # LOOPING THOUGH ALL ELEMENTS THAT CONTAIN DISCUSSION OF DEMANDED DISEASE
        for link in get_discussion_link:

            # BASE URL OF MAIN SITE
            base_url = "https://patient.info"

            # GETTING LINK WE WANT AND IGNORE ALL OTHER LINKS
            link_class, link_title = link.get("class"), link.get("title")

            # IGNORE LINK IF NOT THE WANTED ONE
            if link_class and link_title == "View replies":
                pass

            # ADD LINK TO THE DISCUSSION HOLDER IF IT'S THE WANTED ONE
            else:

                # INCREMENTING COUNTER
                i += 1

                # SETTING EXTRACTED DATA IN THE DICTIONARY
                data = {
                    "discussion_id": i,
                    "discussion_title": link.text,
                    "discussion_link": base_url + link.get("href")
                }

                # APPENDING DICTIONARY TO LIST OF DISCUSSIONS
                discussionHolder.append(data)

    # IF DISCUSSION PAGE HAVE MULTIPLE PAGES JUST LOOP THROUGH IT
    else:

        # EXTRACTING FIRST PART OF URL
        url_start = discussion_url.split("=", 1)
        url_start = url_start[0]

        # EXTRACTING SECOND PART OF URL
        url_end = discussion_url.split("#", -1)
        url_end = url_end[1]

        # LOOPING THROUGH EACH PAGE TO GRAB DISCUSSION LINKS
        for page in range(page_count):

            # REGENERATING THE DISCUSSION PAGE URL SO WE CAN EASILY ITERATE THROUGH EACH PAGE USING LOOP
            url = url_start + "=" + str(page) + "#" + url_end

            # GRABBING PAGE CONTENT OF DISEASE DISCUSSIONS FROM URL OF DEMANDED DISEASE
            plainContent = requests.get(url)

            # CONVERTING PLAIN CONTENT TO HTML CONTENT
            htmlContent = plainContent.content

            # PARSING HTML CONTENT INTO SOUP
            soup = BeautifulSoup(htmlContent, 'html.parser')

            # GETTING ELEMENTS THAT CONTAINS DISCUSSION INFO OF DEMANDED DISEASE
            get_discussion_link = soup.find_all('a', attrs={"rel": "discussion"})

            # COUNTER INCREMENT
            i = 0

            # LOOPING THOUGH ALL ELEMENTS THAT CONTAIN DISCUSSION OF DEMANDED DISEASE
            for link in get_discussion_link:

                # BASE URL OF MAIN SITE
                base_url = "https://patient.info"

                # GETTING LINK WE WANT AND IGNORE ALL OTHER LINKS
                link_class, link_title = link.get("class"), link.get("title")

                # IGNORE LINK IF NOT THE WANTED ONE
                if link_class and link_title == "View replies":
                    pass

                # ADD LINK TO THE DISCUSSION HOLDER IF IT'S THE WANTED ONE
                else:

                    # INCREMENTING COUNTER
                    i += 1

                    # SETTING EXTRACTED DATA IN THE DICTIONARY
                    data = {
                        "discussion_id": i,
                        "discussion_title": link.text,
                        "discussion_link": base_url + link.get("href")
                    }

                    # APPENDING DICTIONARY TO LIST OF DISCUSSIONS
                    discussionHolder.append(data)

    # MAKE DIRECTORY OF EACH GROUP IF DOES'NT EXIST
    disease_group = 'group_' + disease["title"][:1]

    # CREATING PATH WHERE TO SAVE DATASET
    file_path = disease_group + '/' + disease["title"] + '_dataset.json'

    # WRITING JSON FILE OF EACH GROUP TO THE RESPECTIVE DIRECTORY
    with open(file_path, 'w') as f:
        json_formatted_str = json.dumps(discussionHolder, indent=4)
        f.write(json_formatted_str)

    print("")
    print("Task Completed Successfully!")
    print("For results please navigate to this directory. [/" + file_path + "]")


# ASKING USER ABOUT THE DISEASE TO SEARCH
disease = input("Enter disease you want to explore : ")

# FINDING DATASET THAT CONTAIN THE DEMANDED DISEASE
diseases_dataset = datasetFinder(disease.lower())

# START SEARCHING DEMANDED DISEASE AND RETURN DATA AFTER SUCCESS
disease_found = demandedDiseaseFinder(disease.lower(), diseases_dataset)

# FETCHING DISCUSSION OF THE DEMANDED DISEASE
scrapdiscussionDisease(disease_found)