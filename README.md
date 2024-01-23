# `simsleuth`

**Reconnaissance tool designed to identify Twitter accounts vulnerable to sim-swap attacks.**

![simsleuth](https://i.imgur.com/nh6xna9.png)

**[Setup](#setup)**
・**[Demo](#demo)**
・**[Goals](#goals)**

*Please note that this project is a work in progress. Refer to the [goals section below](#goals).*

### What is `simsleuth`?
`simsleuth` is a specialized reconnaissance tool designed for the purpose of identifying Twitter accounts that may be vulnerable to sim-swap attacks. Sim-swap attacks are a type of cybersecurity threat where an attacker fraudulently gains control over a victim's phone number, often by tricking a mobile carrier into transferring the number to a new SIM card under the attacker's control.

> *"Over the past four months $13.3M+ has been stolen as a result of 54 SIM swaps targeting people in the crypto space."* - [ZachXBT](https://twitter.com/zachxbt/status/1694326221511794706)

![zach](https://pbs.twimg.com/media/F4N0t25WYAA4ca7?format=jpg&name=large)

### Demo
https://github.com/prostate/simsleuth/assets/803285/6ec9429b-ee37-47ce-9af9-7f915e23e5e4

### Goals
- Implement doxx pre-check to avoid "Further verification needed"
- Provide Twitter Account Interaction Statistics
- Automate Phone Carrier Lookup (e.g., T-Mobile, AT&T, Verizon)
- Enhance Autodoxxing capabilities using [IntelX](https://intelx.io)

### Setup

To get started, clone the repository:

```sh
git clone https://github.com/prostate/simsleuth && cd simsleuth
```

Fill in the `config.toml` file with the necessary information:

```toml
[telegram]
token = "YOUR_TELEGRAM_BOT_TOKEN"

[web]
proxy_url="http://user:password@ip:port"
```

Then:

```sh
pip3 install telebot toml rich requests
```
```sh
python3 svc.py
```

## Acknowledgments
* [ZachXBT](https://twitter.com/zachxbt) (aka fed): For inspiring this project
