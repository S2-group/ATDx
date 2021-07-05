Setting up the environment
---

Thank you for your interest in using the ATDx framework. With the help of Bachelor students and professors, we developed this 

## Requirements
This framework requires Python 3 along with MacOS or Linux.  Current and former contributors have used Ubuntu 18.04 and Ubuntu 20.04 along with Python 3.8

## Setting up environment and dependencies
### Local machine
1. Click on the **Fork** icon in the top right hand corner once you're logged into Github.
2. Once it finishes loading, click on the green **Code** button. Copy `git clone git@github.com:[your_username]/ATDx.git` and then paste that into your terminal after navigating to the desired local development environment.
3. Type `cd atdx` to enter the framework's main directory.
4. Install dependencies:
    1. For controller to work:
        - `pip install jsons`
        - `pip install pandas`
        - `pip install matplotlib`
        - `pip install ckwrap`
        - `pip install tabulate`
    
Now you can run it locally

### Server option
In the case that you want to run the server, steps from 1 to 4 are the same but in addition you have to:
4. Install extra dependencies:
    1. For running the server:
        - `pip install Flask`
        - `pip install GitHub-Flask`
    
5. You need to set the following variables in the Flask_server according to [Github authentication requirements](https://docs.github.com/en/rest/guides/basics-of-authentication):
    1. ```app.config['GITHUB_CLIENT_ID']```
    2. ```app.config['GITHUB_CLIENT_SECRET']```
    
6. Once this values have been set up, check that your server has a public ip and add it to the FlaskServer initialization:
    1. ``` app.run(debug=False, host="YOUR_IP_ADDRESS"")```
    
7. You can run the server but you need to log in because your account hasn't been validated yet:
    1. In your browser run: ```YOUR_IP_ADDRESS:5000/LOGIN```
    2. It will redirect your to a Github page where you need to enter your credentials
    
8. All set in the server side.

Now you need to set your repository to trigger the events and communicate it so to the ATDx tool. A detailed explanation can be found [here](https://docs.github.com/en/enterprise-server@3.0/developers/webhooks-and-events/webhooks/about-webhooks).

## Before You Begin
It's important for us to make sure that any updates to the framework add value and that the updates adhere to the original goals of the framework.  Before spending a lot of time making substantial changes, please raise an `issue` on Github so we're made aware of the changes you'd like to implement.  We'll provide feedback to inform you whether we think it's viable.

## Environment
Your forked repository will come with one branch, called `master`.  Create additional branches for experiments and/or development with `git branch branch_name`.  To update your forked repo with parent repo, `git checkout master` and type `git fetch upstream` followed by `git rebase upstream/master` so your local work is put on top of any changes made to the parent repo.  Note, this may mean you'll have to stash whatever you were working on.  In this case, `git stash save "message"` before `git checkout master`.  Once `master` has been updated, checkout the other branches to update with `git merge master`.  Then, `git stash pop stash@{#}` to continue working on changes.

## Making Changes to Your Forked Repo
### Commits
Any commits should contain logically similar changes.  Commit messages (`git commit -m "[text]"`) should be informative but also concise.  Good commits make changes easier to review later.  To limit the number of commits, use `git rebase` to squash the commits down to a more reasonable number.

## Submitting a Pull Request
Pull requests should be made from secondary branches (ie, not `master`).  Also make sure the branch is not behind in commits compared to master.  Any changes that need to be made while a pull request is still pending review should be made on a third branch to prevent polluting the pull request with other changes if they're not relevant.  

## Communication
The best way to communicate with the ATDx team is by raising an `issue` on Github or asking on Slack or Canvas.
