import re
import random
import difflib
from thefuzz import process

# Git command responses
git_help = {
    r"\b(hello|hi|hey|hiya)\b": [
        "Hello! How can I assist you today?",
        "Hey there! How's it going?"
    ],
    
    r"good morning|morning": [
        "Good morning! How can I help you today?",
        "Morning! Hope you're having a great day so far!"
    ],
    
    r"good afternoon|afternoon": [
        "Good afternoon! What can I do for you today?",
        "Afternoon! How’s your day going so far?"
    ],
    
    r"good evening|evening": [
        "Good evening! How can I assist you tonight?",
        "Evening! Hope you're having a peaceful end to your day."
    ],
    r"git init|\b(init)\b": [
        "You can use `git init` to initialize a new Git repository in your project folder. It creates a `.git/` directory to track changes. You write it like this: `git init`",
        "The `git init` command helps you start version control for a new project. It can be written like this: `git init` within the project directory."
    ],
    r"start project|initialize repository|new repo|begin git|create project|create repo|create repository|make repo": [
        "You can start a new Git project by creating a project folder, navigating into it, and then running `git init`.  Here are the steps:\n1. Create a folder: `mkdir my-project`\n2. Navigate into it: `cd my-project`\n3. Initialize Git: `git init`",
        "The `git init` command helps you initialize a new Git repository, which is the first step to start version controlling your project. The steps are:\n1. Create a new folder.\n2. Open your terminal in the new folder.\n3. Run `git init`."
    ],
    r"git remote add|remote add": [
        "You can use `git remote add` to link your local Git repository to a remote repository. You write it like this: `git remote add origin <remote_repo_url>`",
        "The `git remote add` command helps you connect your local repository to a remote one, allowing you to share your code. You can write it like this: `git remote add origin <remote_repo_url>`"
    ],r"git push|\b(push)\b": [
        "You can use `git push` to upload your local commits to a remote repository. You write it like this: `git push origin <branch-name>`. Before pushing, make sure you've committed your changes.",
        "The `git push` command helps you share your code changes with others by sending them to a remote repository. You can write it like this: `git push origin <branch-name>`. Note that you can use `-u` (e.g., `git push -u origin <branch-name>`) to set the upstream branch for your local branch, simplifying future pushes and pulls, or `-f` (e.g., `git push -f origin <branch-name>`) to force push, overwriting the remote branch's history (use with caution!)."
    ],
    r"git commit|\b(commit)\b": [
        "You can use `git commit` to save your changes with a descriptive message. You write it like this: `git commit -m 'Your commit message'`.  First, stage your changes with `git add`.",
        "The `git commit` command helps you record snapshots of your project's files, along with a message explaining what you changed. You can write it like this: `git commit -m 'Your commit message'`. Note that you can use `-a` (e.g., `git commit -a -m 'Your commit message'`) to stage all modified and deleted tracked files before committing, or `-v` (e.g., `git commit -v -m 'Your commit message'`) to include the diff of the changes being committed in the commit message editor."
    ],
    r"git branch|\b(branch)\b": [
        "You can use `git branch` to create and manage different branches of your project.  To create a branch: `git branch <branch-name>`. To switch to it: `git checkout <branch-name>`",
        "The `git branch` command helps you work on different features or bug fixes in isolation from your main codebase. To create a branch: `git branch <branch-name>`. To switch to it: `git checkout <branch-name>`. Note that you can use `-d` (e.g., `git branch -d <branch-name>`) to delete a local branch (if it has been merged), or `-D` (e.g., `git branch -D <branch-name>`) to force delete a local branch."
    ],
    r"git reset|\b(reset)\b": [
        "You can use `git reset` to undo changes in your staging area or working directory. To unstage a file: `git reset <file-name>`. To reset to a specific commit: `git reset --hard <commit-id>`",
        "The `git reset` command helps you manage changes in your local repository, allowing you to unstage files or revert to previous commits. To unstage a file: `git reset <file-name>`. To reset to a specific commit: `git reset --hard <commit-id>`. Note that `--hard` resets the working directory, staging area, and HEAD."
    ],
    r"git tag|\b(tag)\b": [
        "You can use `git tag` to mark specific commits with a descriptive name, often used for releases. You write it like this: `git tag <tag-name>`",
        "The `git tag` command helps you create labels for important points in your project's history, such as version releases. You can write it like this: `git tag <tag-name>`. Note that you can use `-a` (e.g., `git tag -a <tag-name> -m 'Your tag message'`) to create an annotated tag with a message and author information, or `-m` (e.g., `git tag -m 'Your tag message' <tag-name>`) to create a tag with a message directly on the command line."
    ],
    r"git checkout|\b(checkout)\b": [
        "You can use `git checkout` to switch between different branches or to restore files to a previous state. To switch branches: `git checkout <branch-name>`. To restore a file: `git checkout <file-name>`",
        "The `git checkout` command helps you navigate between different branches of your project or undo changes to specific files. To switch branches: `git checkout <branch-name>`. To restore a file: `git checkout <file-name>`. Note that you can use `-b` (e.g., `git checkout -b <branch-name>`) to create a new branch and immediately switch to it."
    ],
    r"git pull|\b(pull)\b": [
        "You can use `git pull` to download changes from a remote repository and merge them into your current branch. You write it like this: `git pull origin <branch-name>`",
        "The `git pull` command helps you keep your local branch up-to-date with the latest changes from the remote repository. You can write it like this: `git pull origin <branch-name>`. Note that you can use `--rebase` (e.g., `git pull --rebase origin <branch-name>`) to integrate changes by rebasing instead of merging."
    ],
    r"git fetch|\b(fetch)\b": [
        "You can use `git fetch` to download changes from a remote repository without automatically merging them. You write it like this: `git fetch origin <branch-name>`",
        "The `git fetch` command helps you see the changes available on the remote repository before deciding whether to merge them into your local branch. You can write it like this: `git fetch origin <branch-name>`. Note that you can use `--prune` (e.g., `git fetch --prune origin`) to remove any local references to remote branches that have been deleted on the remote repository."
    ],
    r"git remote|\b(remote)\b": [
        "You can use `git remote` to manage connections to remote repositories.  You write it like this: `git remote` (to list remotes).",
        "The `git remote` command helps you configure and interact with remote repositories. You can write it like this: `git remote` (to list remotes). Note that you can use `-v` (e.g., `git remote -v`) to view the remote repositories and their associated URLs in more detail."
    ],
    r"git diff|\b(diff)\b": [
        "You can use `git diff` to see the differences between your working directory, staging area, and previous commits. For working directory vs. staging area: `git diff`. For comparing commits: `git diff <commit-id1> <commit-id2>`",
        "The `git diff` command helps you understand the changes you've made to your project files. For working directory vs. staging area: `git diff`. For comparing commits: `git diff <commit-id1> <commit-id2>`. Note that you can use `--staged` or `--cached` (e.g., `git diff --staged`) to see the differences between the staged changes and the last commit."
    ],
    r"git log|\b(log)\b": [
        "You can use `git log` to view the history of commits in your repository. You write it like this: `git log`",
        "The `git log` command helps you see a list of all the commits that have been made to the project, including their messages and authors. You can write it like this: `git log`. Note that you can use `--oneline` (e.g., `git log --oneline`) to display a condensed version of the commit history, or `-p` (e.g., `git log -p`) to display the commit history along with the diffs for each commit."
    ],
    r"git clone|\b(clone)\b": [
        "You can use `git clone` to create a copy of a remote repository on your local machine. You write it like this: `git clone <repo_url>`",
        "The `git clone` command helps you download an existing Git repository to your computer. You can write it like this: `git clone <repo_url>`"
    ],
    r"git status|\b(status)\b": [
        "You can use `git status` to check the current state of your Git repository, including changes that have been made but not yet committed. You write it like this: `git status`",
        "The `git status` command helps you see which files have been modified, added, or deleted in your project. You can write it like this: `git status`"
    ],
    r"git merge|\b(merge)\b": [
        "You can use `git merge` to combine changes from one branch into another branch. You write it like this: `git merge <other-branch-name>` (after checking out the target branch). Here are the steps:\n1. Checkout the target branch: `git checkout <target-branch>`\n2. Merge the other branch: `git merge <other-branch-name>`",
        "The `git merge` command helps you integrate changes from one branch into another, bringing different lines of development together. The steps are:\n1. Checkout the target branch.\n2. Run `git merge <other-branch-name>`."
    ],
    r"delete branch|\b(delete)\b": [
        "To delete a branch: \n1️⃣ Locally: `git branch -d <branch-name>`\n2️⃣ Remotely: `git push origin --delete <branch-name>`",
        "To delete a branch locally, use `git branch -d <branch-name>`. For remote branches, use `git push origin --delete <branch-name>`."
    ],
    r"gitignore|\b(ignore)\b": [
        "You can use a `.gitignore` file to specify which files and directories Git should ignore. You write rules for it in the `.gitignore` file itself.",
        "The `.gitignore` file helps you prevent unwanted files (like temporary files, build artifacts, or sensitive data) from being accidentally added to your Git repository. You create and edit this file directly in your project directory.  There's no direct command to 'run' on the `.gitignore` file; Git automatically reads it."
    ],
    r"git add": [
        "You can use `git add` to add files to the staging area, preparing them for commit.  You write it like this: `git add <file-name>` (for a specific file) or `git add .` (for all changes).",
        "The `git add` command helps you select which changes you want to include in your next commit. You can write it like this: `git add <file-name>` (for a specific file) or `git add .` (for all changes). Note that you can use `-p` (e.g., `git add -p`) to interactively patch changes, allowing you to choose which parts of a file to stage."
    ],
    r"git config|configure": [
        "You can use `git config` to configure your Git username and email. You write it like this: `git config --global user.name 'Your Name'` and `git config --global user.email 'your.email@example.com'`.",
        "The `git config` command helps you set your global Git configuration, including your name and email, which are included in your commits. You can write it like this: `git config --global user.name 'Your Name'` and `git config --global user.email 'your.email@example.com'`.  The `--global` option sets these for all your repositories."
    ],

    # Push issues
    r"can't push|can not push|unable to push|push not working|push fails": [
        "I'm sorry to hear you're having trouble pushing to GitHub. Let's check a few things:\n"
        "1. Are you authenticated? Try `git remote -v` to see if your remote is set up.\n"
        "2. If you're using HTTPS, make sure your credentials are correct.\n"
        "3. If you get an error about rejected updates, try `git pull --rebase` before pushing.\n"
        "4. If you rebased or amended commits, you might need to force push: `git push --force` (use with caution!).\n"
        "5. If you see a permission error, check your SSH key with `ssh -T git@github.com` or verify repository access."
    ],

    # Pull issues
    r"can't pull|can not pull|unable to pull|pull not working": [
        "It looks like you're having trouble pulling updates. Here are some things to check:\n"
        "1. Do you have uncommitted changes? Run `git status`—if you do, commit or stash them with `git stash`.\n"
        "2. If there’s a conflict, Git will show a merge error. Resolve conflicts, then run `git commit`.\n"
        "3. If `git pull` hangs, check your internet connection or remote availability with `git remote -v`.\n"
        "4. If your branch is out of sync, try `git fetch origin` followed by `git merge origin/<branch>` instead of `git pull`."
    ],

    # Clone issues
    r"can't clone|can not clone|unable to clone|clone fails|clone error": [
        "Cloning issues can have multiple causes. Try these steps:\n"
        "1. Check if the repository URL is correct by visiting it in a browser.\n"
        "2. If using SSH, ensure your SSH key is added to GitHub (`ssh -T git@github.com`).\n"
        "3. If you see a 'Permission Denied' error, try switching to HTTPS (`git clone https://github.com/user/repo.git`).\n"
        "4. If the clone is slow or stuck, check your internet connection and firewall settings."
    ],

    # Merge conflicts
    r"merge conflict|conflict during merge|error merging": [
        "Merge conflicts can be tricky, but here’s how to resolve them:\n"
        "1. Run `git status` to see which files have conflicts.\n"
        "2. Open the conflicting files and manually choose which changes to keep.\n"
        "3. After resolving conflicts, stage the files using `git add <file>` and commit with `git commit`.\n"
        "4. If you want to cancel the merge, use `git merge --abort`."
    ],

    # Detached HEAD state
    r"detached head|lost commit|cannot find branch|can't find branch": [
        "It looks like you’re in a detached HEAD state. Here's what you can do:\n"
        "1. If you need to save your work, create a new branch: `git checkout -b new-branch`.\n"
        "2. To go back to a branch, run `git checkout <branch-name>`.\n"
        "3. If you lost a commit, try `git reflog` to find and restore it with `git checkout <commit-hash>`."
    ],

    # Permission issues
    r"permission denied|access denied": [
        "Permission issues often occur due to authentication problems. Try these:\n"
        "1. If using SSH, test your connection with `ssh -T git@github.com`.\n"
        "2. If you see 'Permission Denied', check if your SSH key is added to GitHub.\n"
        "3. Try using HTTPS instead of SSH: `git remote set-url origin https://github.com/user/repo.git`.\n"
        "4. If working with a private repo, ensure your account has the right access."
    ],

    # Commit issues
    r"can't commit|can not commit|unable to commit|commit error": [
        "Commit issues usually come from untracked or unstaged changes. Check these steps:\n"
        "1. Run `git status` to see which files are modified or untracked.\n"
        "2. If files are missing, add them with `git add <file>` before committing.\n"
        "3. If you see an error about author identity, set it up with `git config --global user.name 'Your Name'` and `git config --global user.email 'you@example.com'`.\n"
        "4. If a commit is stuck, try `git commit --amend` or `git reset --soft HEAD~1`."
    ],

    # Fetch issues
    r"can't fetch|can not fetch|unable to fetch|fetch error": [
        "Having trouble fetching updates? Try these fixes:\n"
        "1. Run `git remote -v` to check if the remote URL is correct.\n"
        "2. If fetch hangs, check your internet connection or repository availability.\n"
        "3. If you get a 'refusing to update' error, try `git remote prune origin` to remove stale references.\n"
        "4. If your branch isn’t updating, use `git fetch --all` to get all changes."
    ],

    # Rebase issues
    r"rebase error|can not rebase|can't rebase|rebase conflict": [
        "Rebase issues can be resolved with these steps:\n"
        "1. If conflicts occur, resolve them manually, then run `git rebase --continue`.\n"
        "2. To cancel a rebase, use `git rebase --abort`.\n"
        "3. If rebase fails due to uncommitted changes, stash them with `git stash`, then retry.\n"
        "4. If interactive rebase (`git rebase -i HEAD~3`) isn’t working, check commit history with `git log --oneline`."
    ],
    
    r"\b(goodbye|bye|see you|take care)\b": [
        "Goodbye! Have a great day ahead!",
        "Take care! See you next time!"
    ]
}

