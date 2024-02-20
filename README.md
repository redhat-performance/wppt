# Overview

wppt provides an easy way to intercept, manage, manipulate and re-send a webhook to any Rest API or incoming webhook service (like JIRA).

# Why Is This Needed?

Some services/platforms don't provide an easy-to-use integration vehicle for transforming and syncing requests, payloads and automation e.g. Gitlab -> Jira. Instead of paying for an expensive third-party service to provide integrations you can do this easily yourself on-premise.

# How To Use wppt?

Fill me in.

[![Unix Build Status](https://img.shields.io/github/actions/workflow/status/grafuls/wppt/main.yml?branch=main&label=linux)](https://github.com/grafuls/wppt/actions)
[![Windows Build Status](https://img.shields.io/appveyor/ci/grafuls/wppt.svg?label=windows)](https://ci.appveyor.com/project/grafuls/wppt)
[![Coverage Status](https://img.shields.io/codecov/c/gh/grafuls/wppt)](https://codecov.io/gh/grafuls/wppt)
[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/grafuls/wppt.svg)](https://scrutinizer-ci.com/g/grafuls/wppt)
[![PyPI License](https://img.shields.io/pypi/l/wppt.svg)](https://pypi.org/project/wppt)
[![PyPI Version](https://img.shields.io/pypi/v/wppt.svg)](https://pypi.org/project/wppt)
[![PyPI Downloads](https://img.shields.io/pypi/dm/wppt.svg?color=orange)](https://pypistats.org/packages/wppt)

## Setup

### Requirements

* Python 3.11+

### Installation

Install it directly into an activated virtual environment:

```text
$ pip install wppt
```

or add it to your [Poetry](https://poetry.eustace.io/) project:

```text
$ poetry add wppt
```

## Usage

After installation, the package can be imported:

```text
$ python
>>> import wppt
>>> wppt.__version__
```
