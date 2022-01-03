# Development Notes

This project has been ported to and currently maintained using [JupyterBook](https://jupyterbook.org/intro.html).

After completing routine edits to notebooks, data, or configuration files, open a terminal window and navigate to the directory of the local git repository. 

```
jupyterbuild clean ../cbe30338-book
```

Rebuild the book by executing the following command from the terminal window while 

```
jupyterbuild build ../cbe30338-book
```

Commit and push changes to the remote git repository.

```
git add --all
git commit -m "commit message"
git push
```

Move relevant html files to github pages.

```
ghp-import -n -p -f _build/html
```