general_problems= {r"\b(problem|can't|can not|unable|fails|issue|trouble|error|struggle|having trouble|having issues)\b.*": [
    "I'm sorry, I couldn't quite understand the issue you're facing. Could you please provide more details about the problem? It would help me assist you better.\n"
    "In the meantime, you can try the following steps if the problem persists:\n"
    "1. Check your internet connection and ensure it's stable.\n"
    "2. Verify if your Git configuration is correct by running `git config --list`.\n"
    "3. Make sure your Git is up to date. Run `git --version` to check and update if necessary.\n"
    "4. If you recently updated Git or made changes to your setup, restarting your terminal or computer can sometimes resolve unexpected issues.\n"
    "5. If the problem persists, you may want to consult the Git documentation or search for specific error messages you’ve encountered for more detailed help."
    ]}

# Random fallback responses for unmatched inputs
fallback_responses = [
    "I'm not sure about that, but I could help you with Git if you need.",
    "That doesn’t seem familiar, but if you have any Git-related questions, I'm here to help.",
    "I didn’t quite get that, but I can definitely assist with Git topics.",
    "I might not have an answer for that, but feel free to ask me about Git.",
    "Not sure about that one, but if you're working with Git, I’d be happy to help."
    # "I'm not sure about that command. Try asking about `git init`, `git clone`, or `git push`.",
    # "Hmm, I don’t recognize that. Could you rephrase or ask about Git commands like `git commit`?",
    # "I didn’t understand. Maybe you meant something like `git branch` or `git merge`?",
    # "That's not something I know yet! But I can help with Git commands like `git status` or `git checkout`.",
    # "That doesn’t match any Git command I know. Try something like `git log` or `git pull`."
]

