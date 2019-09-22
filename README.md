# BritBot
BritBot is a general purpose Discord Bot with various different features and British... undertones.

## Fun
BritBot has a few Fun commands, although more will come in future.

---

#### noot
It's pointless. Try it.

---

#### pong
Links to an online pong game **¯\\\_(ツ)_/¯**

---

## Util
BritBot has many util commands, and yet more to come!

---
#### whois
Return info on a given user.

Aliases:
* user
* u
> brit whois @leet_hakker
---
#### whoami
Returns info on you.

Aliases:
* me
* m
---
#### say
Have BritBot say something. This command is only available to those with **Manage Messages** permissions

Aliases:
* s
> brit say Hello

> Hello

---

#### bug
Report a bug to the devs

Aliases:
* b
> brit bug Not enough fun commands

Keep in mind that your username is included in the bug report.

---
#### ping
Return BritBot's ping to the Discord API

Aliases:
* latency
* p
* l
---
#### tea
Return news on a given query or subject.

Arguments:
* query
* category
* country
* source

Aliases:
* t
* news
> brit tea query:bitcoin category:business country:US source:Gizmodo.com

## Programming
BritBot has various code formatting commands - for those of you who like Python - that is.

---
#### blacken
Format code with "black"

Aliases:
* bn
* black
>brit blacken
> `\``py
> def very_important_function(template: str,*variables,file: os.PathLike,engine: str,header: bool = True,debug: bool = False):
>     with open(file, "w") as f:
>         print(f.read())
>
> `\``
Returns:
```py
def very_important_function(
    template: str,
    *variables,
    file: os.PathLike,
    engine: str,
    header: bool = True,
    debug: bool = False
):
    with open(file, "w") as f:
        print(f.read())
```
---
#### yapfify
Formats code using the Google YAPF formatting.

Aliases:
* y
* yp
* yapf
>brit yapfify
> `\``py
> def very_important_function(template: str,*variables,file: os.PathLike,engine: str,header: bool = True,debug: bool = False):
>     with open(file, "w") as f:
>         print(f.read())
>
> `\``
Returns:
```py
def very_important_function(template: str,
							*variables,
							file: os.PathLike,
							engine: str,
							header: bool = True,
							debug: bool = False):  
	with open(file, "w") as f:
		print(f.read())
```
---
#### pepify
Formats code using PEP8 formatting

Aliases:
* pep
* pep8
* p8
>brit pepify
>\`\``py
> def very_important_function(template: str,*variables,file: os.PathLike,engine: str,header: bool = True,debug: bool = False):
>     with open(file, "w") as f:
>         print(f.read())
>
> `\``

Returns:
```py
def very_important_function(template: str, *variables, file: os.PathLike, engine: str, header: bool = True, debug: bool = False):
    with open(file, "w") as f:
        print(f.read())
```
This is the least noticeable of all the formatters.

---
