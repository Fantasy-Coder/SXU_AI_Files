#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	point p,q(100,100);
	line l1(100,200,300,400);
	l1.showpoint();
	cout<<"l1的距离="<<l1.getdist()<<endl;
	line l2(p,q);
	l2.showpoint();
	cout<<"l2的距离"<<l2.getdist()<<endl;
} 

/*1.h的内容
#include"iostream"
#include"math.h"
using namespace std;
class point
{
	private:
		int x,y;
	public:
		point(int x,int y);
		point(point &);
		point();
		int getx();
		int gety();
		void setx(int);
		void sety(int);
		~point();
};
int point::getx()
{
	return x;
}
int point::gety()
{
	return y;
}
point::point(int x,int y)
{
	this->x=x;
	this->y=y;
	cout<<"point constructor1 called"<<endl;
}
point::point(point &p)
{
	x=p.x;
	y=p.y;
	cout<<"point constructor2 called"<<endl;
}
point::point()
{
	x=0;
	y=0;
	cout<<"point constructor3 called;"<<endl;
}
void point::setx(int a)
{
	x=a;
}
void point::sety(int b)
{
	y=b;
}
point::~point()
{
	cout<<"point deconstructor called"<<endl;
}

class line
{
	private:
		point p1,p2;
		double dist;
	public:
		line(int x1,int y1,int x2,int y2);
		line(point,point);
		double getdist();
		void showpoint();
		~line();
};
line::line(int x1,int y1,int x2,int y2):p1(x1,y1),p2(x2,y2)
{
	double x=x1-x2;
	double y=y1-y2;
	p1.setx(x1),p1.sety(y1);
	p2.setx(x2),p2.sety(y2);
	dist=sqrt(x*x+y*y);
	cout<<"line constructor1 called"<<endl;
}
line::line(point xp1,point xp2):p1(xp1),p2(xp2)//类的组合，传入point类，初始化line中point,调用四次拷贝构造函数，传入形参调用两次，用形参初始化p1,p2调用两次 
{
	double x=p1.getx()-p2.getx();
	double y=p1.gety()-p2.gety();
	dist=sqrt(x*x+y*y);
	cout<<"line constructor2 called"<<endl;
}
double line::getdist()
{
	return dist;
}
void line::showpoint()
{
	cout<<"p1("<<p1.getx()<<","<<p1.gety()<<")"<<endl;
	cout<<"p2("<<p2.getx()<<","<<p2.gety()<<")"<<endl;
}
line::~line()
{
	cout<<"line deconstructor called"<<endl;
}*/ 
