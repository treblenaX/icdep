# How can we send commands ("SLEEP", "RESTART", "ARE-YOU-THERE", etc) to individual nodes in the network, rather than treat them as pass-through intermediaries?

If we analyze the proposal in Q4 in the [extension file](extension.md), we should acknowledge the assumption that **each node should have an unique identifier**. This would allow the recipient to have a record of what nodes each card has passed through and the time it took.

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

