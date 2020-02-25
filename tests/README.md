# Testing

## Description

This project uses the `unittest` module which comes standard with python. Every
module of this project should have every function tested for stability. The goal
is to have 100% test coverage. That is to say that every piece of code in the
library has at least a few tests written for it.

## Run all the tests

```
python -m unittest discover -s tests
```

## Responsibility

As a developer on this library it is your job to write tests to prove to other
developers that your code is good for the ecosystem of the project. A PR has a
much smaller chance of getting merged if there are no tests written for it and
all tests will be run on the requested branch before the PR is accepted. 