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


def get_markdown(data):
    df = pandas.DataFrame.from_dict(data)
    return df.to_markdown(index=False)


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

f = open("BUGS.MD", "w")
f.write(get_markdown(issues))
f.close()
