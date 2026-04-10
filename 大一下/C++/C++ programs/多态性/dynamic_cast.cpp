#include"iostream"
using namespace std;
class base
{
	public:
		virtual void fun1(){cout<<"base::fun1()"<<endl;}
		virtual ~base(){}
};
class derived1:public base
{
	public:
		virtual void fun1(){cout<<"derived1::fun1()"<<endl;}
		virtual void fun2(){cout<<"derived1::fun2()"<<endl;}
};
class derived2:public derived1
{
	public:
		virtual void fun1(){cout<<"derived2::fun1()"<<endl;}
		virtual void fun2(){cout<<"derived2::fun2()"<<endl;}
};
void fun(base *b)
{
	b->fun1();
	derived1* d=dynamic_cast<derived1*>(b);//dynamic_cast可将积累指针显示转换为派生类的指针或引用，但是有条件的，需类型兼容才允许转换，否则返回空指针 
	if(d!=0)//转换成功才调用fun2函数，否则d返回的是空指针 
	{
		d->fun2();
	}
}
int main()
{
	base b;
	fun(&b);//因为fun2是derived中新引入的函数，只能对derived1和derived2调用 
	derived1 d1;
	fun(&d1);
	derived2 d2;
	fun(&d2);
}