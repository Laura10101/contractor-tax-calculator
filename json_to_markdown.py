"""Generate a markdown file from Github JSON data"""
import json
import pandas

# Load the JSON data
f = open('issues.json')
raw = json.load(f)
f.close()

# Helper functions


def remove_multiple_blank_lines(string):
    string = string.replace('\r\n', '<br/>')
    while '<br/><br/>' in string:
        string = string.replace('<br/><br/>', '<br/>')
    return string


def issue_key(issue):
    return issue['Number']


def get_markdown(issues):
    issues.sort(key=issue_key)

    # Add title lines
    md_lines = []
    md_lines.append('# Resolved Bugs\r\n')
    md_lines.append(
        'The folllowings bugs have been resolved '
        + ' and retested.\r\n'
    )

    # Add issue lines
    for issue in issues:
        md_line = str(issue['Number'])
        md_line += '. **' + issue['Title'] + '**<br/>'
        md_line += issue['Description'] + '<br/>'
        md_line += '**Resolution**<br/>' + issue['Resolution']
        md_line += '\r\n'

        md_lines.append(md_line)
    return md_lines


# Generate issues dictionary from raw data
issues = []
for gh_issue in raw:
    print(str(gh_issue))

    # Extract and format data
    title = '[' + gh_issue['title'] + '](' + gh_issue['url'] + ')'
    description = remove_multiple_blank_lines(gh_issue['body'])
    solution = ''
    try:
        solution = remove_multiple_blank_lines(gh_issue['comments'][0]['body'])
    except Exception:
        pass

    # Create issue dictionary
    issue = {
        'Number': gh_issue['number'],
        'Title': title,
        'Description': description,
        'Resolution': solution
    }
    print(str(issue))
    issues.append(issue)

md = get_markdown(issues)
print(md)

f = open("BUGS.MD", "w")
for line in md:
    f.write(line + '\r\n')
f.close()
