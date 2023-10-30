# [lansing-homeschool.github.io](https://lansing-homeschool.github.io)

A GitHub Pages site for sharing information about the Lansing Homeschool Hackers program, including FIRST LEGO League.

## Prerequisites

### RVM

If you don't already have Ruby installed, you might consider RVM, as it allows you to use different Ruby versions for different projects. Here are the steps to install it on Ubuntu:

```bash
sudo apt-get update
sudo apt-get install software-properties-common gpg build-essential zlib1g-dev -y
gpg --keyserver keyserver.ubuntu.com --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
curl -sSL https://get.rvm.io | bash -s stable --ruby
```

### Jekyll and Bundler

In order to run this locally, you will need to setup Jekyll. [Click here for instructions](https://jekyllrb.com/docs/installation/) or use the following for Ubuntu:

```bash
gem install jekyll bundler
```

### Bundled Gems

Before starting the local Jekyll the first time you need to run the following from this directory:

```powershell
bundle install
```

## Running locally

To start Jekyll, you can run the following:

```powershell
bundle exec jekyll serve
```

With Jekyll running, you can view the site at [http://localhost:4000](http://localhost:4000).

## Upgrading Ruby Gems

In order to upgrade the Ruby Gems used by Jekyll, run the following:

```powershell
bundle update
```

## Comments

The site uses Disqus for comments. All comments must be approved.

## Contributing

Fork the repo and then create a PR
