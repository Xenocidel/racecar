#include <ros/ros.h>
#include <sensor_msgs/Image.h>
#include <math.h>
#define square(x) x*x
#define get(vec,vec_W,i,j) vec[i*vec_W + j]

class zedNav
{
  ros::NodeHandle nh_;
  ros::NodeHandle private_nh_;

  ros::Publisher pub_;
  ros::Subscriber sub_;


  void callback(const sensor_msgs::Image& msg)
  {
	sensor_msgs::Image edge;
    int i,j;
    int W = msg.width, H = msg.height;
    if (msg.encoding.compare("mono8")) {
        printf("Match failed\n");
        return;
    }
    edge.header = msg.header;
    edge.height = msg.height;
    edge.width = msg.width;
    edge.encoding = "mono8";
    edge.is_bigendian = msg.is_bigendian;
    edge.step = msg.step;
    std::vector <unsigned char> bw = msg.data;

    int dx,dy;
    for (i=0;i<H;i++) {
        if (i==0 || i==(H-1)) {
            for (j=0;j<W;j++) edge.data.push_back(0);
        }
        else {
            edge.data.push_back(0);
            for (j=1;j<W-1;j++) {
                int index = W*i + j; 
                //dx = bw[index]- bw[index-1];
                //dy = bw[index-W] - bw[index];
                dx = bw[index+W+1] + 2*bw[index+1] + bw[index-W+1] \
                - (bw[index+W-1] + 2*bw[index-1] + bw[index-W-1]);
                dy = bw[index-W-1] + 2*bw[index-W] + bw[index-W+1]\
                - (bw[index+W-1] + 2*bw[index+W] + bw[index+W+1]);
                //printf("%d, %d, %f%%\n",i,j,(float)edge.data.size()/bw.size()*100);
                /*dx = get(bw,W,i+1,j+1) + 2*get(bw,W,i,j+1) + get(bw,W,i-1,j+1) \
                - (get(bw,W,i+1,j-1) + 2*get(bw,W,i,j-1) + get(bw,W,i-1,j-1));
                printf("dx\n");
                dy = get(bw,W,i-1,j-1) + 2*get(bw,W,i-1,j) + get(bw,W,i-1,j+1) \
                - (get(bw,W,i+1,j-1) + 2*get(bw,W,i+1,j) + get(bw,W,i+1,j+1));
                */
                edge.data.push_back(sqrt(square(dx) + square(dy)));
            }
            edge.data.push_back(0);
        }
    }

    printf("publishing\n");

    pub_.publish(edge);	
	
  }

  public:
  zedNav():nh_(), private_nh_("~")
  {
	pub_ = nh_.advertise<sensor_msgs::Image>("right_edges",10);
	sub_ = nh_.subscribe("right_bw",10,&zedNav::callback,this);

  }
  
};

int main(int argc, char** argv)
{
	ros::init(argc,argv,"zed_nav");
	zedNav z;
	ros::spin();
	return 0;
}


