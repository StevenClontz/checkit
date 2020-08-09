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

## Why "CheckIt"?

I used to call this platform "Mastr/MasterIt", but switched
to ☑️It/CheckIt. While the problem banks on this platform (so far)
are designed with Mastery/Pointless Grading in mind, there's
no hard-requirement that they be used for this purpose. But as
[Jean-Sébastien](https://twitter.com/JeanSebTurcotte/status/1290691807718903808)
pointed out, "CheckIt" emphasizes the purpose of the platform:
to *check* student understanding, while also reflecting the use
of checkmarks in many objective-based grading systems (such
as my own).