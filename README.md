# HouseBot
HouseBot is a simple personal Discord bot written for my house.

## Features
This is a list of all current and planned features for HouseBot.
- [x] Polls
- [ ] HUE Light Control
- [ ] Nest Control
- [ ] Ping a particular roommate whenever *any* roommate is pinged

## Installation
Running HouseBot requires a bot user created through the Discord Developer Portal. After the bot has been created and is in your server:
1. Close this repo to your system.
2. Setup the BOT_TOKEN environment variable, providing the token given to you when you created the bot user.
3. Run `.\main.py --setuponly` for first-time setup.
4. Run `.\main.py`

The bot should now be running and will shortly show up as online in your server.

## Usage
### Commands
The bot has the following commands implemented, each of which can be run by mentioning the bot in your server.
#### Poll CommandGroup
- `poll create title *options` (ex. @HouseBot poll create "My Poll" "Option 1" "Option 2")
- `poll close id` (ex. @HouseBot poll close 14)
#### Standalone Commands
- `roll roll_syntax [count]` (ex. @HouseBot roll 2d4kh1)

## Contributing
If you've got an improvement, feel free to open a PR. All I ask is that you do your best to stick with the existing style.

Here are a few common possible additions

### Adding a new Command
There are two levels to the command interface in HouseBot. The first are CommandGroup objects, which group related commands under the same command prefix. For example, we have the "poll" CommandGroup, which contains "create" and "close" Commands. Calling the former is done as "poll create".

When creating a new CommandGroup, add a new file under `bot/commands`.

In that file, you will first create your CommandGroup object like `command_group = CommandGroup("MyCommandGroup")`

Then you can define classes that are your individual Command objects. The Command constructor takes the name of the Command as its first argument. You can also set the Command as admin-only by passing in `admin=True`. Within your Command object's constructor, you will define your Command arguments, and add them to the command using `self.add_arg(command_arg)`. The CommandArg object is just a wrapper for argparse arguments, and takes all of the same parameters, which you can read more about [here](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument).

Finally, with your Command defined, add it to the CommandGroup at the bottom of the file with `command_group.add_command(MyCommand())`.

As a note, CommandGroup objects can have other CommandGroup objects nested inside of them. Both CommandGroup and Command objects are sub-classes of CommandHandler. 

### Listening to a new kind of Discord event
This bot uses Discord.py, whose events are listed [here](https://discordpy.readthedocs.io/en/stable/api.html#event-reference). We subclass discord.Client, and so we override all event functions that we want to listen to in `bot/discordclient.py`. Their documentation details all parameters that the event will receive.

### Adding a new database interaction
Currently, all database interactions live in `database/databaseinterface.py`

You'll see there that most interactions follow the same format:
1. A command string using the named placeholder (:name) format described [here](https://docs.python.org/3/library/sqlite3.html#sqlite3-placeholders).
2. A dictionary holding the data to be placed in the command string.
3. An execute wrapped in a try-except and with statement.
   1. The try-execpt should be obvious, in order to catch any SQL errors.
   2. The with statement allows the SQL connection object to handle commits and rollbacks for us.

Here's a simple example from the code:
```python
def get_poll_by_id(self, poll_id) -> sqlite3.Row:
    get_cmd = "SELECT * FROM polls WHERE poll_id = :poll_id"
    data = {"poll_id": poll_id}
    result = None

    try:
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(get_cmd, data)
            result = cursor.fetchone()
    except sqlite3.DatabaseError:
        print("ERROR: Failed to retrieve poll")

    return result
```

## License
[MIT](https://choosealicense.com/licenses/mit/)