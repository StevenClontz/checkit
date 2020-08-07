# CheckIt 

Platform for authoring free and open randomized exercises for practice and assessment.

Visit <https://checkit.clontz.org> to learn more.

## Developing the CheckIt platform

TODO

```bash
git clone [link from GitHub]
git update-index --skip-worktree banks/*.ipynb
```

If one of the bank notebooks needs to be updated, copy Code cells to
new ones (without running) and delete old ones for a clean result.
Then do the following.

```bash
git update-index --no-skip-worktree banks/{bank}.ipynb
git add banks/{bank}.ipynb
git commit -m "Message"
git update-index --skip-worktree banks/*ipynb
```