#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	void shapeinfo(shape *pobj);				//显示面积和周长的信息，利用虚函数调用时的多态性，circle和rectangle中都重写了虚函数area()和len()，将调用circle和rectangle中的函数 
	circle cobj(2);
	rectangle robj(2,3);
	shapeinfo(&cobj);
	shapeinfo(&robj);
}

void shapeinfo(shape *pobj)
{
	pobj->show();
	cout<<"的面积为 "<<pobj->area()<<" 周长为 "<<pobj->len()<<endl;	
}

/*
1.h的内容
#include"iostream"
using namespace std;
class shape
{
	public:
		virtual double area()=0;		//只定义，未声明的函数成员称为纯虚函数 				（1）不能用抽象类定义对象，但可以定义抽象类的引用，对象指针 （2）抽象类可以作为基类定义派生类 
		virtual double len()=0;			//								（3）派生类继承纯虚函数成员时，只是继承其函数原型，需为纯虚函数成员编写函数体代码，实现纯虚函数成员，派生类实现了所有纯虚函数成员后，则变为一个普通的类，可以实例化	
		virtual void show()=0;			//	抽象类的应用：（1）同一类族接口，使类族中所有派生类都具有相同的接口  （2）重用代码，利用虚函数调用时的多态性，让类族中所有派生类对象可以重用相同的代码
};										 

										
class circle:public shape
{
	public:
		double r;
		double area()
			{
				return (3.14159*r*r);			
			}
		double len()
			{
				return (3.14*2*r);
			}
		void show()
			{
				cout<<"圆形"; 
			}
		circle();
		circle(double x);	
};
circle::circle(){};
circle::circle(double x)
{
	r=x;
}

class rectangle:public shape		
{
	public:
		double a,b;
		double area()
			{
				return (a*b);
			}
		double len()
			{
				return (2*(a+b));
			}
		void show()
			{
				cout<<"矩形";
			}
		rectangle();
		rectangle(double x,double y);	
};
rectangle::rectangle(){};
rectangle::rectangle(double x,double y)
{
	a=x,b=y;
} 
*/