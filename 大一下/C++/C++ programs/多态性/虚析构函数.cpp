#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	base *b=new derived();
	fun(b);
}
/*
1.h的内容
#include"iostream"
using namespace std;
class base
{
	public:
		virtual ~base(){cout<<"Base deconstructor is called"<<endl;}  //如果一个类得析构函数是虚函数，那么它派生而来的所有子类的析构函数也是虚函数，可使用指针类的动态绑定 
};
class derived:public base
{
	public:
		derived(){p=new int(0);}	
		~derived(){cout<<"Derived deconstructor is called"<<endl; delete p;}
	private:
		int *p;
};

void fun(base *b)//若通过基类指针调用对象的析构函数（通过delete），需要让基类的析构函数成为虚函数，否则可能无法调用 
{
	delete b;
} 
*/