eliza_patterns = [
    (r"\b(hello|hi|hey)\b", "Hey there! How’s your day going? Let me know if you need help with Git."),
    (r"(good morning|good evening|good afternoon)", "Good day! Hope things are going well. Need any Git assistance?"),
    (r"(how are you|how’s it going|how do you do)", "I’m doing well, thanks for asking! How about you? Need any Git help?"),
    (r"(tell me a joke|make me laugh)", "Alright! Why do programmers prefer dark mode? Because light attracts bugs! 😆 Also, if you need Git help, I’m here."),
    (r".*\b(bored|tired|sick|happy|sad|excited|angry|upset)\b.*", "I hear you. Hope things get better soon! Let me know if I can help with Git."),
    (r"i am (.*)", "I see, you’re {0}. Hope you're doing well! Let me know if you need help with Git."),
    (r"i feel (.*)", "That’s understandable. What’s on your mind? By the way, I can also help with Git if needed."),
    (r"why (.*)", "That’s an interesting question! If you're dealing with Git issues, I might have some answers."),
    (r"what (.*)", "That depends! If it's something about Git, I’d be happy to explain."),
    (r"how (.*)", "Good question! If you’re asking about Git, I can definitely help."),
    (r"because (.*)", "That makes sense. If you're working with Git and run into trouble, I’m here."),
    (r"can you (.*)", "I might not be able to {0}, but I can definitely help with Git!"),
    (r"do you (.*)", "That’s an interesting thought! If you’re dealing with Git, I can assist."),
    # (r".*", "That’s interesting! If you're working on Git and need help, I’d be happy to assist.")
]

