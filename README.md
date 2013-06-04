github-messages
===============
Represent short (24 or less characters) messages with a 3x3 font and display
them in the github activity chart.

Currently, only previewing the message with matplotlib in the 3x3 font works;
github commit functionality to be added soonish.

Requirements
----
- numpy
- matplotlib (optional)


License
----
Copyright © 2013 Arthur Neuman <<arthur.neuman@gmail.com>>

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
<http://www.wtfpl.net/> for more details.

Example
----
Entering the following at the command line will generate a preview, as shown
below, in matplotlib.

    python3 preview.py this is a test message

![matplotlib image](https://raw.github.com/zarthur/github-messages/master/images/test_message.png)

Sources
----

- 3x3 Font
  - http://www.norwegianink.com/
  - http://www.dafont.com/3x3-font-for-nerds.font
