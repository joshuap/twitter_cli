#!/usr/bin/python
'''
Copyright (c) 2016, Ilker Temir
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import sys
import argparse
import twitter
from settings import *

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')
parser_follow = subparsers.add_parser('follow', help='Follow users')
parser_follow.add_argument('user',nargs='+')
parser_unfollow = subparsers.add_parser('unfollow', help='Unfollow users')
parser_unfollow.add_argument('user',nargs='+')
parser_reciprocity =  subparsers.add_parser('reciprocity',
                                            help='Unfollow users that do not follow you')
parser_reciprocity.add_argument('--whitelist', metavar='user', nargs='+',
                                help='Whitelist users')
cli_options = parser.parse_args()

try:
    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET)
except twitter.TwitterError, e:
    print "Cannot initialize Twitter (%s)" % str(e)
    sys.exit(1)

if cli_options.command == 'follow':
    for user in cli_options.user:
        try:
            api.CreateFriendship(screen_name=user)
            print "Following user '%s'." % user
        except twitter.TwitterError, e:
            print "Error following user '%s' (%s)" % (user, str(e))
elif cli_options.command == 'unfollow':
    for user in cli_options.user:
        try:
            api.DestroyFriendship(screen_name=user)
            print "Unfollowing user '%s'." % user
        except twitter.TwitterError, e:
            print "Error unfollowing user '%s' (%s')" % (user, str(e))
elif cli_options.command == 'reciprocity':
    friend_ids = api.GetFriendIDs()
    follower_ids = api.GetFollowerIDs()
    print "You have %d friends and %d followers." % (len(friend_ids), len(follower_ids))
    whitelisted_user_ids = {}
    for user in cli_options.whitelist:
        try:
            user_id = api.GetUser(screen_name=user).id    
            whitelisted_user_ids[user_id]=user
        except twitter.TwitterError, e:
            print "Error looking up user '%s' (%s)" % (user, str(e))
    if whitelisted_user_ids:
        print "%d whitelisted users." % len(whitelisted_user_ids)
    for user_id in friend_ids:
        if user_id in whitelisted_user_ids:
            print "User id %d (%s) whitelisted." % (user_id, whitelisted_user_ids[user_id])
        if user_id not in follower_ids:
            try:
                api.DestroyFriendship(user_id=user_id)
                print "Unfollowing user id '%d'." % user_id
            except twitter.TwitterError, e:
                print "Error unfollowing user id '%d' (%s')" % (user_id, str(e))            
    
