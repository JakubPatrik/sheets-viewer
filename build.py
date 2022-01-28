import csv
import sys
import os
import subprocess

MAP_CLASSES = {
    0: "id",
    1: "company",
    2: "address",
    3: "ico",
    4: "icpdh",
    5: "do-issue",
    6: "do-supply",
    7: "item",
    8: "amount",
}


def build(csv_path: str) -> None:
    """
    Build a static html page(.html) in the sub-directories of the given path to 
    :param path: path for the csv document to be rendered as the main element table
    """
    # Read the csv file
    reader = None
    with open(csv_path, "r") as f:
        reader = csv.reader(f.readlines())

    # Copy the template into the new file
    year: str = csv_path.split('/')[-1].split('.')[0]
    web_path: str = f"public/{year}.html"

    # Clear the template
    subprocess.run(
        f"touch {web_path} && cp public/template.html {web_path}", shell=True)

    # Read the html template
    html_string: str = ''
    with open(web_path) as web:
        html_string = ''.join(web.readlines())

    html_string = fill_template(
        title=year, template=html_string,  reader=reader)

    # The HTML is populated with the latest data
    # Congratulations
    with open(web_path, "w") as web:
        web.write(html_string)


def fill_template(title: str, template: str, reader) -> str:
    # Set the title
    htmls: str = template.replace("$title$", title)

    # Append the active class to the current year webpage
    a_tag = f"<a class=\"nav\" href=\"./{title}.html\">"
    year_idx: int = htmls.index(a_tag) + 10
    htmls = htmls[:year_idx] + "active " + htmls[year_idx:]

    start_idx: int = htmls.index("<table>") + 7
    end_idx: int = htmls.index("</table>")
    table: str = '\n'

    for i, row in enumerate(reader):
        # ignore rows with no data
        if len(''.join(row)) == 0:
            continue

        # Build table header for the first row, otherwise table row
        tag: str = "th" if i == 0 else "td"
        table += f'\t\t\t<tr>\n'

        for j, data in enumerate(row):
            # wrap the invoice number to link to the actual invoice pdf
            content: str = data
            if i > 0 and j == 0:
                invoice_num: str = row[j]
                purchaser: str = row[j + 1]
                invoice_path = _get_invoice(num=invoice_num, company=purchaser)
                content = f'<a href="{invoice_path}" target="_blank">{data}</a>'

            class_id: str = MAP_CLASSES[j]
            table += f'\t\t\t\t<{tag} class="{class_id}">{content}</{tag}>\n'

        table += f'\t\t\t</tr>\n'

    return htmls[:start_idx] + table + '\t\t' + htmls[end_idx:]


def _get_invoice(num, company) -> str:
    if "Emobia" in company:
        return f"C:/Users/Jakub Patrik/Desktop/Emobia/Invoices/Faktura_{num}.pdf"
    if "SVK media" in company:
        return f"C:/Users/Jakub Patrik/Desktop/SVKMedia/Invoices/Faktura_{num}.pdf"
    if "heartfish" in company:
        return f"C:/Users/Jakub Patrik/Desktop/Heartfish/Invoices/Invoice_{num}_en.pdf"
    if "mEleven" in company:
        return f"C:/Users/Jakub Patrik/Desktop/mEleven/Invoices/Faktura_{num}.pdf"
    return '/'


# Expect the cli argument of the path to the csv file
# to generate the web content for
if __name__ == "__main__":
    file = sys.argv[1]
    if os.path.exists(file) and file.endswith('.csv'):
        build(csv_path=file)
    else:
        raise FileNotFoundError("must be a valid csv file of invoices")
