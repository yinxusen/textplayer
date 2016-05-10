
# text-player

This code provides an interface for running text-based games using Frotz.

Keep in mind that if there is more than one instance of Frotz running, there are no guarantees it will work.

## Requirements

The only requirement aside from this source code is Frotz, a Z-Machine interpreter written by Stefan Jokisch in 1995-1997. More information [here](http://frotz.sourceforge.net/).

```bash
$ sudo apt-get install frotz
```

## Usage

This code is set up to run in python. Example commands are below.

```python
t = TextPlayer('zork1.z5', False)
start_info = t.run()
command_output = t.execute_command('go north')
t.quit()
```

## Known Issues

When the same command is sent more than 15 times in a row, output is empty until a different command is sent.

## Games

Games are provided in this repo, but more games are available [here](http://www.ifarchive.org/indexes/if-archiveXgamesXzcode.html).

## Miscellaneous

If you are the copyright holder for any of these game files and object to their distribution in this repository, e-mail the owner at daniel.ricks4 (-a-t-) gmail.com.
