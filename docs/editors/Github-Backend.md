# GitHub Features

GitHub's Version Control can handle very complex situations comprising multiple systems built by large teams distributed over wide geographies and languages.  This is great in that it will handle nearly every situation in which we're likely to find ourselves; the downside is that it can be overwhelming when all you're expecting to use is a fraction of that power.  

GitHub is based around collections of folder and files called “repositories”, or repos for short.  How to organizes repos is really up to the user, but for the time being I have one repo called “board”, which basically corresponds to everything Simbli provides for us today.  Eventually big repos can split up, or smaller repos consolidated, but generally keeping everything in a single repo is the best place to start until and unless they good too large to manage.

Repos also provide for various Permission levels.  So, for instance, one person can have full privileges, while another might only be able to read what’s what’s in a repo but not make contributions, or another just write, etc.  These permissions will be managed by Dave to start, but can eventually transition to Devan's team.

Since repos are designed to be distributed, you can have multiple repos in multiple places depending on the need.  Typically there is one repo considered the “origin”, which basically means that it is the main repo which represents the ultimate state of truth.  This is the repo that GitHub hosts, but we could easily have one housed on our own servers if necessary.  

Then, there can be other repos which are copies of the main ‘origin’ called ‘remotes’.  The most typical use of remotes is to have a copy of the repo on an individual’s computer so that they can work on the files independently.  Eventually we may wish to have remotes for each of us, but we’ll save that for the future. For our purposes, we will be working directly with the origin repo through the web interface found at https://www.github.com.  

Again, there is a huge amount of functionality when using GitHub, but we'll focus on four main concepts to start:

1. Branching
1. Commits
1. Pull Requests
1. Merging

#### Branching

Branching is equivalent to duplicating Word files.  When you create a branch, you are making a copy of the original file, which you then own and can make edits to.  The main branch -- sometimes referred to as the “trunk” -- is what is considered the “official” file, equivalent to what the Board has approved and is currently in force at the District.  Multiple people can work on the same branch, and there can be multiple branches at any given time.  

Once branched, that set of files can be worked on independently from the main trunk, and periodically receive updates from GitHub (called ‘pulling’) or to send updates to GitHub (called ‘pushing’).  

The power of GitHub resides in its ability to manage the state and changes between these branches automatically.  We’ll revisit this later when we get into the fourth concept of ‘merging’.

#### Commits

Commits are equivalent to saving Word files.  More precisely, it’s like a “Save As”, with each save representing a particular version of the document at that time.  Commits can be made to any branch at any time; every commit is saved forever; and every commit includes meta-data about the commit itself (such as side-discussions or notes about what was changed in that particular commit.)

Commits allow us to go back into time to correct errors, to see what we were thinking at a particular moment, or to see the evolution of a policy document, etc.  All commits have unique identifiers, and so this allows us to see the entire history of everything at any moment, and is a very powerful feature of GitHub.

One key difference between a commit and a save is that commits can refer to multiple files at the same time.  For instance, if we were to update a policy by breaking it out into an AR, both the changes to the Policy and the AR can be bundled in the same commit; again, the commit itself is just a reference pointer to what the entire repo looks like at that particular moment in time.  So when working on an actual policy you save the file and make changes to it as often as you like; only when a commit is made does that state get a permanent reference.  

And it’s also worth noting that deleting a file (which is analogous to rescinding) doesn’t actually remove the file forever; it simply removes it from the current version of the main trunk.  It is very straightforward to go back in time to a commit when the file still existed, and it will pop back into place with no recovery required.  

This part is important, as while our repo today is “Private” and accessible only to invited members, I do hope that eventually it can be made “Public”, which means that everything done is part of the public record.  I consider this a feature, not a bug, but it does mean that we need to recognize nothing is every really deleted from GitHub; it just  means that it’s no longer officially part of the “main” branch.

#### Pull Requests

Pull Requests are equivalent to sending an email with an attached Word file and saying “can we add this text to the policy?”  As mentioned before, when we update files to GitHub that is called a “push”, and when we update files from GitHub that is called a “pull”.  And of course, this means that these terms are reversed depending on the perspective (ie, one person’s push is the other person’s pull).  

In this context, a Pull Request refers to the person who has made the changes on a branch making a `request` for the main trunk to `pull` those changes and make them part of the official repo.  The Pull Request itself is simply a particular commit (again, a particular branch representing a particular set of files with particular changes at a particular point in time) bundled in such a way that are designed to ensure whatever makes it into the main trunk has passed certain checks.

For instance, one of those checks could be to ask specific reviewers to look at the Pull Request and approve it, reject it with recommendations, or simply provide feedback.  You can add specific checks such as mandatory reviews from particular people, or computerized checks like spelling, or more complicated checks that “passes an Artificial Intelligence for legality”, etc.

We can manage multiple Pull Requests at a time, with multiple checks as we choose.  Once these checks pass, the Pull Request is ready for merging into the main trunk, which is the last step in the workflow.

For our purposes, the creation of a Pull Request effectively means “we’d like to send this collection of changes to the Board.  Do you approve? ”  Prior to that, various commits and back and forth edits and comments can be made on the branch itself -- and should -- without creation of a pull request.   The Pull Request simply formalizes things so that we have a record of it officially being ready for a reading/action.

#### Merging

Merging is the equivalent of doing all the final editing in a single Word document, saving the results, and printing it out as the final version.  It can be as simple as accepting the final file in one swipe, or as complicating as reconciling differences word-by-word.

Once a pull request is merged, it becomes part of the main trunk -- along with all of the commits, edits, notes, changes, history, etc. -- and the branch itself effectively ceases to exist.

GitHub provides many tools to help ease the merging process, including presenting clear and precise “diffs” (the differences between the file versions) from the main branch, prior versions of the edited commits, or anything at any point in the history of the policies.  However, the merging process itself is still manual: a human being must decide what is OK to include and what is not.

In computer code, this person typically is a project manager of some type who is ultimate responsible for what gets in to the main branch.  In our world, this is Board itself when it decides to approve a policy revision.  So for us, the workflow will be for Niki to review all Pull Requests and ensure they are ready for the Agenda, then posted, then voted on and, if approved, then merged into the main branch and are official policy.

### Summary
Most of what I described above is handled specifically by the Decap CMS tool.  However, should the need arise to do something not managed by Decap, then you can always use Github directly on the back-end to accomplish what you want.
