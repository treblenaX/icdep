<h1>What needs fixing in the Index Card Data Exchange Protocol?</h1>
<p>Please check the individual files or refer to the dropdowns below...</p>

<details>
    <summary>anti-dupe.md</summary>
    <div>
        
---
# Q1: How can we ensure that each card is received once and only once?

> Assuming that an index card contains up to 4 ASCII characters as the body and that Alice wants to send a message to Bob, we need to keep track of the data from the header metadata. First, we sum up the number of cards in a message and add it to each card's header as the `message_length` to describe the total number of cards in the message. Second, we think about the whole message as an array of cards in the correct order, and then be aware of each card's respective index in the array. Then we add each card's respective index into its header as the `message_index`. Therefore, Bob is now able to see if he has received all of the cards to make the message by comparing the number of cards he has to the `message_length` metaadata in the header. Received cards less or larger than the `message_length` could help Bob be aware of a discrepancy. 

--- 
## However, what there is a risk of Bob receiving duplicate cards?
---



We can place another person, we will call them Nodey, before Bob tasked with the job of keeping track of duplicate cards and discarding them. Generally, when Nodey receives a card, they will acknowledge receiving that card and deny any cards with the same data. Then, Nodey will proceed to give that card to Bob, ensuring that he will receive the card only once. If Nodey receives a duplicate card, they will reject that card and discard it. Therefore, Bob will never have known the duplicate card's existence. 

> For example, Alice's message contains 3 cards total and Nodey has received the incoming cards in this (zero-indexed) order [0, 1, 0, 2, 2]. 

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

    </div>
</details>

<details>
    <summary>extension.md</summary>
    <div>
        
---
# Q2: How can we add additional features to the protocol without breaking previous functionality?

> Assuming that an index card contains up to 4 ASCII characters as the body, Nodey is before Bob as the anti-duplication manager from the [`anti-dupe problem`](/anti-dupe.md), and that Alice wants to send a message to Bob...

Generally, we can add additional features to the protocol without breaking previous functionality by adding more metadata to the card's `header` and/or introducing nodes with a special role.

---
## Q3: How can we send a message to any individual on the whole UW campus?
---

If there are enough people on the whole UW campus standing right next to each other where they could pass the card to any message recipient, we can send a message to any individual by adding the recipient's name as `recipient_name` in the metadata `header`. Then the nodes/people can keep passing the card until they find the right node with the recipient name.

On the other hand, if the people are not right next to each other and there's some distance, then the nodes would have to travel to the next node and repeat the process until they reach the destination described in the `recipient_location` metadata where they can hand the message to the person with the name under `recipient_name`.

:white_check_mark: Therefore, the most optimal way to send a message to the correct individual would be to include `recipient_location` and `recipient_name` in the metadata `header`. We need the location so if the nodes have to travel to pass the card towards the destination, then they know exactly where to travel towards. Then, when they have arrived at the destination, they can just search for the specific person with the name under `recipient_name`. This is very similar to an **envelope** where one usually writes the recipient's name and address on it so the postal service knows where to go to and who to give the message to.

---
## Q4: How can we specify whether contents are ASCII text, Unicode text, or binary values?
---

:white_check_mark: To specify whether the contents or body are ASCII text, Unicode text, or binary values, we can add the value `content_type` to the metadata `header` so each nodes and the recipients would know what format the body data is in. This is basically the practice of the `Content-Type` header when working with [HTTP requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type).

---
## Q5: How can we keep a record of what nodes the card has passed through?
---

Assuming that each node has a unique identifier, we need to add a `route-map` variable to the `header` metadata to keep a record of what nodes the card has passed through. The `route-map` variable is a collection of key-value pairs. When the card is first sent out, the sender adds their unique identifier and the timestamp sent to the `route-map`. When the card is acknowledged by a node/person, they would add their unique identifier as the key and the timestamp received as the value to `route-map`. Then when the card is finally received by the recipient, they can use their acknowledgement timestamp to calculate exactly how long it took to get from the sender to the receiver and the intermediary times in between nodes.

> For example, if the route is [Alice, Z, Y, X, Bob] then this would be the interaction:

    Alice acknowledges the card, appends { Alice: '0' } into the map, then sends it out to Z.
    Z acknowledges the card, appends { Z: '100' } into the map, then sends it out to Y.
    Y acknowledges the card, appends { Y: '200' } into the map, then sends it out to X.
    X acknowledges the card, appends { X: '300' } into the map, then sends it out to Bob.
    Bob acknowledges the card, appends { Bob: '500' } into the map.

:white_check_mark: Now the entire history of the card's journey is marked and the latency of the card can be determined as well. 

    {
        Alice: '0', // in ms
        Z: '100',
        Y: '200',
        X: '300',
        Bob: '500'
    }

    Recipient   |   TBN*     |   Calculation |
    _________________________________________
    Alice       |   0ms     |   NA          |
    Z           |   100ms   |   100 - 0     |
    Y           |   100ms   |   200 - 100   |
    X           |   100ms   |   300 - 200   |
    Bob         |   200ms   |   500 - 300   |

    *TBN = Time Between Nodes

    </div>
</details>

<details>
    <summary>admin.md</summary>
    <div>
        
---
# Q6: How can we send commands ("SLEEP", "RESTART", "ARE-YOU-THERE", etc) to individual nodes in the network, rather than treat them as pass-through intermediaries?

If we analyze the proposal in Q5 in the [extension file](extension.md), we should acknowledge the assumption that **each node should have an unique identifier**. This would allow the recipient to have a record of what nodes each card has passed through and the time it took.

Therefore, we should consider each person as a node, including the sender and recipient. 

Naturally, every person has a name as their unique identifier. If I was a node, then my unique identifier would be "Elbert Cheng". If there is another person with the same name as me, then we can resolve this issue by changing the naming protocol to have each node have a hash as their unique identifier rather than a full name.

![Picture of a Graph](http://web.cecs.pdx.edu/~sheard/course/Cs163/Graphics/graph1.png)

Then we start to see a resemble to a graph in terms of connections and nodes. If we can want to send a command to an individual node, then we need to add the `recipient_name` in the metadata `header`. Maybe also a `content_type` of `COMMAND` to describe that we want the individual node to perform a specific action. Then we can start sending the message. When the specific node receives the message instruction, it will acknowledge the message to the sender so we know that the node has successfully received the message and is performing the action.

> Here's a possible example: If the sender is Node 1 and they want to send the command, `SLEEP`, to Node 5 then what would the interaction be?

    Node 1 prepares the message.
        Header: 
            {
                recipient_name: 4,
                content_type: 'COMMAND',
                ...
            }
        Body: 'SLEEP'
    Node 1 sends the card to Node 5.
    Node 5 receieves the card and acknowledges it.
    Repeat until Node 5 receives the entire message.
    Node 5 acknowledges the entire message then performs the command.

:white_check_mark: Therefore, if everyone has a unique identifier, and we consider all of the people as a node that could send the cards and receive the cards. Then we can send commands and honestly any sort of regular message to the individual nodes in the network. This would be very similar to a Peer-2-Peer (P2P) network.


    </div>
</details>