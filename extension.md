# How can we add additional features to the protocol without breaking previous functionality?

> Assuming that an index card contains up to 4 ASCII characters as the body, Nodey is before Bob as the anti-duplication manager from the [`anti-dupe problem`](/anti-dupe.md), and that Alice wants to send a message to Bob...

Generally, we can add additional features to the protocol without breaking previous functionality by adding more metadata to the card's `header` and/or introducing nodes with a special role.

---
## How can we send a message to any individual on the whole UW campus?
---

If there are enough people on the whole UW campus standing right next to each other where they could pass the card to any message recipient, we can send a message to any individual by adding the recipient's name as `recipient_name` in the metadata `header`. Then the nodes/people can keep passing the card until they find the right node with the recipient name.

On the other hand, if the people are not right next to each other and there's some distance, then the nodes would have to travel to the next node and repeat the process until they reach the destination described in the `recipient_location` metadata where they can hand the message to the person with the name under `recipient_name`.

Therefore, the most optimal way to send a message to the correct individual would be to include `recipient_location` and `recipient_name` in the metadata `header`. We need the location so if the nodes have to travel to pass the card towards the destination, then they know exactly where to travel towards. Then, when they have arrived at the destination, they can just search for the specific person with the name under `recipient_name`. This is very similar to an **envelope** where one usually writes the recipient's name and address on it so the postal service knows where to go to and who to give the message to.

---
## How can we specify whether contents are ASCII text, Unicode text, or binary values?
---

To specify whether the contents or body are ASCII text, Unicode text, or binary values, we can add the value `content_type` to the metadata `header` so each nodes and the recipients would know what format the body data is in. This is basically the practice of the `Content-Type` header when working with [HTTP requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type).

---
## How can we keep a record of what nodes the card has passed through?
---

Assuming that each node has a unique identifier, we need to add a `route-map` variable to the `header` metadata to keep a record of what nodes the card has passed through. The `route-map` variable is a collection of key-value pairs. When the card is first sent out, the sender adds their unique identifier and the timestamp sent to the `route-map`. When the card is acknowledged by a node/person, they would add their unique identifier as the key and the timestamp received as the value to `route-map`. Then when the card is finally received by the recipient, they can use their acknowledgement timestamp to calculate exactly how long it took to get from the sender to the receiver and the intermediary times in between nodes.

> For example, if the route is [Alice, Z, Y, X, Bob] then this would be the interaction:

    Alice acknowledges the card, appends { Alice: '0' } into the map, then sends it out to Z.
    Z acknowledges the card, appends { Z: '100' } into the map, then sends it out to Y.
    Y acknowledges the card, appends { Y: '200' } into the map, then sends it out to X.
    X acknowledges the card, appends { X: '300' } into the map, then sends it out to Bob.
    Bob acknowledges the card, appends { Bob: '500' } into the map.

Now the entire history of the card's journey is marked and the latency of the card can be determined as well. 

    {
        Alice: '0', // in ms
        Z: '100',
        Y: '200',
        X: '300',
        Bob: '500'
    }

    *TBN = Time Between Nodes
    Recipient   |   TBN*     |   Calculation |
    _________________________________________
    Alice       |   0ms     |   NA          |
    Z           |   100ms   |   100 - 0     |
    Y           |   100ms   |   200 - 100   |
    X           |   100ms   |   300 - 200   |
    Bob         |   200ms   |   500 - 300   |
