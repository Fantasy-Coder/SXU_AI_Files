#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	derived obj(1,2,3,4);
}
/*
1.h的内容
#include"iostream"
using namespace std;
class base1
{
	public:
		base1(int i){cout<<"Construction base 1 is called......"<<i<<endl;}			//派生类构造函数执行：（1）调用基类构造函数，按照被声明的顺序,虚基类最先被够制造
		~base1(){cout<<"Deconstructor base1 is called"<<endl;}						//					  							（2）对派生类新增成员进行初始化，按照被声明的顺序 
};																					                                                 //										    （3）执行派生类的构造函数体中的内容
class base2																												//析构函数调用顺序与构造函数相反 
{
	public:
		base2(int i){cout<<"Construction base 2 is called......"<<i<<endl;}
		~base2(){cout<<"Deconstructor base2 is called"<<endl;}
};
class base3
{
	public:
		base3(){cout<<"Construction base 3 is called......"<<endl;}
		~base3(){cout<<"Deconstructor base3 is called"<<endl;}
};
class derived:public base2,public base1,public base3
{
	public:
		derived(int a,int b,int c,int d):base1(a),number2(b),number1(c),base2(b)
		{
			cout<<"Constructor derived is called"<<endl;
		}
		base1 number1;
		base2 number2;
		base3 number3;
};
*/
