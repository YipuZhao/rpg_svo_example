#include "svo_ros/svo_node_base.h"

int main(int argc, char **argv)
{
	for (int i=0; i<argc; ++i)
	cout << "argv[i] = " << argv[i] << endl;

  svo_ros::SvoNodeBase::initThirdParty(argc, argv);

  svo_ros::SvoNodeBase node;
  node.run();
}
