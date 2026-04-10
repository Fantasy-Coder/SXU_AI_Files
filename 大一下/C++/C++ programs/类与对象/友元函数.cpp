#include"iostream"
#include"1.h"
using namespace std;
int main()
{	A obj;
	fun1();
}

/*
1.h中内容
#include"iostream"
using namespace std;
class A
{
	public:
		int x;
		A(int a,int b,int c);
		A();	
	friend void fun1();			//声明fun1为类A的友元函数 （1）友元的声明部分可以在任意位置（2）友元函数时类外的其他的函数，不是类的成员（3）友元函数体中可以访问该类对象的所有成员，不受权限约束 
	protected:
		int y;
	private:
		int z;
	
	};

A::A(int a,int b,int c)
{
	x=a;
	y=b;
	z=c;
}
A::A(){};

void fun1()
{
	A obj(2,4,6);
	cout<<obj.x<<"	"<<obj.y<<"	"<<obj.z<<endl;
}
*/
	
/*
class B
{
	friend class A;				//声明A类是B的友元类，即A类中所有函数成员都可以调用B中的所有对象，不受权限约束
	friend void A::fun1();		//声明A类中的函数成员fun1为类B的友元函数	
}								//友元关系是单向的，且友元关系不能传递 
*/