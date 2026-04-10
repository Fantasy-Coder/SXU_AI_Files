#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	cout<<"演示1：通过对象名分别调用虚函数fun1和非虚函数fun2"<<endl;
	A aobj;
	B bobj;
	bobj.fun1();//通过派生类成员直接访问，将访问派生类的新增成员，覆盖基类成员 
	bobj.fun2();
	cout<<endl<<"演示2：通过基类引用分别调用虚函数fun1和非虚函数fun2"<<endl;
	A &raobj=bobj;							//通过基类引用访问，调用派生类的新增成员fun1 
	raobj.fun1();
	raobj.fun2();
	cout<<endl<<"演示3：通过基类对象指针分别调用虚函数fun1和非虚函数fun2"<<endl; 
	A *paobj=&bobj;
	paobj->fun1();
	paobj->fun2(); 
}
/*
1.h的内容
#include"iostream"
using namespace std;
class A
{
	public:
		virtual void fun1();											//（1）只有在类声明部分声明虚函数，类实现部分不用加virtual  （2）基类中声明的虚函数成员被继承到派生类后，自动成为派生类的虚函数成员  （3）若派生类重写基类的虚函数成员，且函数原型一致（即函数名相同），则该函数自动成为派生类的虚函数成员 
		void fun2();													//（4）若使用基类引用或对象指针调用派生类对象的普通成员，调用的是基类成员，若调用的是虚函数成员，则调用虚函数成员  （5）通过对象名访问对象成员，将访问其新增成员（同名覆盖）			
};

void A::fun1()															//实现基类对象与派生类对象之间多态的条件：（1）基类中声明虚函数成员 （2）派生类需公有继承类 （3）通过基类的引用或对象指针调用虚函数成员 
{
	cout<<"Base class A :vitual fun1()called."<<endl;
}
void A::fun2()
{
	cout<<"Base class A :non-virtual fun2()called."<<endl;
}

class B:public A
{
	public:
	    virtual void fun1();
	    void fun2();
};

void B::fun1()
{
	cout<<"Derived class B :virtual fun1()called."<<endl;
}
void B::fun2()
{
	cout<<"Derived class B :non-virtual fun2()called"<<endl;
} 
 
*/