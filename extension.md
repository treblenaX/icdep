# How can we add additional features to the protocol without breaking previous functionality?

Consider:
    - Send to any individual on the whole UW campus
    - Specify whether contents are ASCII text, Unicode text, or binary values
    - Keep a record of what nodes the card has passed through.

Your extension mechanism should allow for any kind of extension we can imagine

> Assuming that an index card contains up to 4 ASCII characters as the body and that Alice wants to send a message to Bob...

To add additional features to the protocol without breaking previous functionality, we need to inscribe metadata as a `header` for each respective card that Alice sends to Bob. 

In the [previous problem](anti-dupe.md), we utilized a `header` that has each card's index with `message_index` and the total amount of cards in the message as `message_length`. Therefore, we will be using the same concept to add more features to the protocol. Assuming that the protocol contains the same `message_index` and `message_length` metadata in the header as in the `anti-dupe.md` problem, we acknowledge that we have the previous functionality (and don't forget Nodey before Bob) to prevent duplicate cards.

## How can we send to any individual on the whole UW campus?

add destination and source in header

## How can we specify whether contents are ASCII text, Unicode text, or binary values?

add the type of message in header

## How can we keep a record of what nodes the card has passed through? 

add the names of the person (node) as it travels to the destination