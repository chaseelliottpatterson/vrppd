##Installation
git clone https://github.com/chaseelliottpatterson/vrppd.git

##Usage
cd vrppd
python evaluateShared.py --cmd "python submission.py" --problemDir "Training Problems"

###Note
if using this script with evaluateShared.py or a variation on this script please ensure snippit "line = line.replace('\r','')" is included under the loadSolutionFromString() function (line 78 on evaluateShared.py). I was having diificulty removing '\r' from python stdout so I cleaned it on the inupt side instead

##Resources
Single-Depot VRP (Clark>Wright Savings Algorithm) -- https://web.mit.edu/urban_or_book/www/book/chapter6/6.4.12.html

Clarke and Wright Savings Algorithm as Solutions Vehicle Routing Problem with Simultaneous Pickup Delivery (VRPSPD) -- https://iopscience.iop.org/article/10.1088/1742-6596/2421/1/012045/pdf

A Heuristic Approach Based on Clarke-Wright Algorithm for Open Vehicle Routing Problem -- https://pmc.ncbi.nlm.nih.gov/articles/PMC3870871/