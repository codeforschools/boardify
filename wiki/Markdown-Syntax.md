## **Markdown** is nothing more than a *plain text files* which use a particular *syntax* for *stylistic presentation*.  

What I mean by:

### Plain Text Files
Plain text files are best understood in comparison to application-specific files (such as Microsoft Word).  Application-specific files can only be read by their parent application (or through the use of converters).  This means that the files are stored in binary format, which if you opened it would look something like this:

```
504b 0304 1400 0600 0800 0000 2100 007b
9e36 8801 0000 5b06 0000 1300 0802 5b43
6f6e 7465 6e74 5f54 7970 6573 5d2e 786d
6c20 a204 0228 a000 0200 0000 0000 0000
```

This is something only a computer can understand. In contrast, a plain text file are just letters and numbers that any application can open and understand.  But plain text files are, well, plain.  There are no things like Bold, Titles, Italics, Bullet Points, etc.  That's where the Markdown syntax comes in.

### Markdown Syntax
The Markdown syntax is a set of conventions that allow for plain text files to convey additional meaning and be human readable without special applications.  The easiest way to show this is through demonstration:

If you, for instance, use double-stars before and after some words, that is considered strong emphasis.  Such as:

```
These are some **strong emphasis** words
```

And while this is perfectly readable and understandable, it does lead to the final aspect of Markdown, which leads to stylistic presentation.

### Stylistic Presentation
By following the same conventions, other programs can then take those easily-readable Markdown files and turn them into web pages, PDFs, or even high-level applications (such as Microsoft Word).  And so now when I write:

These are some **strong emphasis** words.

You'll notice that this website has made `strong emphasis` bold automatically.  And it's not just bold; an entire set of conventions are available to do all sorts of more advanced formatting, up to and including really complicated things like linking, advanced math, tables, and more.  For a better demonstration of this, see this [Github Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) website.  

## Summary
This is the problem Markdown was created to solve: simple, portable, human-readable plain text files that can also be shared and printed in multiple formats with full stylistic control.