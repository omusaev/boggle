# Overview
Implementation of famous Boggle game (https://en.wikipedia.org/wiki/Boggle)

# Installation
The app is Docker friendly, so here we go:

Development environment with live reload:
```bash
$ cd deploy/docker-compose
$ docker-compose -f docker-compose.dev.yml up
```

Production environment:
```bash
$ cd deploy/docker-compose
$ docker-compose -f docker-compose.prod.yml up
```

# Tests
```bash
$ cd deploy/docker-compose
$ docker-compose -f docker-compose.test.yml up
```