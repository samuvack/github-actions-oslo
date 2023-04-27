import json
import logging
import logging.handlers
import os
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)


def generate_markdown(data):
    """
    Generate a Markdown string based on the data from a JSON file.
    """
    markdown = ""
    for key, value in data.items():
        markdown += f"## {key}\n"
        markdown += f"{value}\n\n"
    return markdown


def write_to_file(file_name, markdown):
    """
    Write the Markdown string to a file.
    """
    with open(file_name, 'w') as file:
        file.write(markdown)


# Load data from JSON file
with open('data.json', 'r') as json_file:
    data = json.load(json_file)

# Generate Markdown string
markdown = generate_markdown(data)

# Write Markdown string to file
write_to_file('output.md', markdown)

print("Markdown file has been generated successfully!")


if __name__ == "__main__":
    logger.info(f'Monitoring completed')
