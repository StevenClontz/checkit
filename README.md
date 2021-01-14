# CheckIt Dashboard

A platform for authoring free and open randomized exercises for practice and assessment.

Exercise banks are hosted for the public using the *CheckIt Viewer*, available at
<https://checkit.clontz.org>.

## Running the CheckIt Dashboard

The CheckIt Dashboard runs completely inside your web browser, powered by
[CoCalc.com](https://cocalc.com/). Open the
[template project](https://cocalc.com/share/00854508a0fa6e8a193cbc90aff10b9dd7f446b4/checkit/?viewer=share)
and click the green "Open with one click!" button.
(CoCalc trial accounts take some time to load and compute, so consider
purchasing a CoCalc subscription if you like using CheckIt.)

Open `dashboard.ipynb` to get started. The dashboard contains instructions on
**previewing exercises** to get a new randomly generated exercise, and
**building banks** to get files for a bank that can be used with
your LMS or the CheckIt Viewer.

## Connect with the community

Our community of authors and developers is organized in the #checkit-app channel of the
[Mastery Grading Slack workspace](https://bit.ly/join-mastery-grading). Come join us!

## Using your bank with the CheckIt Viewer

Using custom generated banks with the CheckIt Viewer at <https://checkit.clontz.org>
is not yet supported, but will be in the future. For now, contact
[Steven Clontz](mailto:steven.clontz@gmail.com) if you have a bank you'd like to
share with the public on the Viewer.

## Using your bank with Canvas

First use the dashboard to build a private version of the bank you wish to use with Canvas.
The output from the dashboard will tell you where to browse using CoCalc's file manager
to download `canvas-outcomes.csv` and `canvas-qtibank.zip`.

- Instructions for uploading outcomes: [community.canvaslms.com](https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-import-outcomes-for-a-course/ta-p/702)
- Instructions for uploading QTI bank (exercises for use on quizzes): [community.canvaslms.com](https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-import-quizzes-from-QTI-packages/ta-p/1046).

## Developing the CheckIt Dashboard

The following lines will get you set up to start developing. Note
that the Jupyter notebook serving as the dashboard GUI
changes every time it is used to save the latest output,
so we want to ignore those changes in general.

```bash
git clone git@github.com:StevenClontz/checkit.git
git update-index --skip-worktree dashboard.ipynb
```

If the dashboard's underlying code needs to be updated, copy each Code cell to a
new one (without running) and delete each old one for a clean result.
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
of checkmarks in many outcomes-based grading systems.

An important note: CheckIt aims to provide instructors a tool to efficiently check students'
understanding directly by quickly providing randomly-generated exercises
that typically ask for full explanations rather than just typing in a "final answer";
there is no automatic grading of these exercises.