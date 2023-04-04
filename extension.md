
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
