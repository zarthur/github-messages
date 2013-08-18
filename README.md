github-messages
===============
Represent short (24 or less characters) messages with a 3x3 font and display
them in the github activity chart.

This might be timezone dependent; so while it might look correct
to you, it could look weird to someone in a different timezone.


## How to use
First, create a new GitHub account (don't want existing commit history
interfering with the message) and a new repo.  Next, either add your usual user
as a collaborator or create new SSH keys for the new GitHub account.  Create a
config file with the correct settings.  Finally, run

    python3 github.py PATH_TO_CONFIG AWESOME_MESSAGE


## Requirements
- numpy
- matplotlib (optional)


## Examples
### matplotlib
Entering the following at the command line will generate a preview, as shown
below, in matplotlib.

    python3 preview.py This is a test message.

![matplotlib image](https://raw.github.com/zarthur/github-messages/master/images/test_message.png)

### GitHub
After setting up a GitHub account and updating the config file, running

    python3 github.py config.yml "This is a test message."

produced this:

![github image](https://raw.github.com/zarthur/github-messages/master/images/github.png)


## Sources
- [3x3 Font](http://www.norwegianink.com), [More](http://www.dafont.com/3x3-font-for-nerds.font)
- [Python function to find next specified weekday after a given date](http://stackoverflow.com/questions/6558535/python-find-the-date-for-the-first-monday-after-a-given-a-date)


## License
Copyright © 2013 Arthur Neuman <<arthur.neuman@gmail.com>>

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
<http://www.wtfpl.net/> for more details.

