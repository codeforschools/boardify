# Components

Here are the components that are used by the site:

## [Markdown](https://www.markdownguide.org)
Markdown is a **syntax**.  It is a convention for writing files in plain-text that is designed to be human-readable, but which computers also know how to turn into websites.

## [Github](https://www.github.com)
Github is a cloud-based service that stores and manages files under version control.  It provides a number of features for editing, tracking changes, and project management as well as hosting of the website itself.

## [Zensical](https://zensical.org)
Zensical is Static Site Generator, or SSG.  It takes files that are written in the Markdown syntax and builds them into HTML so that they can become a website on the internet.

## [Sveltia](https://sveltiacms.app)
Sveltia is a Content Management System, or CMS.  This provides a private interface designed for internal use that allows content creators to write and manage files that use familiar tools, saving the output as Markdown automatically.

Here is a more expansive explanation each tool’s function:

### Markdown
Typically we write files using proprietary software such as Microsoft Word.  Formatting such as Bold, Italic, Underling, Titles, etc., are put into place by selecting text and clicking buttons.  The software then translates those button clicks into what we want to see, which is saved in the file as a set of internal instructions only available to that particular software.  

In contrast, Markdown is just plain text.  There are no “secret” instructions unique to that software program.  Instead, Markdown is a set of simple conventions that are well-known by other computers, software and intuitively readable by humans.  Generally speaking, a person totally unfamiliar with Markdown itself should be able to read the content of a Markdown file and not only process the words themselves, but also understand formatting context such as bold, italics, sections, lists, etc.

For instance, when we want to emphasis a word, we surround it in asterisks.  This accomplishes two things:

1. When reading in plain text, humans know that the word `*asterisks*` has added emphasis without needing to see the italics themselves.  
2. Computers also know what this means and so if we wanted to print it, save it as a PDF, render into a webpage, etc., then it removes the asterisks and presents the worked *asterisks* with italics (or bold, underline, etc.) accordingly.

Markdown can do most everything a proprietary software like Word can do, including headings, bullet lists, tables, equations, images, etc., in any text editor application.  Moreover, there are a variety of applications that produce Markdown using all the same buttons and keystrokes to which a user has become accustomed.

> To see this in action, try [Dillinger](https://dillinger.io), which is a free Markdown editor that is entirely online. Other popular desktop and mobile applications include [Obsidian](https://obsidian.md), [Typora](https://typora.io), [IA Writer](https://ia.net/writer) -- or simply search online for “Markdown Editor” and try them all.  


### Github

GitHub is a service that hosts version-controlled file storage.  Version Control is just like it sounds: it tracks changes in files through time, and keeps a record of each version for future use.  The underlying engine that does this is open-source software called `[Git](https://git-scm.com)`, and GitHub is one popular Git-as-a-Service provider.  Git was developed to help manage computer code, which is its primary use-case today, but can manage any files that are text-based.

When we make duplicates of Word files and then send those edits via email with one person accepting or modifying those changes, we are effectively doing version control.  However, using this approach means that we have to do a lot of manual processing with a great deal of mental juggling on whose edits should be accepted, where they should be sent, and when they are valid -- along with the additional challenges of managing software incompatibilities between various platforms and applications.

In contrast, GitHub was designed specifically to track and manage changes in distributed systems.  And while GitHub can track all sorts of files (including PDFs, Word documents, Images, etc.) it works best with plain text in general, and knows how to format Markdown specifically.  This is why using Markdown is important; it allows access to this suite of open-source and widely available tools that otherwise are inaccessible to proprietary software approaches like Word or Simbli.

Your organization has a GitHub organization, and all the files related to this app are kept in a content repository there.


### Zensical

Zensical is an open-source Static-Site Generator, or SSG.  This is a tool that takes the plain-text files written in Markdown syntax and converts them into HTML, or the language of websites.  These converted HTML files can then be uploaded to the internet where they can be served to the public at large.  

Zensical is tailored towards documentation, which is the closest proxy to our policies that I can envision.  It provides a clean, easy-to-understand interface and allows for rapid searching and easy formatting.  But there are others freely available should a different tool prove more useful.

In addition to creating HTML, Zensical also does some heavy-lifting like site-security, searching, internationalization, and accessibility.  Zensical specifically adheres to the [Web Content Accessibility Guidelines](https://en.wikipedia.org/wiki/Web_Content_Accessibility_Guidelines) Version 2, standard AA -- the standard to which public school district websites are held.

### Sveltia

Sveltia is a headless Content Management System, or CMS.  Content Management Systems are designed to do just that: provide a way to manage the creation, deletion, modification and organization of content.  They have straightforward, familiar tools to format documents (similar to how the Word application creates Word docs), and also can provide additional tools for editorial and organization control and management.  They are designed for admins and moderators, and are generally private, internally-facing and password-protected.

The "headless" portion means that Sveltia is fully decoupled from the greater system, and can be used with different providers, syntax, or SSGs -- avoiding vendor lock-in.  This is in contrast to other CMS systems like WordPress or Simbli, which are all-in-one solutions that are full-service but also do not allow for flexibility or portability.

## Understanding the Underlying System

> You can safely ignore this section unless you want to know a bit about what happens under the hood.

The core workflow of the Boardify system depends on a Version Control system called Git.  As the name suggests, Version Control tracks file changes through time, and can go back to any earlier version at any time.  This means we handle documents in a slightly different way than on a file system using an application like Word, and can be a bit counter-intuitive.

To explain a bit more, When you update, create, or delete a particular file (ie, a policy or regulation) in Boardify, every time you save a change you make a copy of the document automatically and log that transaction in the system.  Think of it like creating a copy of a Word Document that you call "Policy Edits V2" with your individual changes, which you then might send back to the original author or to a group of people.  But in Boardify there is only one file that everyone works on at the same time, and every change from every person at every moment through time is tracked and logged, automatically.

So then rather than manage multiple versions of a file saved on a drive or passed around email, there is one and only one canonical version of a policy that is either Updated, Created, or Deleted.  (You can also rename a file, which is a special case but the computer thinks of as "Create and Delete at the same time".)

Most of these details are hidden from the Decap CMS front-end, but everything is accessible from GitHub, which is the hosting provider for the Git version control system that we use.  More on this, in [Project-Management](Project-Management.md)

## Summary

With these four tools (Markdown, GitHub, Zensical and Sveltia) we can replace all our current functionality using a better, more comprehensive workflow, include rich history, and do more with the resulting content than we currently do.  It will require some changes in how we write the policies and think about the flow, but overall will be in a much better position for ourselves, the administration and our patrons.

Oh, and did I mention all of these tools are free?  :-)
