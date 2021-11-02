# Build, package and release

Remember to bump the version number in `setup.py`, then run:

```
python -m build
```

You can install the locally built version with:

```
python3 -m pip install dist/pins-0.1.1.tar.gz
```

And then, when you're happy, upload with:

```
python3 -m twine upload dist/pins-0.1.3*
```

This information is mostly distilled from the
[official docs](https://packaging.python.org/tutorials/packaging-projects/).

