# Capstone Project

## About

This project combines LDA topic modelling and sentiment analysis to analyze the change in sentiment an author has towards a topic in a corpus.

## Bugs and suggestions

If you would like to report a software bug, make a suggestion on how we can improve the app, or have any other requests, feel free to create an issue on the James github under the Issues tab.

## Running James Locally

If you want to run James on your local machine, checkout the dev branch with:

```code
git checkout dev
```

## Front End

- Written in JavaScript with React

### Requirements

- Node
- NPM

### Usage

From the root:

- move into the ui folder with:

```code
cd ui
```

- install dependencies with:

```code
npm i
```

- start ui wth:

```code
npm start
```

- ui can also be started from root with:
```code
npm start --prefix ui
```

## Back End

- Written in python with flask

### Requirements

- python3
- pip3
- java
- git

### Usage

From the root:

- install requirements with:

```code
pip3 install -r api/requirements.txt
```

- run setup with:

```code
python3 api/setup.py
```

- start server with:

```code
python3 api/server.py
```

If you're encountering errors running the backend, try running the following commands:

```
python3 -c "import nltk;nltk.download('averaged_perceptron_tagger');nltk.download('wordnet')"
```
