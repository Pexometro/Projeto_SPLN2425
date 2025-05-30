import csv
import html
from collections import defaultdict
import sys

if sys.argv[1] == "Famalicao":
        cidade = "Famalicao"
        print("Famalicao")
elif sys.argv[1] == "VilaReal":
        cidade = "VilaReal"    
        print("VilaReal")
else:
        print("Cidade não reconhecida. A execução do script será encerrada.")
        sys.exit(1) 

def csv_to_html_table(csv_file_path):
    """
    Converts a CSV file to an HTML table with clickable links.

    Args:
        csv_file_path (str): The path to the CSV file.

    Returns:
        str: An HTML string representing the table.
    """

    html_table = "<table>\n"
    
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        for i, row in enumerate(csv_reader):
            html_table += "  <tr>\n"
            for col_index, cell in enumerate(row):
              # Check if it's the 'documento' column
                if i == 0:
                  html_table += f"    <th>{html.escape(cell)}</th>\n"
                elif csv_file_path.split('/')[-1] == f"{cidade}/entidades_{cidade}.csv" and col_index == 2:
                  # Make the content of the cell a clickable link
                  html_table += f"    <td><a href='{html.escape(cell)}' target='_blank'>{html.escape(cell)}</a></td>\n"
                else:
                  html_table += f"    <td>{html.escape(cell)}</td>\n"
            html_table += "  </tr>\n"
    
    html_table += "</table>\n"
    return html_table

def create_html_file(html_content, output_file_path):
    """
    Creates an HTML file with the given content.

    Args:
        html_content (str): The HTML content to write to the file.
        output_file_path (str): The path where the HTML file should be saved.
    """
    with open(output_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

# Main script execution
csv_file_path = f"{cidade}/entidades_{cidade}.csv" 
output_file_path = f'entidades_{cidade}.html' 

html_table_content = csv_to_html_table(csv_file_path)
create_html_file(f"<html><head><meta charset='utf-8'></head><body>{html_table_content}</body></html>", output_file_path)

print(f"HTML file created successfully: {output_file_path}")