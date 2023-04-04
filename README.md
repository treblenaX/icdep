<h1>What needs fixing in the Index Card Data Exchange Protocol?</h1>
<p>Please check the individual files or refer to the dropdowns below...</p>
<p><em>The markdowns in the dropdowns are automatically updated with each markdown edit! So they are up-to-date :)</em></p>

<details>
    <summary>anti-dupe.md</summary>
        
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

</details>

<details>
    <summary>extension.md</summary>
        
---
# How can we add additional features to the protocol without breaking previous functionality?

> Assuming that an index card contains up to 4 ASCII characters as the body, and that we follow the anti-duplication protocol from the [`anti-dupe problem`](/anti-dupe.md)...

---
## Q2: How can we send a message to any individual on the whole UW campus?
---
If there are enough people on the whole UW campus standing right next to each other where they could pass the card to any message recipient, we can send a message to any individual by adding the recipient's name as `recipient_name` in the metadata `header`. Then the nodes/people can keep passing the card until they find the right node with the recipient name.

On the other hand, if the people are not right next to each other and there's some distance, then the nodes would have to travel to the next node and repeat the process until they reach the destination described in the `recipient_location` metadata where they can hand the message to the person with the name under `recipient_name`.

### Protocol Extension:
>Therefore, the most optimal way to send a message to the correct individual would be to include `recipient_location` and `recipient_name` in the metadata `header`. We need the location so the nodes that have to travel to pass the card towards the destination knows the direction to travel towards. Then, when they have arrived at the destination, they can just search for the specific node with the name under `recipient_name`. This is very similar to an **envelope** where one usually writes the recipient's name and address on it so the postal service knows where to go to and who to give the message to.

:white_check_mark: We can now send a message to any individual on the whole UW campus and each node still follows the `anti-duplication` functionality as mentioned before! Thus, not breaking any existing functionalities.

---
## Q3: How can we specify whether contents are ASCII text, Unicode text, or binary values?
---

### Protocol Extension:
>To specify whether the contents or body are ASCII text, Unicode text, or binary values, we can add the value `content_type` to the metadata `header` so each nodes and the recipients would know what format the body data is in. The values under `content_type` is an enumeration of the type of data that the card is carrying. This is basically the practice of the `Content-Type` header when working with [HTTP requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type). 

:white_check_mark: Now we can have each node understand what type of messages we are sending and the previous functionalities are not broken as we are only extending the `header` metadata. 

---
## Q4: How can we keep a record of what nodes the card has passed through?
---

### Protocol Extension:
> We need to introduce the idea that each node has a **unique identifier**.
> Next, we need to add a `route-map` variable to the `header` metadata to keep a record of what nodes the card has passed through. The `route-map` variable is a collection of key-value pairs.
>
>Before the sender sents the card, the sender adds their unique identifier and a timestamp of processing to the `route-map`. Then they can proceed to sent the card out.
>
>When the card is acknowledged by a receiving node, they would follow this protocol and add the key-value pair below to the card's `route-map` metadata.

    {
        <NODE_UID>: <TIMESTAMP_RECEIVED>
    }
>The other intermediary nodes will proceed to follow this protocol.
>
>Then when the card is finally received by the recipient, the recipient can use their acknowledgement timestamp to calculate exactly how long it took to get from the sender to the receiver and the intermediary times in between nodes.

For example, if the route is [Alice, Z, Y, X, Bob] then this would be the interaction:

    Alice acknowledges the card, appends { Alice: '0' } into the map, then sends it out to Z.
    Z acknowledges the card, appends { Z: '100' } into the map, then sends it out to Y.
    Y acknowledges the card, appends { Y: '200' } into the map, then sends it out to X.
    X acknowledges the card, appends { X: '300' } into the map, then sends it out to Bob.
    Bob acknowledges the card, appends { Bob: '500' } into the map.

:white_check_mark: Now the entire route history of the card's journey is marked and the latency of the card can be determined as well. The previous functionalities are not broken as we are only extending the `header` metadata and are not interfering with previous protocols!

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

</details>

<details>
    <summary>admin.md</summary>
        
---
# Q5: How can we send commands ("SLEEP", "RESTART", "ARE-YOU-THERE", etc) to individual nodes in the network, rather than treat them as pass-through intermediaries?

> Assuming that an index card contains up to 4 ASCII characters as the body, and that we follow the previous protocols from the [`anti-dupe problem`](/anti-dupe.md) and the [`protocol extension problems`](/extension.md)...
---

### Protocol Extension
> If we analyze the proposal in Q4 in the [extension file](extension.md), we should acknowledge the protocol that **each node should have an unique identifier**. This would allow the recipient to have a record of what nodes each card has passed through and the time it took.
>
>Therefore, we should consider each person as a node, including the sender and recipient. 
>
>Naturally, every person has a name as their unique identifier. If I was a node, then my unique identifier would be "Elbert Cheng". If there is another person with the same name as me, then we can resolve this issue by changing the naming protocol to have each node have a hash as their unique identifier rather than a full name.

![Picture of a Graph](http://web.cecs.pdx.edu/~sheard/course/Cs163/Graphics/graph1.png)

> Then we start to see a resemblance to a graph in terms of connections and nodes. If we want to send a command to an individual node, then we need to add the `recipient_name` and `recipient_location` in the `header` metadata. Maybe also add a `content_type` of the `COMMAND` type to tell the individual node that we want them to perform a specific action.
>
> Now we can start sending the message. When the recipient node receives the message instruction, it will acknowledge the message to the sender so we know that the node has successfully received the message and is performing the action.

Here's an example: If the sender is Node 1 and they want to send the command, `SLEEP`, to Node 5 then what would the interaction be?

    Node 1 prepares the message.
        Header: 
            {
                recipient_name: 4,
                content_type: 'COMMAND',
                ...
            }
        Body: 'SLEEP'
    Node 1 sends the first card to Node 5.
    Node 5 receieves the card and acknowledges it.
    Repeat sending the rest of the cards to Node 5 until Node 5 receives the full message.
    Node 5 acknowledges the success of receiving the message and then performs the command.

:white_check_mark: Therefore, if every node has a unique identifier (including the sender and recipient), and that every node follows all of the protocols that we have established in this entire exercise set. Then we can expect every node to behave the same way and enable the processing of commands for each node. This would be very similar to a Peer-2-Peer (P2P) network.


</details>