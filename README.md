# BLST Senior Design Project

## Install required packages

```
> pip install -r requirements.txt 
```

## Run tests

```
> python -m unittest discover -s tests
```

## Contributing

### Make an issue

For any work that needs to be done on the project make an issue describing the
what needs to be done and use tags to identify the type of work it is.

### Taking an issue

If you would like to work on an issue please assign it to yourself. Then create
a new local branch on your machine where you are going to work on the code and
make all your changes for the issue there.

### Writing a test

Every new function must have a test associated with it in the `/tests` directory
in the according file. If a file for the piece of code you are testing has not
been created then create one using the convetion `test_{module name}.py`.

### Submitting a change

Push your branch to the repo and then create a pull request. Assign
`ece-jacob-scott` as a reviewer. 

### Packaging the library

First step before uploading the library to pypi is to increment the version
number in the `setup.py` file.

Then, to allow the package to be distributed with our local pypi server you need
to first package it using `wheel`. To do this enter the command below, it should
create the folders `BLSTController.egg...`, `build`, and `dist`. These folders
contain the processed library and will allow pypi to distribute our library.

```
> python setup.py sdist bdist_wheel
```

Once all the source files are built you need to upload the source files to the
server using the command below (skip the first one if twine is already installed
). You will be prompted to enter credentials when uploading the files to the
server (contact Jacob or Austin for credentials). The skip existing flag is used
so that you only upload the most recent versions of the package and don't
overwrite existing versions on the server.

```
> pip install twine
> twine upload --skip-existing --repository-url https://pypi.austinbunker.com dist/*
```

Finally to install the library for another project just use the command below.

```
> pip install --index-url https://pypi.austinbunker.com BLSTController
```

## Code Structure

### Arduino Code

All code related to the Arduino lives in the Arduino folder and each sketch
has it's own folder.

### Python Code

Python code lives in the project root directory for now. Later if needed we can
move more modules to their own folders if the code requires a higher level of
organization.

### STL Files

The STL files for the footpedal live within the STL_Files folder. Each pedal is
the same so everything will need to be printed twice. The Pot_holder.stl is the 
part that holds the potentiometers for the pitch and roll axis so it will need to
be printed 4 times (two for each foot). The Full_Design.stl is the stl file that
shows the final configuration for one pedal.
