# w3aio

This is the beginning of an asyncio version of the Ethereum Web3 libraries.
This system has been written in Python3.6.

More usage and explanations of code coming soon!

## Why This Library was Written

At Mimir, we have been building systems that work with the Ethereum blockchain for some time. What we found was that Python is an amazing language but, at some level of complexity things can get... messy. See below:

![alt text](https://imgs.xkcd.com/comics/electric_skateboard_double_comic.png)

As an aside, you can see more amazing comics at [xkcd](https://xkcd.com/license.html).

### The Hard Lessons
#### Duck Typing is Both Wonderful and Terrible

What we found was that although duck typing is great, mixing duck typing with
strong typing has it's downsides. It often left our code feeling brittle and
uncoordinated. Things like

```python
some_hex_string.replace('0x','').lower() == some_other_hex_string.replace('0x','').lower()
```

started to litter our code. Refactors cleaned this up, but there was always some edge case that worked its way back into the code. This got us thinking... what if all solidity types were objects, that knew how to add, compare, iterate, and encode themselves? Then, all of that mess could be contained in one place and not spread like a terrible virus. So we built a psuedo-strong typing system.

#### Stateful Filtering on the Node is a Bad Idea

When PubSub was added to the JSONRPC spec of Ethereum, we were like giddy children. Such a great new toy! Imagine the possibilities! What we found was that, when you mix websockets, load balancers, stateful server side filters, and production code... you get a nightmare. So all filtering is done using client side polling of the server. We also found some clients left the `proc` filesystem a little messy... almost memory leaky. This is also scary. So we said,

```
No more server side filters!

From thence day forth, all block filtering shall be done

on the client side, using a long poll and callbacks!
```
... and life has been better since.

#### Connection Objects Should Eat from a Queue

You know, graceful reconnection, backpressure, and what not.

#### More

More lessons here!

## Usage

Usage goes here!
