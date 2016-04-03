Twitter CLI Utility for Python
==============================
A simple command line utility written in Python to perform several Twitter operations. It is released under BSD 2-clause license.  

Requires [python-twitter](https://github.com/bear/python-twitter) (pip install python-twitter on most systems). settings.py or local_settings.py needs to contain valid Twitter OAuth keys. Twitter applications can be created and managed from [Twitter Apps](https://apps.twitter.com/) page.

Examples:

    $ ./twitter_cli.py -h
    usage: twitter_cli.py [-h]
                          
                          {lookup,post,follow,unfollow,reciprocate,followListMembers,listPendingFriends,listPendingFollowers}
                          ...

    positional arguments:
      {lookup,post,follow,unfollow,reciprocate,followListMembers,listPendingFriends,listPendingFollowers}
        lookup              Lookup users
        post                Post message
        follow              Follow users
        unfollow            Unfollow users
        reciprocate         Unfollow users that do not follow you
        followListMembers   Follow the members of a list
        listPendingFriends  Show pending Friendship requests
        listPendingFollowers
                            Show pending Follower requests

    optional arguments:
       -h, --help            show this help message and exit
    $

Lookup user details:

    $ ./twitter_cli.py lookup ilkertemir
    ilkertemir:
    ===========
      location: San Francisco Bay Area
      lang: en
      time_zone: Pacific Time (US & Canada)
      followers_count: 259
      [....]
    $

Post a message:

    $ ./twitter_cli.py post "Hello world."
    Message posted.
    $

Follow one or more users:

    $ ./twitter_cli.py follow ilkertemir newzsec
    Following user 'ilkertemir'.
    Following user 'newzsec'.
    $

Unfollow one or more user:

    $ ./twitter_cli.py unfollow ilkertemir 
    Unfollowing user 'ilkertemir'.
    $

Unfollow users who do not follow you back (with optional whitelist):

    $ ./twitter_cli.py reciprocate --whitelist ilkertemir
    You have 187 friends and 407 followers.
    1 whitelisted users.
    Unfollowing user id '2743874258'.
    User id 43869794 (ilkertemir) whitelisted.
    $

Follow the members of a list ([Ilker](https://www.ilkertemir.com/)'s [Top Security Influencers](https://twitter.com/IlkerTemir/lists/top-security-influencers) list in this example):

    $ ./twitter_cli.py followListMembers ilkertemir top-security-influencers
    ilkertemir/top-security-influencers has 100 members.
    Following user 'dotMudge'.
    Following user 'e_kaspersky'.
    Following user 'cBekrar'.
    [....]
    $
