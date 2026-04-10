#include"iostream"
#include"1.h"
using namespace std;
int main()
{	//指向类的非静态成员的指针的演示 
	int A::*p1;//声明指向数据成员的执政，格式： 类型说明符 类名::*指针名 
	p1=&A::a;//对数据成员指针赋值，格式： 指针名=&类名::数据成员名 
	int (A::*p2)(int);//声明指向函数成员的指针，格式： 类型说明符 （类名::*指针名）（参数表）
	p2=&A::fun;//p2指向函数成员，进行赋值 
	A obj;
	A *p3=&obj;
	obj.a=1,obj.c=2;
	cout<<obj.*p1<<endl;//访问数据成员时，可用 对象名.*类成员指针名 
	cout<<p3->*p1<<endl;//也可用 对象指针名->*类成员指针名
	cout<<(p3->*p2)(1)<<endl;//调用时要用 （对象指针名->*函数成员指针名）（形参）
	
	//指向类的静态成员的指针的演示
	int *pt1=&A::x;//类的静态成员不依赖于对象，所以可以用普通指针来指向和访问静态成员
	cout<<*pt1<<endl; 
}
/*
1.h的内容
#include"iostream"
using namespace std;
class A
{
public:
    int a;
    int c;
    static int x;
    A(int i);
    A();
    int fun(int b);
};
int A::x=1;
A::A(){}
A::A(int i)
{
	a=i;
}
int A::fun(int b) 
{ 
    return ((a*c) + b); 
} 
*/
