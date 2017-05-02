#include <ros/ros.h>
#include <sensor_msgs/Image.h>
#include <stdlib.h>

struct elapsed{
    int seq; double start; double end;
};

int equals(elapsed e1, int id) { return e1.seq==id; }

class timingTattler
{
  ros::NodeHandle nh_;
  ros::NodeHandle private_nh_;

  ros::Subscriber sub_raw,sub_proc;
  std::vector <elapsed> measurements;
  int offset;

  void callback_raw(const sensor_msgs::Image& msg)
  {
    if (offset==0) 
    {
        offset = msg.header.seq;
        printf("set offset to %d\n",offset);
    }
    elapsed e = {msg.header.seq - offset,msg.header.stamp.toSec(),0};
    measurements.push_back(e);
  }

  void callback_proc(const sensor_msgs::Image& msg)
  {
    int id = msg.header.seq;
    double time = msg.header.stamp.toSec();
    for (int i =0;i<measurements.size();i++) {
        if (equals(measurements[i],id)) {
            measurements[i].end = time;
            printf("%f\n",measurements[i].end - measurements[i].start);
            return;
        }
    }
  }

  public:
  void getAverageProcessingTime() 
  { 
    int sum;
    int n;
    for (int i =0;i<measurements.size();i++) {
        if (measurements[i].end==0) continue;
        int temp = measurements[i].end - measurements[i].start;
        if (temp<0) continue;
        sum += temp;
        n++;
    } 
    double avg = (double)sum/n;
    printf("Average elapsed time was %f\n",avg);
  }

  timingTattler():nh_(), private_nh_("~")
  {
    offset = 0;
    sub_raw = nh_.subscribe("/zed/right/image_raw_color",10,&timingTattler::callback_raw,this);
    sub_proc = nh_.subscribe("/right_edges",10,&timingTattler::callback_proc,this);
  }
  
};


int main(int argc, char** argv)
{
    ros::init(argc,argv,"timer");
    timingTattler t;
    ros::spin();
    return 0;
}


