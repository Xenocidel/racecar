// Posssible Driver outline

// safety mode is controlled by the Driver independently from states given by the Codriver
bool safetyMode;

enum State
{
	Auto,
	Turning,
	Slow
}

void autoProgram()
{
}

void turningProgram()
{
}

void slowProgram()
{
}

void safetyProgram()
{
}

// function that gets called by spin?? Not sure if this is how ROS does it...
void callback(const State driverState)
{
    if(!safetyMode) // car can perform normal activity...
    {
	switch(driverState)
	{
		case Auto:
			autoProgram();
			break;
		case Turning:
			turningProgram();
			break;
		case Slow:
			slowProgram();
			break;
	}
    }
    else    // car is in safety mode...
    {
	safetyProgram();
    }
}


int main(int argc, char** argv)
{
	//ros::init(argc, argv, "driver");
	
	//ros::Subscriber codriver_sub = n.subscribe("codriver_sub", callback);
	//ros::Publisher motor_pub = n.advertise .....

	ros::spin();
}