alternatives = ["additionally", "furthermore", "moreover", "besides", "also"]

# Define stopwords (expand this list as needed)
stopwords = {"what", "does", "do", "or", "make", "is", "the", "a", "an", "why", "how"}

# keywords = ['git init', 'start project', 'initialize repository', 'new repo', 'begin git', 'git remote add', 'remote add', 'git push', 'push', 'git clone', 'clone', 'git status', 'status', 'git commit', 'commit', 'git branch', 'branch', 'git merge', 'merge', 'git log', 'log', 'git checkout', 'checkout', 'git pull', 'pull', 'git fetch', 'fetch', 'git reset', 'reset', 'git diff', 'diff', 'git tag', 'tag', 'how do I (initialize', 'create) a new git repository', 'how do I create a new branch', 'how do I check the status of my repository', 'how do I add files to the staging area', 'how do I commit changes', 'how do I push my changes', 'how do I pull changes from the remote repository', 'how do I clone a git repository', 'how do I merge branches', 'how do I delete a branch', 'how do I reset my repository', 'what is a .gitignore', 'how do I configure my git username and email', 'git push -u', 'push -u', 'git commit -a', 'commit -a', 'git commit -m', 'commit -m']
# def get_best_match(user_input):
#     match, score = process.extractOne(user_input, keywords)
#     if score > 80:  # Accept if similarity is high
#         return match  
#     return None
polite_closings = [
    "Let me know if you need further assistance.",
    "I hope that helps! Let me know if you have more questions.",
    "Does that answer your question?",
    "Let me know if anything needs clarification.",
    "Feel free to ask if you need more details.",
    "I'm here to help if you have any other issues.",
    "Would you like to go over anything else?",
    "If you run into any more issues, don’t hesitate to ask.",
    "I'm happy to assist further if needed.",
    "Let me know how else I can support you."
]
def clean_input(user_input):
    # Lowercase and split into words
    words = re.findall(r'\b\w+\b', user_input.lower())
    # Remove stopwords
    filtered_words = [word for word in words if word not in stopwords]
    return " ".join(filtered_words)  # Reconstruct cleaned phrase

