# Wppt
#### Webhook Payload Proxy Transformer
![wppt](/assets/whippet.png?raw=true)
[![Unix Build Status](https://img.shields.io/github/actions/workflow/status/grafuls/wppt/main.yml?branch=main&label=linux)](https://github.com/grafuls/wppt/actions)
[![Coverage Status](https://img.shields.io/codecov/c/gh/grafuls/wppt)](https://codecov.io/gh/grafuls/wppt)

## Overview

Wppt(Pronounced: [ˈwɪpɪt]) provides an easy way to intercept, manage, manipulate and re-send a webhook/API call to any Rest API or incoming webhook service (like JIRA).

## Why Is This Needed?

Some services/platforms don't provide an easy-to-use integration vehicle for transforming and syncing requests, payloads and automation e.g. Gitlab -> Jira. Instead of paying for an expensive third-party service to provide integrations you can do this easily yourself on-premise.

## How Does `wppt` Work?

 Wppt leverages Flask dynamic routing. The endpoint is variable and defined via one or multiple yaml files. 
 Based on the endpoint url, `wppt` parses all the yaml files stored on the `transformers` directory, and retrieves the outgoing webhook url and the translations. It then parses all the translations and converts the existing data from the incoming webhook into a new payload structure as defined on the yaml.

### Example:

```yaml
gitlab2jira:
  enabled: true
  target_webhook: https://example.com/rest/cb-automation/latest/hooks/{JIRA_WEBHOOK_ID}
  translations:
    data:
      name: '[{data[project][name]}][{data[object_kind]}] {data[object_attributes][title]}'
      description: 'Description: {data[object_attributes][description]}\nURL:{data[object_attributes][url]}'
```

Given the following incoming webhook payload to `http://{FQDN}:5005/gitlab2jira/`:
```json
{
    "project":{"name":"landing"}, 
    "object_kind":"story", 
    "object_attributes":{
        "title": "Issue with", 
        "description":"Short description here", 
        "url": "SITE HERE"
    }
}
```

`wppt` will then send and HTTP post request to `target_webhook` with the following payload:
```json
{
    "data": {
        "name": "[landing][story] Issue with", 
        "description": "Description: Short description here\\nURL:SITE HERE"
    }
}
```

## Requirements

* Python 3.11+
* Flask
* requests

## Installation

Install it directly into a poetry virtual environment:

```bash
$ git clone https://github.com/redhat-performance/wppt
$ cd wppt
$ make install
```

## Usage

After installation, the server can be started with:

```bash
$ make run
```

### Via Podman

#### Building the image
```bash
$ cd docker
$ podman build -t wppt .
```

#### Running
```bash
$ podman run -it --rm -v /path/to/local/transformers/:/opt/wppt/transformers -p 5005:5005 wppt
```

