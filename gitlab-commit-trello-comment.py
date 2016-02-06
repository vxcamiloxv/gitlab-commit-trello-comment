#!/usr/bin/python -tt
#
# Copyright (C) 2012 Shawn Sterling <shawn@systemtemplar.org>
# Copyright (C) 2013 Xiongfei(Alex) Guo <xfguo@credosemi.com>
# Copyright (C) 2016 Camilo QS <vxcamiloxv@openmailbox.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# gitlab-commit-trello-comment: a script which push gitlab commit to trello card comment.
# modify from gitlab-webhook-receiver: a script for gitlab & puppet integration
#
# The latest version of git will be found on:
# https://github.com/vxcamiloxv/gitlab-commit-trello-comment
#
# Fork from:
# https://github.com/xfguo/gitlab-commit-trello-comment
#
# The latest version of gitlab-webhook-receiver will be found on shawn-sterling's github page:
# https://github.com/shawn-sterling/gitlab-webhook-receiver

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import re
import sys
import json
import logging
import logging.handlers

from trolly import client as trolly_client
from trolly import board as trolly_board
from urlparse import urlsplit
from trolly import card

import config

import pprint

log = logging.getLogger('log')
log.setLevel(config.log_level)
log_handler = logging.handlers.RotatingFileHandler(config.log_file,
                                                   maxBytes=config.log_max_size,
                                                   backupCount=4)
f = logging.Formatter("%(asctime)s %(filename)s %(levelname)s %(message)s",
                      "%B %d %H:%M:%S")
log_handler.setFormatter(f)
log.addHandler(log_handler)

class webhookReceiver(BaseHTTPRequestHandler):
    def comment_to_trello(self, card_short_id, comment, board_id, board_name = ''):
        log.debug("Try comment on card #%d, [\n%s\n]" % (card_short_id, comment))
        trello_key = config.trello_key
        trello_token = config.trello_token

        client = trolly_client.Client(trello_key, user_auth_token = trello_token)
        board_class = None

        if board_name:
            for board in client.get_boards():
                board_information = board.get_board_information()
                if to_snakecase(board_information['name']) == to_snakecase(board_name):
                    log.debug("Change board to %s" % (board_name))
                    board_class = board;
                    break
        try:
            board = board_class or trolly_board.Board(client, board_id)
            card = board.get_card(str(card_short_id))
            result = card.add_comments(comment)
            log.debug("Success post comment in card #%d, [\n %s \n]" % (card_short_id, result['data']['text']))
        except:
            not_found = board_name or board_id
            log.debug("Board %s not found: %r" % (str(not_found), sys.exc_info()[0]))

    def do_POST(self):
        """
            receives post, handles it
        """
        log.debug('got post')
        self.rfile._sock.settimeout(5)
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        message = 'OK'
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.send_header("Content-length", str(len(message)))
        self.end_headers()
        self.wfile.write(message)
        log.debug('gitlab connection should be closed now.')

        # parse data
        post = json.loads(data_string)
        repo = post['repository']
        repo_name = repo['name']
        # got some urls
        repo_url = repo['homepage']
        branch = re.split('/', post['ref'])[-1]
        branch_url = repo_url + '/commits/%s' % branch
        board_id_path = self.path.replace('/', '')
        board_id = config.board_id
        if board_id_path:
            board_id = board_id_path

        log.debug(pprint.pformat(post))

        for commit in post['commits']:
            card_values_list = re.findall('#([0-9]+)\s+(\[.*?])?', commit['message'], flags=re.IGNORECASE)
            board_name_global = re.findall('(board|borad|@)(:?)(\s+)?\[(.*)]', commit['message'], flags=re.IGNORECASE)
            git_hash = commit['id'][:7]
            git_hash_url = commit['url']
            author = commit['author']['name']
            comment = commit['message']

            # Comment
            trello_comment = '''\[**%s** has a new commit about this card\]
\[commit: [%s](%s) | branch: [%s](%s) | repo: [%s](%s)\]
----
%s''' % (author, git_hash, git_hash_url, branch, branch_url, repo_name, repo_url, comment)
            for card_values in card_values_list:
                # Remove empty tuples
                card_values = filter(None, card_values)

                # Set card en board values
                card_short_id = int(card_values[0])
                board_name = ''

                if len(card_values) >= 2:
                    board_name = re.sub(r'\[|\]', '', card_values[1])
                elif len(board_name_global):
                    board_name = board_name_global[0][-1]

                self.comment_to_trello(card_short_id, trello_comment, board_id, board_name)

def to_snakecase(s):
    return re.sub("([\s])", "-", s).lower().lstrip("-")

def main():
    """
        the main event.
    """
    try:
        # Default values
        server_port = 9000
        server_name = ''
        if hasattr(config, 'server_port'):
            server_port = config.server_port
        if hasattr(config, 'server_name'):
            server_name = config.server_name
        # Run server
        server = HTTPServer((server_name, int(server_port)), webhookReceiver)
        msg_run = 'started web server...'
        log.info(msg_run)
        print(msg_run)
        server.serve_forever()
    except KeyboardInterrupt:
        msg_down = 'ctrl-c pressed, shutting down.'
        log.info(msg_down)
        print(msg_down)
        server.socket.close()

if __name__ == '__main__':
    main()
