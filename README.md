Twitter CLI Utility for Python
==============================
A simple command line utility written in Python to perform several Twitter operations. It is released under BSD 2-clause license.  

Requires [python-twitter](https://github.com/bear/python-twitter) (pip install python-twitter on most systems). settings.py or local_settings.py needs to contain valid Twitter OAuth keys. Twitter applications can be created and managed from [Twitter Apps](https://apps.twitter.com/) page.

Examples:

    $ ./twitter_cli.py -h
    usage: twitter_cli.py [-h] {follow,unfollow,reciprocity} ...

    positional arguments:
      {follow,unfollow,reciprocity}
        follow              Follow users
        unfollow            Unfollow users
        reciprocity         Unfollow users that do not follow you

    optional arguments:
      -h, --help            show this help message and exit

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

    $ ./twitter_cli.py reciprocity --whitelist ilkertemir
    You have 187 friends and 407 followers.
    1 whitelisted users.
    Unfollowing user id '2743874258'.
    User id 43869794 (ilkertemir) whitelisted.
    $
