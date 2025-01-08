def structure_html(output: list[str]) ->list[dict[str, str|int]]: 
    title: str| None = None
    heading: str | None  = None
    sub_heading: str | None = None
    text: list[str] = []
    table_on: bool = False
    table_content: list[str]
    df_json : list[dict[str, str]] = []

    for idx, html_page in enumerate(output):
        paragraph_count: int = 0
        for html_tag in html_page.split("\n"):
            
            if html_tag.startswith('```'): continue
            elif html_tag.startswith("<table"):

                table_on = True
                table_content = []
                continue

            elif table_on and html_tag.startswith("</table>"):
                table_on = False
                table_content = "\n".join(table_content)
                text = ['table', heading, sub_heading, table_content]

            elif table_on:
                table_content.append(html_tag)
                continue

            elif ( html_tag.startswith('<title>') and
                html_tag.split(">")[1].split("<")[0] != title) :

                title = html_tag.split(">")[1].split("<")[0]
                continue

            elif ( html_tag.startswith("<h1>") and
                html_tag.split(">")[1].split("<")[0] != heading):

                heading = html_tag.split(">")[1].split("<")[0]
                continue

            elif (html_tag.startswith("<h2>") and
                html_tag.split(">")[1].split("<")[0] != sub_heading):

                sub_heading = html_tag.split(">")[1].split("<")[0]
                continue

            elif html_tag.startswith("<p>") :
                text = ['text', heading, sub_heading, html_tag.split(">")[1].split("<")[0]]
                paragraph_count += 1

            elif html_tag.startswith("<diagram>"):
                text = ['diagram', heading, sub_heading, html_tag.split(">")[1].split("<")[0]]
                paragraph_count += 1

            elif html_tag.startswith("<chart>"):
                text = ['chart', heading, sub_heading, html_tag.split(">")[1].split("<")[0]]
                paragraph_count += 1
            else:
                continue
            
            if text[3] != '': 

                df_json.append({
                    "heading_identifier": title,
                    "heading_text": text[1],
                    "sub_heading_text": text[2],
                    "text_type": text[0],
                    "paragraph_number": paragraph_count,
                    "text": text[3],
                    "index": idx, 
                })

    return df_json