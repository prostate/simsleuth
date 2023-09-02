# `simsleuth`

**Reconnaissance tool designed to identify Twitter accounts vulnerable to sim-swap attacks.**

![TWMobile](https://i.imgur.com/nh6xna9.png)

**[Setup](#setup)**
・**[Demo](#demo)**
・**[Features](#features)**
・**[Goals](#goals)**

*Please note that this project is a work in progress. Refer to the [goals section below](#goals).*

### What is `simsleuth`?
`simsleuth` is a specialized reconnaissance tool designed for the purpose of identifying Twitter accounts that may be vulnerable to sim-swap attacks. Sim-swap attacks are a type of cybersecurity threat where an attacker fraudulently gains control over a victim's phone number, often by tricking a mobile carrier into transferring the number to a new SIM card under the attacker's control.

> *"Over the past four months $13.3M+ has been stolen as a result of 54 SIM swaps targeting people in the crypto space."* - [ZachXBT](https://twitter.com/zachxbt/status/1694326221511794706)

![zach](https://pbs.twimg.com/media/F4N0t25WYAA4ca7?format=jpg&name=large)

### Demo
https://github.com/prostate/simsleuth/assets/803285/6ec9429b-ee37-47ce-9af9-7f915e23e5e4



### Features
- Raw HTML Requests (Zero Mid-lenium)
- Proxy Support
- Automated Email & Phone Doxxing via [Snusbase](https://snusbase.com)
- Automated Phone Carrier Lookup (e.g., T-Mobile, AT&T, Verizon)
- Telegram Logging
- Very Fast & Easy to use (Thanks Telegram)

### Goals
- Implement doxx pre-check to avoid "Further verification needed"
- Provide Twitter Account Interaction Statistics
- ~~Automate Phone Carrier Lookup (e.g., T-Mobile, AT&T, Verizon)~~ - Done.
- Develop an Algorithm for Account Harvesting to Minimize Manual Work
- Enhance Autodoxxing capabilities using [IntelX](https://intelx.io)

### Setup
> **Warning**
>
> Setup section is currently inaccurate & filled with placeholders.
Use any server, preferably Debian or Ubuntu.

To get started, clone the repository:

```sh
git clone https://github.com/prostate/twmobile
cd twmobile
```

Then install the required dependencies:

```sh
pip install -r requirements.txt
```

Fill in the `.env` file with the necessary information:

```sh
TELEGRAMTOKEN=your_bot_token_here
TELEGRAMCHATID=your_chatid_here
SNUSBASEAPIKEY=your_snusbase_api_key
ROTATINGPROXY=http://username:password@ip:port
```

Next, run the tool using tmux and then disconnect from the server:

```sh
tmux
```

```sh
python3 manager.py
```

```sh
ctrl-b + d
```


## Acknowledgments
* [ZachXBT](https://twitter.com/zachxbt) (aka fed): For inspiring this project
* [Snusbase](https://snusbase.com/): Provider of the necessary DBs for Doxxing and their API