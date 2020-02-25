# BLST Senior Design Project

## Install required packages

```
pip install -r requirements.txt 
```

## Run tests

```
python -m unittest discover -s tests
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

## Code Structure

### Arduino Code

All code related to the Arduino lives in the Arduino folder and each sketch
has it's own folder.

### Python Code

Python code lives in the project root directory for now. Later if needed we can
move more modules to their own folders if the code requires a higher level of
organization.