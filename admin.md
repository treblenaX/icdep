
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

