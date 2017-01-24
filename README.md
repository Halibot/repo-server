Package repository server
=========================

This is a server for halibot packages.

Usage
-----

```
cp default.repo.json repo.json # The repo.json specifies what packages to serve
python main.py update          # Pulls the specified packages down and packages them for serving
python main.py serve           # Runs the server
```
