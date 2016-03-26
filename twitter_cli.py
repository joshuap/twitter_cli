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
parser_lookup = subparsers.add_parser('lookup', help='Lookup users')
parser_lookup.add_argument('user',nargs='+')
parser_follow = subparsers.add_parser('follow', help='Follow users')
parser_follow.add_argument('user',nargs='+')
parser_unfollow = subparsers.add_parser('unfollow', help='Unfollow users')
parser_unfollow.add_argument('user',nargs='+')
parser_reciprocate =  subparsers.add_parser('reciprocate',
                                            help='Unfollow users that do not follow you')
parser_reciprocate.add_argument('--whitelist', metavar='user', nargs='+',
                                help='Whitelist users',default='')
parser_followListMembers = subparsers.add_parser('followListMembers',
                                                 help='Follow the members of a list')
parser_followListMembers.add_argument('username', help='User owning the list')
parser_followListMembers.add_argument('listname', help='Name of the list (slug)')

cli_options = parser.parse_args()

try:
    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET)

except twitter.TwitterError, e:
    print "Cannot initialize Twitter (%s)" % str(e)
    sys.exit(1)

if cli_options.command == 'lookup':
    for user in cli_options.user:
        try:
            user_details = api.GetUser(screen_name=user).__dict__
            print "%s:" % user
            print "=" * (len(user)+1)
            for key in user_details:
                if key == '_status':
                    status = user_details[key]
                    if status:
                        print "  Status:"
                        status = status.__dict__ 
                        for item in status:
                            print "     %s: %s" % (item[1:len(key)], status[item])
                else:
                    print "  %s: %s" % (key[1:len(key)], user_details[key])

        except twitter.TwitterError, e:
            print "Error looking up user '%s' (%s)" % (user, str(e))

elif cli_options.command == 'follow':
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

elif cli_options.command == 'reciprocate':
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
                print "Error unfollowing user id %d ('%s')" % (user_id, str(e))            

elif cli_options.command == 'followListMembers':
    try:
        members = api.GetListMembers(list_id=None,
                                     owner_screen_name=cli_options.username,
                                     slug=cli_options.listname)
    except twitter.TwitterError, e:
        print "Error getting list %s/%s" % (cli_options.username, cli_options.listname)
        sys.exit() 

    print "%s/%s has %d members." % (cli_options.username,
                                     cli_options.listname, 
                                     len(members))

    for member in members:
        try:
            api.CreateFriendship(screen_name=member.screen_name)
            print "Following user '%s'." % member.screen_name

        except twitter.TwitterError, e:
            print "Error following user '%s' (%s)" % (member.screen_name, str(e))
    
