# SARCE - State Aware Remote Command Execution

## Overview

This package provides a thin layer on top of fabric to execute commands with a state like
- current working directory 
- activated virtual environment

## Motivation

The package is mainly intended to facilitate deployment tasks (eg. for django apps) by running a simple python script.
Compared to configuration management tools like Ansible this approach is far less powerful and scalable.
However, it might be easier to understand for developers and thus lowering the hurdle to deploy applications by them selves.
