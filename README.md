# Container images

## `entry` is the image run by a single node that starts the process

1. Gets random Wikipedia article
2. Picks random paragraph from the article

TODO:

3. Scale workers for each word (or sentence? or some other grouping)
4. Sends each worker their segment
5. Collects results

## `worker` is the image run by worker nodes that takes in a string, transforms it, and then returns it

1. Listens for incoming data on port 3130

TODO:

0. Generate database of homophones
   (at docker build time or container load time?)
1. Listen on port for incoming data
2. Return transformed data

# Compiling

1. Go into the directory containing the image you want to build
   (`entry` or `worker`)
2. Run `docker build`
