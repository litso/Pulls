# Pulls
Provides Github Pull Request Metadata in Various Formats

# Setup

## Setup Python 3.8

### Install Pyenv

```
brew update && brew upgrade pyenv
# Will install correct version of python specified in .python-version
pyenv install
```

## Create the Virtual Environment

Create the environment
```
python3 -m venv env
```

And Activate It

```
# Bash or ZSH
source env/bin/activate

# or Fish
. env/bin/activate.fish
```

# Running

## Add Github Token to AWS Systems Manager

Open the parameter store and add the value as a secure string. Use the default KMS Key ID.
Name the value `github-api-key`

For more information see [Approach #1](https://www.serverless.com/blog/aws-secrets-management)

## Invoke Locally

Ignore the warning about ssm not configured since we are running locally

```
sls invoke local --function main --verbose --path events/get-event.json --env GITHUB_API_KEY=123
```