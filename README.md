# Code-For-Future

## Set Up
I recommend, you to work in a virtual environment because This project uses some older version of the libraries and preventing this project to interfere with other projects. In your project directory, let's start off by creating a virtualenv:
``` bash 
$ virtualenv -p python3 venv/
```
And let's activate it with the source command:
``` bash
$ source venv/bin/activate
```
Install SUMO
+ For Linux: 
  ``` bash
  $ sudo add-apt-repository ppa:sumo/stable
  $ sudo apt-get update
  $ sudo apt-get install sumo sumo-tools sumo-doc
  ```
+ For Windows & Mac, Please refer to [this](https://sumo.dlr.de/docs/Installing.html) documentation.\

Clone the Repository. Then, let's use pip to install the requirements:
``` bash
$ pip3 install -r requirements.txt
```
**Note**: 
  + *You can replace `python3` to `python` as per your system variables.*
  + *Run `traffic_light.py`. There will be a pop of SUMO in which you can see code's simulation.*
  + *If SUMO doesn't get activated in python code. Please add SUMO_HOME to your evironment variables.*

## Solution Overview:
Proof Of Concept(POC) for Microsoft's Code For Future submission is defined by this repository. 

Foremost Requirement of our solution is to get Traffic Information. For Traffic Information we can rely on many technique like camera, sensor and more technique. We have bundled a code for `Vehicle Detection`. For in Real life, We can use Azure Cognitive Functions to detect and count vehicles either bundled in rpi or available in City HQ.

Traffic is a dynamic thing. So, We have used a simulator known as SUMO for traffic creation and display. SUMO almost replicates ATC. We have used Q-learnig for handling traffic. 

## Algorithm Overview
The issue definition is a basic one: Minimize the absolute holding up time all things considered 
during the reproduction. Absolute holding up time will be a proportion of the complete gathered measure of 
time held up by vehicles at a red light. To move toward this issue, we use Q-Learning, where an 
operator, in view of the given state, chooses a fitting activity for the convergence so as to 
amplify present and potential compensations. The state-activity sets, likewise called Q esteems, are found out 
also, spared to a table where there values are consistently refreshed until intermingling, where an 
perfect arrangement is found. This calculation is laid out in more detail in the accompanying areas.

We utilized the four-way crossing point, where every street has three paths driving into the 
crossing point: A correct path for right turns in particular, a center path for going straight in particular, and a left 
path for turning left as it were. What's more, a solitary path is utilized on every one of the four streets for conveying 
traffic out of the crossing point. This oversimplified model of a convergence gives us the fundamental 
conditions for testing our model on a four-way crossing point. 

We define traffic signal control issue as support learning issue where an 
specialist interfaces with the convergence at discrete time steps , t = 0,1,2.... , and the objective of operator is 
to diminish the vehicle staying time at the convergence in the long haul. In particular, such an operator 
first watches convergence state S​ t​ (characterized later) toward the get-go step t, at that point chooses and 
impels traffic signals A​ t​ . After vehicles move under impelled traffic signals, convergence state 
changes to another state S​ t​ +1. The operator likewise gets reward R​ t​ (characterized later) toward the finish of time step t 
as a result of its choice on choosing traffic signals. Such prize fills in as a sign 
directing the operator to accomplish its objective. In time succession, the specialist cooperates with the crossing point as 
... , S​ t​ , A​ t​ , R​ t​ , S​ t+1​ , A​ t+1​ ... . Next, we characterize convergence state S​ t​ , operator activity A​ t​ and reward R​ t​ , separately.

### Agent Action
The specialist sees the state and picks one of two activities : 0 - turn on green lights for the 
level streets and 1 - turn on green lights for vertical streets. Each time a state change is 
required (i.e level was green and operator chooses to turn on green lights for vertical streets or 
the other way around), before executing the activity the progressions state, we have to experience a change to the 
next state. Change would include following :- 
1) Change the lights for vehicles going straight to yellow. 
2) Change the lights for vehicles going straight to red. 
3) Change the lights for vehicles going left to yellow. 
4) Change the lights for vehicles going left to red 

Green light term is 10 seconds and yellow light span is 6 seconds. So at each time step, 
operator may choose to keep a similar state or change the state.
