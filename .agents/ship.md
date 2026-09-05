Commit only on the current branch. If HEAD is the default branch `lab-base`, run `git fetch origin amp-fit2/work && git checkout --track origin/amp-fit2/work`.

Never checkout, switch, merge, rebase, or push `lab-base`. Never force-push.

Open the pull request only through:

```
python3 .agents/gh_repo_guard.py pr create --repo ampfit2-lab/ampfit2-lab--alishahryar1--free-claude-code --base lab-base --head amp-fit2/work
```

Never merge. Report the URL and stop.
