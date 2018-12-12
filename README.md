# Bavaria

Bavaria is a Python API for obtaining live data of the S-Bahn system in Munich.
This projects is a wrapper for the undocumented websocket API that used by the
Livemap beta feature in the [Munich Navigator-App][1].

*Note*: Currently the code is highly unstable.

## Quickstart

Install Bavaria using:

``` shell
$ pip install bavaria
```

The following snippet demonstrates how to subscribe on the `newsticker` channel. This channel
provides news messages.

``` python
import asyncio

from bavaria import create_feed
from bavaria.api.messages import NewsTicker

def print_news_item(item):
    """ Print news item to stdout. """
    time = item.updated.strftime('%Y.%m.%d %H:%M')

    print(f'\033[0;37;42m{time}\033[m \033[0;37;41m{item.title}\033[m')
    print(f'{item.content}')


async def main():
    feed = await create_feed()

    # Fetch latest news items from channel 'newsticker'.
    await feed.get('newsticker')

    # Subscribe for new items on items 'newsticker'.
    await feed.subscribe('newsticker')

    try:
        async for item in feed:
            if isinstance(item, NewsTicker):
                for msg in item.messages:
                    print_news_item(msg)

    except KeyboardInterrupt:
        await feed.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
```

## Features

* Newsticker

## License

Bavaria is licensed under MIT License.

[1]: https://www.s-bahn-muenchen.de/s_muenchen/view/service/mue_nav_app.shtml
