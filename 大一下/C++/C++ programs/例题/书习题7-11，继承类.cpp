#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	derive obj1;
	obj1.base::fun1();
	obj1.fun2();//继承后同名覆盖 
	
	derive *p=&obj1;
	p->base::fun1();
	p->fun2();
	
	derive &obj2=obj1;
	obj2.fun1();
	obj2.base::fun2();
}
/*
1.h的内容
#include"iostream"
using namespace std;
class base
{
	public:
		void fun1();
		void fun2();
		base();
};
base::base(){}
void base::fun1()
{
	cout<<"base fun1() is called "<<endl;
}
void base::fun2()
{
	cout<<"base fun2() is called "<<endl;
}

class derive:public base
{
	public:
		void fun1();
		void fun2();
		derive();
};
derive::derive(){}
void derive::fun1()
{
	cout<<"derive fun1() is called"<<endl;
}
void derive::fun2()
{
	cout<<"derive fun2() is called"<<endl;
} 
*/
