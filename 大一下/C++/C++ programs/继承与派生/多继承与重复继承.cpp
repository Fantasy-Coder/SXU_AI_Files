#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	B bobj;
	cout<<"请输入a1和a2的值 ";
	cin>>bobj.a1>>bobj.a2;					//访问不同名的基类成员，直接使用成员名 
	cout<<"请输入基类A中a的值 ";		
	cin>>bobj.A1::a;						//访问重名的基类成员，需在成员名前加“基类名：：” 
	cout<<"请输入基类B中a的值 ";
	cin>>bobj.A2::a;
	bobj.A1::fun();
	bobj.A2::fun();	
}

/*
1.h的内容
#include"iostream"
using namespace std;
class A1
{
	public:
		int a1;
		int a;
		void fun()
			{
				cout<<"基类A "<<a1<<","<<a<<endl;
			}	
};

class A2
{
	public:
		int a2;
		int a;
		void fun()
			{
				cout<<"基类B "<<a2<<","<<a<<endl;
			}	
};
class B:public A1,public A2			//同时继承基类A1,A2 
{
	public:							//不新增成员	
};

class A3:virtual public A1			//重复继承时，不用保留多份成员拷贝的基类，在第一季派生时使用虚基类，用virtual 
{
	public:							//不新增成员 
};
class A4:virtual public A1
{
	public:							//不新增成员	
};

class B1:public A3,public A4		//A3和A4是虚基类继承A1，B1保留一份A1的成员 
{
	public:							//不新增成员 
};
*/