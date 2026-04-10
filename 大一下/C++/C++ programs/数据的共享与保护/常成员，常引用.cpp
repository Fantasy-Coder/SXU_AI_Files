#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	A obj(1,2);
	obj.print1();
	obj.print2();
	int x,y;
	const int i=0; 
	const int j=0; 
	void add(const int &a,int &b);
	add(x,y);//合法，常引用可以绑定常变量和非常变量 
	//add(i,j); 非法，普通引用只能绑定非常变量，不可绑定常变量 
	x++,y++;//合法，引用是常引用，不可更改，传入的数据不一定是常变量 
}
void add(const int &a,int &b)
	{
		//a++; 非法，a为常引用，不可改变a 
		b++;//合法 
	}
/*
1.h的内容
#include"iostream"
using namespace std;
class A
{
	public:
		A(int i,int j);
		void print1() const;
		void print2() const;
		void setx(int x);
	private:
		const int a;
		int x;
		static const int b;
};
A::A(int i,int j):a(i),x(j){}
void A::print1() const
{
	//setx(1);非法				//常成员函数只能调用常成员函数，不能调用非常成员函数，因为可能修改常数据成员，数据成员均可调用,但不能修改 
	cout<<"a="<<a<<endl;	
	print2();
}
void A::print2() const
{
	cout<<"x="<<x<<endl;
}
void A::setx(int x)
{
	this->x=x;
	print1();//合法 
	//a++;非法					//非常成员函数可以调用常成员，但不能修改 
}
*/
