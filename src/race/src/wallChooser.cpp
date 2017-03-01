#include <ros/ros.h>
#include <geometry_msgs/PoseWithCovarianceStamped.h>
#include <std_msgs/Int32.h>
#include "math.h"


int main(int argc, char** argv){
  ros::init(argc, argv, "side_control");

  ros::NodeHandle n;
  ros::Publisher side_pub = n.advertise<std_msgs::Int32>("side", 50);
  ros::Subscriber pose_sub = n.subscribe("amcl_pose",1, callback);


  int car_x = 0;
  int car_y = 0;
  int direction = get_param("direction",1);
  int currentNode = get_param("current_node", 1);
  int in_threshold = 10;
  int out_threshold = 1;

  int nodes[][] = [];


  ros::Time current_time, last_time;
  current_time = ros::Time::now();
  last_time = ros::Time::now();

  ros::Rate r(1.0);
  while(n.ok()){

    ros::spinOnce();               // check for incoming messages
    current_time = ros::Time::now();

    


    //publish the message
    odom_pub.publish(odom);

    last_time = current_time;
    r.sleep();
  }
}

void callback(PoseW



}
