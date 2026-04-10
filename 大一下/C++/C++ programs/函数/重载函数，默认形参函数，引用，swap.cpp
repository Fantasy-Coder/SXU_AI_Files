#include"iostream"
using namespace std;
int max(int,int b=1);			//带默认形参的函数，声明时就要赋值，且在不带默认形参的后面 
int max(int,int,int);			//重载函数 
int swap1(int &x,int &y);
int main()
{
	int a(1),b(2),c(3),Max;
	Max=max(a,b);
	cout<<"max(a,b)调用	"<<Max<<endl;
	Max=max(a);
	cout<<"max(a,b=1),带默认形参调用	"<<Max<<endl;
	Max=max(a,b,c);
	cout<<"max(a,b,c)调用	"<<Max<<endl;
	
	cout<<endl<<"引用"<<endl;
	int x(1);
	const int &x1=x;			//定义成常引用后，x1的值不可改变 
	cout<<x1;					//引用只能在初始化时候指定被引用的对象，其后不能更改 
	int y;
	x++;						//但可以通过改变x的值改变x1的值 
	cout<<endl<<x<<endl;
	
	cout<<endl<<"swap函数"<<endl;
	int a1=1,a2=2;
	swap1(a1,a2);
	cout<<"a1="<<a1<<",a2="<<a2;
}

int max(int a,int b)
{
	return a>b?a:b;
}

int max(int a,int b,int c)
{
	return (c>(a>b?a:b)?c:(a>b?a:b));
}

int swap1(int &x,int &y)		//不引入中间变量，调换x和y的值 
{
	x=x^y;
	y=y^x;
	x=x^y;
//	x=x+y;
//	y=x-y;
//	x=x-y;
}
