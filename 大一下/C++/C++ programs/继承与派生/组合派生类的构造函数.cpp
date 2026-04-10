#include"iostream"
using namespace std;
class A1
{
	public:
		int a1;
		A1(int x=0){a1=x;}
};
class A2
{
	public:
		int a2;
		A2(int x=0){a2=x;}
};
class B1
{
	public:
		int b1;
		B1(int x=0){b1=x;}
};
class B2
{
	public:
		int b2;
		B2(int x=0){b2=x;}
};
									//组合派生类的构造函数 
class C:public A1,public A2			//继承基类A1,A2 
{
	public:
		B1 bobj1,bobj2;				//组合类，类B1的对象成员bobj1,bobj2 
		int c;	
		C(int p1,int p2,int p3,int p4,int p5):A1(p1),A2(p2),bobj1(p3),bobj2(p4)				//组合派生类的构造函数，构造顺序：初始化基类成员，新增对象成员，新增非对象成员 
		{																					//初始化列表中，初始化继承基类成员用的是类名，初始化对象成员用的是对象名 
			c=p5;	
		}	
};