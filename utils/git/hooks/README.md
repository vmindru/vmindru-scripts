# Client hooks

Use this client hooks to ensure your commits are consistent with 
personal standards. 


## pre-commit 

Ensure your commits provide proper author email e.g. mindruv@gmail.com


## commit-msg


Ensure your commits contain a JIRA key, this is needed for Jira/Github integration 
and for better traking of the work. e.g. PROJ-22 or RT-12


## Install 

#### Existing repo 

just copy commit-msg and pre-commit into your hooks dir e.g. 

__Note:__ assuming you are in the desired git repo , replace teh source accordingly  

```
cat commit-msg > $(git rev-parse --show-toplevel)/.git/hooks/commit-msg
cat pre-commit > $(git rev-parse --show-toplevel)/.git/hooks/pre-commit
chmod +x $(git rev-parse --show-toplevel)/.git/hooks/pre-commit
chmod +x $(git rev-parse --show-toplevel)/.git/hooks/commit-msg
``` 



#### Make sure this hooks are added to all your future created, cloned repos 
__Note:__  on various systems location of git-core/templates/hooks path will varry 
          .e.g.  Linux: /usr/share/git-core/templates/hooks adjust the prefix.
                 Biten Apple: /usr/local/share/git-core/templates/hooks 

```
cat commit-msg > /usr/share/git-core/templates/hooks/commit-msg
cat pre-commit > /usr/share/git-core/templates/hooks/pre-commit 
chmod +x /usr/share/git-core/templates/hooks/pre-commit 
chmod +x /usr/share/git-core/templates/hooks/commit-msg
```

### Populate alle existing repos 

__Note:__ Presuming you have all git  repos in the same place

``` find /home/vmindru/proj/git/ -name .git -exec cp /usr/share/git-core/templates/hooks/pre-commit {}/hooks/ \; ```

[