def find_best_match(user_input): #Finds the closest matching Git command if an exact match isn't found.
    command_list = []
    for key in git_help.keys():
        parts = re.sub(r'\b|(|)', '', key).split('|')  # Remove \b, (), and split on |
        command_list.extend(parts)
    match = difflib.get_close_matches(user_input, command_list, n=1, cutoff=0.7)
    return match[0] if match else None

def eliza_fallback(user_input):
    user_input = user_input.lower().strip()

    # Check for Eliza-style patterns
    for pattern, response in eliza_patterns:
        match = re.search(pattern, user_input)
        if match:
            return response.format(*match.groups())

    # If no match, return a general fallback with a Git reminder
    return random.choice(fallback_responses)

def git_assistant(user_input):
    user_input = user_input.lower()
    matched_responses = []
    
    # Check for matching Git command patterns
    for pattern, responses in git_help.items():
        if re.search(pattern, user_input):
            matched_responses.append(random.choice(responses))  # Pick one response per match

    if matched_responses:
        
        separator = random.choice(alternatives)  # Randomly select an alternative separator
        return f" \n{separator} ".join(matched_responses)+"\n\n"+random.choice(polite_closings)  # Join responses with the chosen separator

    best_match = find_best_match(clean_input(user_input))
    if best_match:
        for pattern, responses in git_help.items():
            if re.search(pattern, best_match):
                return f"Did you mean `{best_match.split('|', 1)[0]}`? \n{random.choice(responses)}\n\n{random.choice(polite_closings)}"
                # matched_responses.append(random.choice(responses))
                # return f"Did you mean `{best_match}`? \n{matched_responses[0]}"
    
    for pattern, responses in general_problems.items():
        if re.search(pattern, user_input):
            return random.choice(responses)+"\n\n"+random.choice(polite_closings)  # Pick one response per match


    return eliza_fallback(user_input)  # Return a random fallback response if no match is found
# Example usage

# while True:
#     user_input = input("You: ")
#     if user_input.lower() in ["exit", "quit"]:
#         print("Git Assistant: Goodbye!")
#         break
    
#     print("Git Assistant:", git_assistant(user_input))
