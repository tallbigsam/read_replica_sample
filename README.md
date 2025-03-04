this needs a .env with three values:

username=username
password=password
cluster_fqdn=samplecluster.aownd.mongodb.net

the best way to run this test is to set up an Atlas cluster with the following config:

3x electable nodes which are as far away as possible from you geographically.
1x read only (non electable) node which is in your current region you will run the script from

See that the latency on the connection with read preference connection which is set to nearest is far better than those of the electable nodes which are as far away as possible
