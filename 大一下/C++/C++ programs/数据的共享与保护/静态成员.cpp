#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	point::showpoint();
	point p1(1,1);
	showpoint(p1);//通过类名调用 
	point p2(2,2);
	p2.showpoint(&p2);//通过传入地址调用 
	point p3(3,3);
	p3.showpoint(&p3);
}
/*
1.h的内容
#include"iostream"
using namespace std;
class point
{
	private:
		int x,y;
		static int count;		//静态数据成员，属于整个类，不属于任何一个对象，实现了同一类的不同对象之间的数据共享，调用时可用  类名::标示符 
	public:
		point(int,int);	
		~point();
		static void showpoint(point*p=NULL);	//静态函数成员，只能调用静态数据成员，若要调用非静态数据成员可以用指针或者类名 
		static void showpoint(point&);			//静态函数成员的调用是没有目的对象的，所以只能隐含的通过目的对象访问非静态成员 
};
int point::count=0;				//静态数据成员的初始化，利用类名和变量类别 
point::point(int x,int y)
{
	this->x=x;
	this->y=y;
	count++;
}
point::~point(){}
void point::showpoint(point *p)	//通过指针调用非静态成员 
{
	cout<<"count="<<count<<endl;	//可以直接调用静态成员count 
	if(p!=NULL)
	{
		cout<<"x="<<p->x<<",y="<<p->y<<endl;		
	}
}
void point::showpoint(point&p)	//通过类名调用非静态成员 
{
	cout<<"count="<<count<<endl;
	cout<<"x="<<p.x<<",y="<<p.y<<endl;	
} 
*/
