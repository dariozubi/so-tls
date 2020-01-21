# Self-organizing traffic lights in SUMO
> :warning: I'm not working on this tools anymore, they may or may not work since I last used them in 2018.

## Description

This project contains some tools for the open source traffic simulator [SUMO](http://sumo.sourceforge.net/) that I used for my masters degree that may be of some use for some one else. The main purpose of this files was to create some networks to test the difference between self-organizing traffic lights and other traffic light models.

## Overview

To create a new simulation with this files, you need 7 files:
1. Network
2. Detectors
3. Configuration
4. Output
5. Traffic light programs
6. Routes

Once all the files are created you can run a simulation with the `runner.py` script.

:exclamation: All the scripts mentioned below have a `-h` flag to have more details about the options. 

## Network

To create the network files first you need to take a map from [Open Street Maps](https://www.openstreetmap.org). Then edit it with [JOSM](https://josm.openstreetmap.de/) until it looks as you want in SUMO. To test it in SUMO run the `newMap.py` script inside the `newmap` folder and run the  `runner.py` script.  `newMap.py` creates all the basic files (except the routes) but there's not going to be any simulation yet.

## Routes

To generate some routes for the cars you can use the `generateRoutes.py` script inside the `input` folder. The basic command is:

`python generateRoutes.py -n map -p 0.1 -c 1`

Which generates 0.1% of all routes with 1 vehicle per route for the map called _map_.

## Simulation

Once the routes are added you can run a new simulation with the main `runner.py` script. For example, create an output folder in `output/map`. Then, to run a simulation with the self-organizing method (default) using the _map_ created with the previous scripts and with `sumo-gui` to visualize it you use:

`python runner.py --dirNet map -g`

In this case the script uses the files inside the `input/map` folder, if they don't exist it will fail. The output folder must also be created before running the script.

## Results

If everything works as it should you should get results inside the `output/map` folder. 

If you are using the self-organizing traffic lights you can analyze the results with the `parseResults.py` script inside the `output` folder. To run it you should run something similar to:

`python parseResults.py -d map -s 0 -g`

This should produce some `.txt` files containing the **shanon information** for every street, traffic light and intersection with a traffic light in the simulation. There's also files with the **occupancy**, **mean speed** and **mean waiting time** of the streets divided by priority. All this files produce a graphs inside the `graphs/map` folder. This graphs are made with the `graphMaker.R` script inside the `graphs` folder.