# Introduction

gitlab-commit-trello-comment will monitor your gitlab commit with card number(like #234) and push a format comment to that card of your trello board.
modified from gitlab-webhook-receiver project.

You can set the board  in the following ways
- config.py with: board_id = 'HhKy35Jh'
- hook url with: https://your.ip.hook.here:9000/borad_id
- commit with:
  + "Fix #234 [My Project] #235 [My Other Project] #236" -> Board by card and #236 get baord_id from config.py or hook url
  + "Fix #234 [My Other project] #235 #236 @[My Project]" -> #235 and #236 cards inherited same board and

gitlab-webhook-receiver is a script to receive http posts from gitlab and then
pull the latest branches from a git repo.

# Dependencies

Before getting stated you will need install [Trolly](https://github.com/plish/Trolly) and httplib2 (reqired by trolly).

    pip install trolly httplib2

or

    pip install -r requirements.txt


# License

gitlab-commit-trello-comment is released under the [GPL v2](http://www.gnu.org/licenses/gpl-2.0.html).

# Documentation

(1) Modify the script
---------------------

Copy the config.py.sample to config.py and fill your gitlab and trello info.

(2) create the gitlab webhook
-----------------------------

In gitlab, as admin, go to "Hooks" tab, create hook as: http://your.ip.hook.here:9000

or change the port in config.py

(3) Optional init script
------------------------

remember to edit the script if any of your directories were changed.

# Bugs

Let me know what's happening and I'll try to help
Please open [issues](https://github.com/vxcamiloxv/gitlab-commit-trello-comment/issues).


# Contributing
All [pull request](https://github.com/vxcamiloxv/gitlab-commit-trello-comment/pulls) are welcome.
