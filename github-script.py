import os
import re
import base64
import csv
import argparse
import requests
import sys


def extract_tech_stack(readme_text: str) -> str:
    if not readme_text:
        return 'Not found'
    patterns = [r'(?mi)^(?:##+\s*)?(?:built with|built-with|technolog(?:ies|y)|tech(?: stack)?)[:\s\-]*\n?(.+)$',
                r'(?mi)(?:Built with|Technologies|Tech stack|Stack):\s*(.+)']
    for p in patterns:
        m = re.search(p, readme_text)
        if m:
            return re.sub(r'\s+', ' ', m.group(1).strip())
    keywords = ['Python','Django','Flask','FastAPI','JavaScript','TypeScript','React','Vue','Angular',
                'Node','Express','Go','Rust','C++','Java','Spring','Ruby','Rails','PHP','Laravel',
                'SQL','Postgres','MySQL','MongoDB','Docker','Kubernetes']
    found = [k for k in keywords if re.search(r'\b' + re.escape(k) + r'\b', readme_text, re.I)]
    return ', '.join(found) if found else 'Not found'


def extract_use_case(readme_text: str) -> str:
    if not readme_text:
        return 'Not described'
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', readme_text) if p.strip()]
    for p in paragraphs:
        if re.search(r'!\[|\[!\[|badge', p, re.I):
            continue
        if len(p) < 20:
            continue
        summary = re.sub(r'\s+', ' ', p)
        return summary[:500]
    return 'Not described'


def fetch_readme(owner: str, repo_name: str, headers: dict) -> str:
    readme_url = f"https://api.github.com/repos/{owner}/{repo_name}/readme"
    r = requests.get(readme_url, headers=headers)
    if r.status_code == 200:
        j = r.json()
        content = j.get('content')
        if content:
            try:
                decoded = base64.b64decode(content).decode('utf-8', errors='replace')
                return decoded
            except Exception:
                return ''
    return ''


def format_as_csv(items, out_stream):
    writer = csv.writer(out_stream)
    writer.writerow(['Name', 'Tech Stack', 'Use Case', 'URL'])
    for it in items:
        writer.writerow([it['name'], it['tech'], it['use_case'], it['url']])


def _md_escape(cell: str) -> str:
    if cell is None:
        return ''
    return cell.replace('|', '\\|').replace('\n', ' ')


def format_as_markdown(items, out_stream):
    out_stream.write('| Name | Tech Stack | Use Case | URL |\n')
    out_stream.write('|---|---|---|---|\n')
    for it in items:
        name = _md_escape(it['name'])
        tech = _md_escape(it['tech'])
        use_case = _md_escape(it['use_case'])
        url = it['url'] or ''
        out_stream.write(f'| {name} | {tech} | {use_case} | {url} |\n')


def run(username: str, out_format: str, out_path: str = None):
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    token = os.environ.get('GITHUB_TOKEN')
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f'token {token}'

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"Failed to fetch repositories: {r.status_code}")
        return 1

    repos = r.json()
    items = []
    for repo in repos:
        name = repo.get('name')
        html_url = repo.get('html_url')
        owner = repo.get('owner', {}).get('login', username)
        readme_text = fetch_readme(owner, name, headers)
        tech = extract_tech_stack(readme_text)
        use_case = extract_use_case(readme_text)
        items.append({'name': name, 'tech': tech, 'use_case': use_case, 'url': html_url})

    # output
    out_stream = open(out_path, 'w', newline='', encoding='utf-8') if out_path else sys.stdout
    try:
        if out_format == 'csv':
            format_as_csv(items, out_stream)
        else:
            format_as_markdown(items, out_stream)
    finally:
        if out_path:
            out_stream.close()

    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch GitHub repos + README-derived metadata')
    parser.add_argument('--username', '-u', default='AyyanYe', help='GitHub username')
    parser.add_argument('--format', '-f', choices=['md', 'csv'], default='md', help='Output format')
    parser.add_argument('--out', '-o', help='Output file path (default stdout)')
    args = parser.parse_args()
    sys.exit(run(args.username, args.format, args.out))