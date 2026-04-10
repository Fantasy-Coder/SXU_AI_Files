#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	rectangle rect;
	rect.input();
	rect.output();
}

/*  1.h内容 
#include"iostream"
using namespace std;
class rectangle					//定义类 
{
	private:
		int a;
		int b;
		int squar(int,int);
		int len(int,int);
	public:
		void input();				//在类的成员数中，可以访问到类的全部成员
		void output(); 
};

void rectangle::input()					//定义函数内容 
{
	cin>>rectangle::a>>rectangle::b;
}

void rectangle::output()
{
	cout<<squar(a,b)<<endl;
	cout<<len(a,b)<<endl;
}
int rectangle::squar(int a,int b)
{
	return a*b;
}

int rectangle::len(int a,int b)
{
	return 2*(a+b);
}
*/ 
