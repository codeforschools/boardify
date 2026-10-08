# Editing Workflow

> These instructions are the same whether for Policies or Regulations.

Access the Content Management System (CMS) at the following link:

[https://board.westada.org/admin](https://board.westada.org/admin)

If you are not immediately sent to the Boardify home page, see [Authentication](Authentication.md).

## Home Page
We're going to focus on the content-management components of Boardify.  If you would like a full explanation of all features, as Dave or IT.

On the left menu, you'll see two main sections:  Collections and Files.  The "Files" is a list of the Home Page itself and the various content sections (Mission, Board, Admin, etc.)  These shouldn't change that often, but should you need to make updates to the section landing pages this is where you do that.

> **The Difference Between Editing and Publishing**
> It's important to understand the distinction between Editing and Publishing.  **Editing** is the work we do to change the content itself -- either Updating, Creating, or Deleting.  This is the actual work of changing the words themselves within the content.  **Publishing** is the decision to make those changes available to the public on the website.
> So in our context, we can propose changes to a policy, which then gets presented to an audience that decides to accept or reject those changes.  The proposed changes themselves are part of the Editing Workflow.  The decisions to accept/reject changes are part of the Publishing Workflow.


There are three types of edits that you can make to a Policy or Regulation: Update, Create or Delete.

### Update

Most of the time, you'll be updating an existing policy.  This is fairly straightforward: click on the policy/regulation, make the proposed changes, and click save.  That's pretty much it.  This creates a new draft of the policy, and even though it's the same number it **does not touch** what is currently active and official.  I explain below about how the draft process works internally, but for you it's as simple as making and saving your changes.  Note this is very different than how you would operate in Word or Simbli; just be aware that it's expected that you make your updates directly on the policy itself.  More precisely: do **not** make a duplicate either directly or by creating a copy of what already exists.  Make the proposed changes directly on the policy you want to update; nothing will be made live until expressly asked to be made so.

### Create

Less frequently you may need to create an entirely new policy that doesn't exist.  In that case, you'll need to click on section where the new policy will live, and then click the button on the top right that says "New".  This will open up a screen where you'll add all of the details on the policy/regulation, including the code number, title, type, references and of course the content itself.  Again, this doesn't make anything official -- it just creates a new draft for everyone to work on.  For more details on the "what do I enter where", be sure to check the [Style Guide](Style-Guide.md).

### Delete

Finally, you may need to rescind a policy, which entails deleting it.  To do this, click on the box to select the particular policy, and then click the "Delete" button on the upper right corner.  It will ask for confirmation if you wish to delete, which you should confirm.  Please note that this will not immediately delete the policy/regulation from the website; it will merely propose it for deletion so we can discuss.  So this is a "safe" action.



## Making Edits

Each page has five editable sections:
1. Code
2. Title
3. Kind
4. Reference
5. Content

### Code
Code refers to the policy number itself. This will always take the form of ####-##, or four-digit number, dash, then two-digit prefix, zero-padding as necessary.

So, 0403-50, or 1010-10 is good -- but 403.50 or 1010.1 is not.

The system does not check for duplication in advance, but will produce an error if you try to create a code for an already-existing policy.  And every policy needs a code, so figure that out before you create a new policy.

### Title
This should be a short, general, descriptive title about the content.

So, "Attendance", "Classified Personnel", and "Transportation" are all good titles.  Avoid long titles, and avoid punctuation (commas, parenthesis, dashes, ampersands, etc.)  **Do NOT** include slashes of any kind in the title.

### Kind
There are two kinds of documents:  "Policy" and "Regulation".  Just pick which this is from the drop-down.

### Reference
Reference can be anything, but mostly means referring to statute codes, IDAPA regulations, or other external references.

### Content
The Content refers to the substance of the policy/regulation itself.  This is where you can write free-form exactly what it is you're trying to accomplish.  There are two modes to writing, which you can toggle between using the switch on the upper right hand corner of the writing area.

The first is "Rich Text", which presents the content in the form in which it will be rendered (ie, WYSIWYG) and uses Microsoft Word-style buttons to create headings, bold, italics, lists, etc.  The is the default mode.  If you wish to switch to [Markdown](Markdown-Syntax.md), then click the "M" button on the upper right corner.  Feel free to use the mode with which you're most comfortable, or switch between them.

Regardless of method chosen, the content itself should follow certain conventions to ensure a consistent style.  See the [Style Guide](Style-Guide.md) for details.

## Saving Changes

Click the blue "Save" button to save changes.  You may be asked if you wish to "Send your changes for review".  To understand what this means, see [Publishing](Publishing-Workflow.md) below.


## Move on to Publishing
Now that you have an overview of the Editing Workflow, move on to [Publishing](Publishing-Workflow.md)
<!-- Commenting this out, as no one should do this near-term.

> Common Pattern: "Lift and Shift"
>
> As part of the overall Policy Review process, we frequently need to take existing policies and split them into two separate files: one for policy and one for the associated regulation.  We call this a "lift and shift".
>
> The first step in this process is to `Duplicate` the existing policy, change the Kind from `Policy` to `Regulation`, and then click Save.
>
> Next, you should edit the existing policy with new language consistent with the [Style Guide](Style-Guide.md).  If you're not sure what this new language should be, feel free to simply put in "TBD".  Then, click Save.
>
> This process is called a "lift-and-shift", and it results in two files (one Policy and one Regulation) with the same code, and both in Draft state that can then be worked on independently but will eventually be Published together.
-->
