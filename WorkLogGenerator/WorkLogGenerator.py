"""Get commits form the repo specified as parameter and write work log."""
import os
import sys

from github import Github


def format_message_for_rst(message):
    """Format message for a nice rst print."""
    new_message = ""
    split_message = message.splitlines()
    for i in range(len(split_message)):
        if i is not 0 and split_message[i] is not "":
            new_message += "- "
        new_message += split_message[i] + "\n" * 2
    return new_message


def main(output, token, repo_name):
    """
    Catch main function.

    Read commits from repo_name and write to output file in rst format.
    """
    restTructuredText = ""

    g = Github(token)
    message = "Journal de travail"
    restTructuredText += message + "\n"
    restTructuredText += '=' * len(message) + "\n" * 2
    repo = g.get_user().get_repo(repo_name)
    for commit in repo.get_commits():
        com = commit.commit
        date = com.author.date
        restTructuredText += str(date) + "\n"
        restTructuredText += '-' * len(str(date)) + "\n" * 2
        restTructuredText += format_message_for_rst(com.message)

    with open(output, 'a') as f:
        f.write(restTructuredText)


def get_possible_repos(token):
    print('Your available repositories are:')

    g = Github(token)
    for repo in g.get_user().get_repos():
        print(f'\t{repo.name}')


def get_token():
    try:
        GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
    except KeyError as e:
        print(f'Environnement variable {e} not found!')
        print('Put your github token in an environnement variable!')
        exit(-1)

    return GITHUB_TOKEN


if __name__ == "__main__":

    tok = get_token()

    if len(sys.argv) < 2:
        print("Please specify the target repository.")
        get_possible_repos(tok)
        exit(-1)

    output = 'workLog.rst'
    repo_name = str(sys.argv[1])

    if os.path.isfile(output):
        os.remove(output)

    main(output, tok, repo_name)
