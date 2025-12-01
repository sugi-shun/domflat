import json
import re
from typing import Any, Dict

import pandas as pd
from bs4 import BeautifulSoup, Tag


def build_dom_from_csv(csv_filepath: str) -> str:
    try:
        df = pd.read_csv(csv_filepath).sort_values(by='id').reset_index(drop=True)
    except FileNotFoundError:
        return "Error: CSV file not found."
    except KeyError:
        return "Error: CSV must contain 'id', 'xpath', 'attributes', and 'contents' columns."

    data_map: Dict[int, Dict[str, Any]] = df.set_index('id').to_dict('index')
    element_map: Dict[int, Tag] = {}
    for row_id, row_data in data_map.items():
        xpath_parts = row_data['xpath'].split('/')
        tag_name_with_index = xpath_parts[-1]
        tag_name = re.sub(r'\[\d+\]', '', tag_name_with_index)
        attributes = json.loads(row_data['attributes'])
        new_element = BeautifulSoup('', 'html.parser').new_tag(tag_name)
        new_element.attrs = attributes
        element_map[row_id] = new_element

    for row_id, row_data in data_map.items():
        current_element = element_map[row_id]
        contents_str = str(row_data['contents'])

        if contents_str != 'None' and contents_str != 'nan':
            contents_str = contents_str.replace(r'\{', '#ESCAPED_LBRACE#').replace(r'\}', '#ESCAPED_RBRACE#')
            parts = re.split(r'(\{id\d+\})', contents_str)

            for part in parts:
                if part.startswith('{id') and part.endswith('}'):
                    try:
                        child_id = int(part[3:-1])
                        child_element = element_map.get(child_id)
                        if child_element:
                            current_element.append(child_element)
                        else:
                            current_element.append(f"[ID_REF_ERROR: {child_id}]")
                    except ValueError:
                        current_element.append(part)
                else:
                    text_content = part.replace('#ESCAPED_LBRACE#', '{').replace('#ESCAPED_RBRACE#', '}')
                    current_element.append(text_content)

    if 0 in element_map:
        return element_map[0].prettify()
    else:
        return "Error: Root element (id 0) not found."


if __name__ == '__main__':
    import sys
    csv_file = sys.argv[1]
    html = build_dom_from_csv(csv_file)
    with open(sys.argv[2], "w") as f:
        f.write(html)
