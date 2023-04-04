
---
# How can we ensure that each card is received once and only once?

> Assuming that an index card contains up to 4 ASCII characters as the body... 

We need to start keeping track of the metadata with a `header` First, we sum up the number of cards in a message and add it to each card's header as the `message_length` to describe the total number of cards in the message. Second, we think about the whole message as an array of cards in the correct order, and then acknowledge each card's respective index in the array. Next, we add each card's respective index into its header as the `message_index`. Therefore, Bob is now able to see if he has received all of the cards to make the message by comparing the number of cards he has to the `message_length` metaadata in the header. Received cards less or larger than the `message_length` after a set amount of time waiting could help Bob be aware of a discrepancy. 

--- 
## Q1: However, what there is a risk of Bob receiving duplicate cards?
---
### Protocol Extension:
>We can have every person (or node) be tasked with the job of keeping track of duplicate cards and discarding them. Generally, when a node receives a card, they will acknowledge receiving that card and deny any future cards with the same data. 
>
>With this protocol, the person/node (let's call them Nodey) who will hand the card to Bob can guarantee that Bob will not receive duplicate cards. If all of the incoming cards go through Nodey, then Nodey will be able to act as a safeguard, and reject any duplicate cards. Thus, Bob will never have known the existence of any duplicate cards.

For example, Alice's message contains 3 cards total and Nodey has received the incoming cards in this (zero-indexed) order [0, 1, 0, 2, 2]. 

    Nodey receives card #0, acknowledges it, and gives it to Bob
    Nodey receives card #1, acknowledges it, and gives it to Bob
    Nodey receives card #0, observes that card #0 has already been received, and throws it away
    Nodey receives card #2, acknowledges it, and gives it to Bob
    Nodey receives card #2, observes that card #2 has already been received, and throws it away

Therefore in Bob's perspective

    Bob receives card #0 and acknowledges it.
    Bob receives card #1 and acknowledges it.
    Bob receives card #2 and acknowledges it.

>If by any chance, Nodey has an unexpected downtime, then the successor of Nodey can request Bob to send them the cached data of what cards have been received before sending the incoming cards to Bob, and the successor of Nodey can acknowledge that data. Therefore, allowing the protocol to proceed. 
>
>As an extra edge case, if Alice is passing directly to Bob without any intermediary nodes, and there somehow are duplicates. Alice could ask Bob if he has received a specific card before sending it. After Bob acknowledges that he has not, then Alice can proceed to send the card.

:white_check_mark: And thus, it is a guarantee that Bob has received each card once and only once
