#include <ros/ros.h>
#include <sensor_msgs/Image.h>
#include <math.h>
#define square(x) x*x

class zedBW
{
  ros::NodeHandle nh_;
  ros::NodeHandle private_nh_;

  ros::Publisher pub_r_,pub_l_;
  ros::Subscriber sub_r_,sub_l_;


  void callback_r(const sensor_msgs::Image& msg)
  {
    sensor_msgs::Image edge;
    int i,j;
    int W = msg.width, H = msg.height;
    if (msg.encoding.compare("bgr8")) {
        printf("Incorrect Image format type (not currently able to handle other than 'bgr8')\n");
        return;
    }
    edge.header = msg.header;
    edge.height = msg.height;
    edge.width = msg.width;
    edge.encoding = "mono8"; // now single color (B/W)
    edge.is_bigendian = msg.is_bigendian;
    edge.step = msg.step/3; // only have 1/3 the data in bw (no R, G, B arrays)
    std::vector <unsigned char> bw; // to hold raw bw
    std::vector <double> edges; // to hold sgm 
    
    /* Consolidate color into black and white photo */
    for (i=0;i<H;i++) {
        for (j=0;j<W;j++) {
            long sum = 0;
            int k;
            for (k=-1;k<2;k++) sum += msg.data[3*W*i + 3*j +k];
            bw.push_back(sum/3);
        }
    }

    /* Calculate dx, dy, sgm */
    int dx,dy;
    double max = 0;
    for (i=0;i<H;i++) {
        if (i==0 || i==(H-1)) { // top/bottom row
            for (j=0;j<W;j++) edges.push_back(0);
        }
        else {
            edges.push_back(0); // left column
            for (j=1;j<W-1;j++) {
                int index = W*i + j; 
                dx = bw[index+W+1] + 2*bw[index+1] + bw[index-W+1] \
                - (bw[index+W-1] + 2*bw[index-1] + bw[index-W-1]);
                dy = bw[index-W-1] + 2*bw[index-W] + bw[index-W+1]\
                - (bw[index+W-1] + 2*bw[index+W] + bw[index+W+1]);
                double sgm = sqrt(square(dx) + square(dy));
                max = (max<sgm)? sgm: max;
                edges.push_back(sgm);
            }
            edges.push_back(0); // right column
        }
    }

    /* Scale edge (sgm) data to 0 to 255 range */
    for (i=0;i<edges.size();i++) edge.data.push_back(edges[i]/max*255);
    
    /* free up data, in case */
    edges.clear();
    bw.clear(); 

    pub_r_.publish(edge); 
    
  }

  void callback_l(const sensor_msgs::Image& msg)
  {
    sensor_msgs::Image edge;
    int i,j;
    int W = msg.width, H = msg.height;
    if (msg.encoding.compare("bgr8")) {
        printf("Incorrect Image format type (not currently able to handle other than 'bgr8')\n");
        return;
    }
    edge.header = msg.header;
    edge.height = msg.height;
    edge.width = msg.width;
    edge.encoding = "mono8"; // now single color (B/W)
    edge.is_bigendian = msg.is_bigendian;
    edge.step = msg.step/3; // only have 1/3 the data in bw (no R, G, B arrays)
    std::vector <unsigned char> bw; // to hold raw bw
    std::vector <double> edges; // to hold sgm 
    
    /* Consolidate color into black and white photo */
    for (i=0;i<H;i++) {
        for (j=0;j<W;j++) {
            long sum = 0;
            int k;
            for (k=-1;k<2;k++) sum += msg.data[3*W*i + 3*j +k];
            bw.push_back(sum/3);
        }
    }

    /* Calculate dx, dy, sgm */
    int dx,dy;
    double max = 0;
    for (i=0;i<H;i++) {
        if (i==0 || i==(H-1)) { // top/bottom row
            for (j=0;j<W;j++) edges.push_back(0);
        }
        else {
            edges.push_back(0); // left column
            for (j=1;j<W-1;j++) {
                int index = W*i + j; 
                dx = bw[index+W+1] + 2*bw[index+1] + bw[index-W+1] \
                - (bw[index+W-1] + 2*bw[index-1] + bw[index-W-1]);
                dy = bw[index-W-1] + 2*bw[index-W] + bw[index-W+1]\
                - (bw[index+W-1] + 2*bw[index+W] + bw[index+W+1]);
                double sgm = sqrt(square(dx) + square(dy));
                max = (max<sgm)? sgm: max;
                edges.push_back(sgm);
            }
            edges.push_back(0); // right column
        }
    }

    /* Scale edge (sgm) data to 0 to 255 range */
    for (i=0;i<edges.size();i++) edge.data.push_back(edges[i]/max*255);
    
    /* free up data, in case */
    edges.clear();
    bw.clear(); 

    pub_l_.publish(edge); 
    
  }


  public:
  zedBW():nh_(), private_nh_("~")
  {
    pub_r_ = nh_.advertise<sensor_msgs::Image>("right_edges",10);
    pub_l_ = nh_.advertise<sensor_msgs::Image>("left_edges",10);
    sub_r_ = nh_.subscribe("/zed/right/image_raw_color",10,&zedBW::callback_r,this);
    sub_l_ = nh_.subscribe("/zed/left/image_raw_color",10,&zedBW::callback_l,this);

  }
  
};

int main(int argc, char** argv)
{
    ros::init(argc,argv,"zed_bw");
    zedBW z;
    ros::spin();
    return 0;
}


