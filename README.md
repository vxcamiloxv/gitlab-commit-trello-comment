# Introduction

gitlab-commit-trello-comment will monitor your gitlab commit with card number(like #234) and push a format comment to that card of your trello board.
modified from gitlab-webhook-receiver project.

You can set the board  in the following ways:

- config.py with: board_id = 'HhKy35Jh'
- hook url with: https://your.ip.hook.here:9000/borad_id
- commit with:
  + Board by card and #236 get baord_id from config.py or hook url
    ```
    "Fix #234 [My Project] #235 [My Other Project] #236"
    ```
  + #235 and #236 cards inherited same board
    ```
    "Fix #234 [My Other project] #235 #236 @[My Project]"
    ```

gitlab-webhook-receiver is a script to receive http posts from gitlab and then
pull the latest branches from a git repo.

# Dependencies

Before getting stated you will need install [Trolly](https://github.com/plish/Trolly) and httplib2 (reqired by trolly).
```
    pip install trolly httplib2
```
or
```
    pip install -r requirements.txt
```


# License

gitlab-commit-trello-comment is released under the [GPL v2](http://www.gnu.org/licenses/gpl-2.0.html).

# Documentation

(1) Modify the script
---------------------

Copy the config.py.sample to config.py and fill your gitlab and trello info.

###`trello_key`
https://trello.com/1/appKey/generate

###`trello_token`
This is not so well explained in Trello, but I understood that you need to authorize the app with `trello_key` to access each board separatelly. To do that:

https://trello.com/1/authorize?response_type=token&name=[BOARD+NAME+AS+SHOWN+IN+URL]&scope=read,write&expiration=never&key=[YOUR+trello_key+HERE]

where [YOUR+trello_key+HERE] is the one you entered in the previous step, while [BOARD+NAME+AS...] is, well, what it says. If your board url is

https://trello.com/b/XLvlTFVA/my-project

then you should type in "my-project".

###`board_id`
It is the end of the URL when viewing the board. For example, for https://trello.com/b/XLvlTFVA/my-project, `board_id` is XLvlTFVA.

###`list_progress`
Name of list to move card if not have words like 'close' or 'fix'.

###`list_done`
Name of list to move card if have words like **'close' or 'fix'** regardless of whether is uppercase or lowercase .

(2) create the gitlab webhook
-----------------------------

In gitlab, as admin, go to "Hooks" tab, create hook as: http://your.ip.hook.here:9000

or change the **'port'** in config.py

(3) Optional init script
------------------------

remember to edit the script if any of your directories were changed.

# Bugs

Let me know what's happening and I'll try to help
Please open [issues](https://github.com/vxcamiloxv/gitlab-commit-trello-comment/issues).


# Contributing
All [pull request](https://github.com/vxcamiloxv/gitlab-commit-trello-comment/pulls) are welcome.
