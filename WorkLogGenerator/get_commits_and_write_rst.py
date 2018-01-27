"""Get commits form the repo specified as parameter and write work log."""
import os
import sys

from github import Github

from tokens import GITHUB_TOKEN


def format_message_for_rst(message):
    """Format message for a nice rst print."""
    new_message = ""
    split_message = message.splitlines()
    for i in range(len(split_message)):
        if i is not 0 and split_message[i] is not "":
            new_message += "- "
        new_message += split_message[i] + "\n" * 2
    return new_message


def main(output, repo_name):
    """
    Catch main function.

    Read commits from repo_name and write to output file in rst format.
    """
    restTructuredText = ""
    g = Github(GITHUB_TOKEN)
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


if __name__ == "__main__":

    if len(sys.argv) < 2:
        exit("Il est nécessaire de spécifier sur \
             quel dépôt effectuer la recherche")

    output = 'workLog.rst'
    repo_name = str(sys.argv[1])

    if os.path.isfile(output):
        os.remove(output)

    main(output, repo_name)
