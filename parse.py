import argparse
import os
import re
import urllib.request

from bs4 import BeautifulSoup

LETTERS = "bcdefghijklmnopqrstuvwxyz"

NOTES_PATTERN = (
    "# {title}\n\n"
    "[Link to the paper]({url})\n\n"
    "**{authors}**\n\n"
    "*{source}*\n\n"
    "Year: **{year}**\n\n"
)

README_PATTERN = (
    "[[**Notes**]({filepath})] [[Paper]({url})]"
    " - {year} – **{title}** – {authors} – {source}"
)

README_START_COMMENT = "[comment]: <> (Start of the notes)"


def fetch_html(url):
    html = urllib.request.urlopen(url).read().decode("utf-8")
    return html


def parse_arxiv_content(html):
    soup = BeautifulSoup(html, "html.parser")
    # Discard span descriptions
    for span in soup.find_all("span"):
        span.decompose()
    title = soup.find("h1", class_="title").text.strip()
    authors = soup.find("div", class_="authors").text.strip().split(", ")
    dateline = soup.find("div", class_="dateline").text.strip()
    year = re.search(r"\d{4}", dateline).group()
    return title, authors, year


def get_file_name(authors, year):
    first_author_surname = authors[0].split(" ")[-1].lower()
    file_name = "{}{}.md".format(first_author_surname, year)
    # Append a letter if the file name already exists
    if os.path.exists(os.path.join("assets", file_name)):
        for letter in LETTERS:
            file_name = "{}{}{}.md".format(first_author_surname, year, letter)
            if not os.path.exists(os.path.join("assets", file_name)):
                break
    return file_name


def add_entry_to_readme(readme):
    # Find the first entry and append the new entry before it
    readme_lines = readme.split("\n")
    for i, line in enumerate(readme_lines):
        if line.startswith(README_START_COMMENT):
            readme_lines.insert(i + 1, "\n" + README_PATTERN)
            break

    readme = "\n".join(readme_lines)
    return readme


def add_entry(url):
    html = fetch_html(url)
    if "arxiv.org" in url:
        title, authors, year = parse_arxiv_content(html)
    else:
        raise NotImplementedError("Only arxiv.org is supported")

    file_name = get_file_name(authors, year)
    file_path = os.path.join("assets", file_name)

    if os.path.exists(file_path):
        raise FileExistsError("File already exists: {}".format(file_path))

    with open(file_path, "w") as f:
        f.write(
            NOTES_PATTERN.format(
                title=title,
                url=url,
                authors=", ".join(authors),
                source="arXiv Preprint",
                year=year,
            )
        )

    with open("README.md", "r") as f:
        readme = f.read()

    print("Added entry: {}".format(file_path))

    # Add pattern to the readme
    readme = add_entry_to_readme(readme)
    # Fill in the pattern
    readme = readme.format(
        filepath=file_path,
        url=url,
        title=title,
        authors=", ".join(authors),
        source="arXiv Preprint",
        year=year,
    )
    # Write the readme
    with open("README.md", "w") as f:
        f.write(readme)


def main():
    parser = argparse.ArgumentParser(description="Add a new entry to the notes")
    parser.add_argument("url", help="URL of the paper")
    args = parser.parse_args()
    add_entry(args.url)


if __name__ == "__main__":
    main()
