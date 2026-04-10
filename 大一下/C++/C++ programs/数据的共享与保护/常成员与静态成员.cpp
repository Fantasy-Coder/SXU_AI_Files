#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	double totalcost=0;
	double r1,r2;
	cin>>r1>>r2;
	circlepool pool1(1,1),pool2(1,1);
//	pool1.setprice(10);
	pool1.setradius(r1);
	totalcost+=pool1.getcost();
//	pool2.setprice(10);
	pool2.setradius(r2);
	totalcost+=pool2.getcost();
	cout<<totalcost<<endl;
	return 0;
}

//1.h中内容
 
#include"iostream"
using namespace std;
namespace					//匿名命名空间，没有名字，在一个源文件中无法访问其他源文件的匿名命名空间，只能本文件使用
{
	int i,j;							//具有命名空间作用域的变量也称为全局变量
}
class circlepool
{
	private:
		const double price;			//用const，声明时不能赋初值 
		static double r;			//static声明时不能初始化		
	public:
		circlepool(double p1,double p2):price{10}			//通过构造函数后的初始化列表对const进行赋值，形式为  构造函数名(形参列表）:常数据成员名1（形参1）,......
		{
			//price=p1;
			r=p2;
		}
		/*void setprice(double x)
		{
			if(x<=0)
			{
				price=0;
				cout<<""<<endl;
			}
			else 
			{
				price=x;
			}
		}*/
		double getprice() const;				//常函数成员，只能读取类中的数据成员，不能赋值修改，常函数成员只能调用其他常函数成员 
		void setradius(double x);
		static double getradius();				//静态函数成员只能访问类中的静态数据成员，不能定义成内敛函数 
		double getcost();
};

double circlepool::r=1;			//必须在类声明的大括号外面对静态成员进行定义初始化 

double circlepool::getprice() const			//函数实现部分也要加上const关键字 
{
	return price;
}

void circlepool::setradius(double x)
{
	if(x<=0)
	{
		r=0;
		cout<<""<<endl;
	}
	else
	{
		r=x;
	}
}
		
double circlepool::getradius()		//函数实现部分不用加上static关键字 
{
	return r;
}

double circlepool::getcost()
{
	return (3.14*r*r*price);
}
