### Netskope nonsense...
import truststore
truststore.inject_into_ssl()
########################

from dotenv import load_dotenv
import os
from atlassian.confluence import Confluence

load_dotenv()
print('connecting to Confluence...')

section_id = 56819899
page_id = 1911816634

confluence = Confluence(
    url=os.getenv("CONFLUENCE_URL"),
    username=os.getenv("ATLASSIAN_USER"),
    password=os.getenv("ATLASSIAN_API_KEY")
)

section = confluence.get_page_by_id(page_id=section_id, expand="body.storage")
print("section_id: ", section['title'])

page = confluence.get_page_by_id(page_id=page_id, expand="body.storage")
print("page_id: ", page['title'])
## print contents of the page
print("########### Section Contents ###########")
print("section content: ", section['body']['storage']['value'])
print("########### Page Contents ###########")
print("page content: ", page['body']['storage']['value'])