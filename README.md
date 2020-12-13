# CheckIt

Platform for authoring free and open randomized exercises for practice and assessment.

Exercise banks are hosted for the public at
<https://checkit.clontz.org>.

## Generating new exercises or authoring an exercise bank

The ☑️It platform runs completely inside your web browser, powered by 
[CoCalc.com](https://cocalc.com/)! Open the
[template project](https://share.cocalc.com/share/ba2dd9e2216be0d5c07a18a509afaadeebaf451c/checkit-public/?viewer=share)
and click the green "Open with one click!" button.
(CoCalc trial accounts take some time to load and compute, so consider
purchasing a CoCalc subscription if you like using CheckIt.)
Open <c>dashboard.ipynb</c> to get started.

Our community of authors and developers is organized in the #checkit-app channel of the
[Mastery Grading Slack workspace](https://bit.ly/join-mastery-grading). Come join us!

## TODO PUT IN DASH Generating an exercise bank for Canvas

In a CoCalc project (see previous section),
open the `banks/build.ipynb` notebook and run the cell,
making sure `fixed=False` and `public=False`.

Inside the bank folder, a `build` folder should be present. Select the `qti-bank` folder
and download the `zip` file to your computer. This file can be uploaded to Canvas
via these instructions at
[community.canvaslms.com](https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-import-quizzes-from-QTI-packages/ta-p/1046).

## Developing the CheckIt platform

The following lines will get you set up to start developing. Note
that the Jupyter notebooks used to generate/preview exercise banks
change every time they are used, so we ignore those changes in general.

```bash
git clone git@github.com:StevenClontz/checkit.git
git update-index --skip-worktree dashboard.ipynb
```

If the dashboard actually needs to be updated, copy Code cells to
new ones (without running) and delete old ones for a clean result.
Then do the following.

```bash
git update-index --no-skip-worktree dashboard.ipynb
git add dashboard.ipynb
git commit -m "Updated dashboard notebook."
git update-index --skip-worktree dashboard.ipynb
```

## Why "CheckIt"?

This platform was known as "Mastr/MasterIt" in the past.
While the exercise banks on this platform
are generally designed with Mastery/Pointless Grading in mind, there's
no hard-requirement that they be used for this purpose. But as
[Jean-Sébastien](https://twitter.com/JeanSebTurcotte/status/1290691807718903808)
pointed out, "CheckIt" emphasizes the purpose of the platform:
to *check* student understanding, while also reflecting the use
of checkmarks in many objective-based grading systems.