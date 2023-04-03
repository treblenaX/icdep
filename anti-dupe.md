# Q1: How can we ensure that each card is received once and only once?

> Assuming that an index card contains up to 4 ASCII characters as the body and that Alice wants to send a message to Bob, we need to keep track of the data from the header metadata. First, we sum up the number of cards in a message and add it to each card's header as the `message_length` to describe the total number of cards in the message. Second, we think about the whole message as an array of cards in the correct order, and then be aware of each card's respective index in the array. Then we add each card's respective index into its header as the `message_index`. Therefore, Bob is now able to see if he has received all of the cards to make the message by comparing the number of cards he has to the `message_length` metaadata in the header. Received cards less or larger than the `message_length` could help Bob be aware of a discrepancy. 

--- 
## However, what there is a risk of Bob receiving duplicate cards?
---

We can place another person, we will call them Nodey, before Bob tasked with the job to keep track of duplicate cards and discard them. Generally, when Nodey receives a card, they will acknowledge receiving that card and deny any cards with the same data. Then, Nodey will proceed to give that card to Bob, ensuring that he will receive the card only once. If Nodey receives a duplicate card, they will reject that card and discard it. Therefore, Bob will never have known the duplicate card's existance. 

> For example, Alice's message contains 3 cards total and Nodey has receievd the incoming cards in this (zero-indexed) order [0, 1, 0, 2, 2]. 

    Nodey receives card #0, acknowledges it, and gives it to Bob
    Nodey receives card #1, acknowledges it, and gives it to Bob
    Nodey receives card #0, observes that card #0 has already been received, and throws it away
    Nodey receives card #2, acknowledges it, and gives it to Bob
    Nodey receives card #2, observes that card #2 has already been received, and throws it away

Therefore in Bob's perspective

    Bob receives card #0 and acknowledges it.
    Bob receives card #1 and acknowledges it.
    Bob receives card #2 and acknowledges it.

:white_check_mark: Bob has received each card once and only once
