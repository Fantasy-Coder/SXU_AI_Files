#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	derived obj;
	obj.fun();					//同名覆盖 
	obj.fun(1);
	obj.base1::fun();
	obj.base1::base0::fun();	//作用域分辨符，  类名::成员名（参数表） 
}
/*
1.h的内容
#include"iostream"
using namespace std;
class base0
{
	public:
		void fun(){cout<<"base0 function is called"<<endl;}
};
class base1:public base0
{
	public:
		void fun(){cout<<"base1 function is called"<<endl;}
};
class base2
{
	public:
		void fun(int i){cout<<"base2 function is called......"<<i<<endl;}
};
class base3
{
	public:
		void fun(){cout<<"base3 function is called"<<endl;}
};
class derived:public base1,public base2
{
	public:
		void fun(){cout<<"derived function is called"<<endl;}
		using base2::fun;		//可以通过使用using来使基类的成员不会被覆盖，构成重载 
}; 
*/
