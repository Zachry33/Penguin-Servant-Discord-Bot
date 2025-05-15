## **Penguin Servant Discord Bot**

This is a simple Discord bot built using Python and discord.py that manages user roles and provides basic interactions in a server. 

The bot supports:

-   Welcoming new members

-   Rolling random numbers

-   Managing a silencing system for "Bad Boys"

## Features
- Automatic Role Setup: Ensures "Penguin Owner" and "Bad Boy" roles exist when the bot starts.

- Welcome Message: Sends a DM to users when they join the server.

- Command: !roll: Returns a random number between 0 and 100.

- Command: !silence <username>: Assigns the "Bad Boy" role, optionally mutes them and changes their nickname (admin-only).

- Command: !unsilence <username>: Removes the "Bad Boy" role and unmutes the user (admin-only).
