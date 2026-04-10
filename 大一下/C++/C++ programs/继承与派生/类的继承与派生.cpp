#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	boardcircle obj;
	cout<<"请输入圆的半径和边框宽度"<<endl;
	obj.input();
	cout<<"圆的面积为"<<obj.area()<<"圆的周长为"<<obj.len()<<endl;
	cout<<"内圆的面积为"<<obj.innerarea()<<"内圆的周长为"<<obj.borderarea()<<endl;
}

/*
1.h的内容
#include"iostream"
using namespace std;
class circle
{
	private:
		double r;
	public:
		void input();				//输入半径 
		double getradius();			//读取半径
		double area();				//求面积
		double len();				//求周长 
		circle();
		circle(double x);
		circle(circle &x);
};

void circle::input()				//公有继承：派生类的公有成员和保护成员可以直接访问，类族之外可通过派生类的对象直接访问基类的公有成员，无论是派生类成员还是派生类的对象都无法直接访问基类的私有成员 
{												//私有继承：派生类的公有成员和保护成员可以直接访问，类族之外的对象无法直接访问，无论是派生类成员还是派生类的对象都无法直接访问基类的私有成员 
	cin>>r;								//保护继承：派生类的其他成员可以直接访问基类的公有成员和保护成员，但类外部的派生类对象无法直接访问，无论是派生类成员还是派生类的对象都无法直接访问基类的私有成员 
	do
	{
		if(r>0)
		{
			break;
		}
		else
		{
			cout<<"输入的数据有误，请重新输入"<<endl; 
			cin>>r;
		}
	}while(1);
}

double circle::getradius()
{
	return r;
}

double circle::area()
{
	return (3.14*r*r);	
} 

double circle::len()
{
	return (3.14*2*r);
}

circle::circle(){};
circle::circle(double x)
{
	r=x;	
}
circle::circle(circle &x)
{
	r=x.r;	
}

class boardcircle :public circle			//类的继承语法    class派生类名：继承方式（public,在派生类中的访问权限与在基类中相同；protected，基类中public成员变为protected，基类中protected和private权限保持不变；private，对基类中成员做全封装，都变为private）    
{											//					派生类将基类中的所有函数成员和数据成员，除了构造成员与析构成员，需要重新编写，且对基类成员重新封装 
											//					保护权限的作用，属于半开放，只对派生类的函数成员开放，但对类外的所有函数都是隐藏的    类的保护权限是向其派生类定向开放的一种权限 
											//					派生类的保护继承是向其下级定向开放的一种半封装 
	public:
		double w;				//边框宽度 
	double innerarea();			//求内圆面积 
	double borderarea();		//求边框面积 
	void input();				//输入半径和边框宽度，可以和继承类中的函数重名，但不是重载函数，若重名新增成员将覆盖基类成员 
	boardcircle(double a,double b);			//有参构造函数 
	boardcircle(boardcircle &obj);			//拷贝构造函数 
	boardcircle();							//无参构造函数 
}; 

boardcircle::boardcircle(double a,double b):circle(a)			//派生类对象的构造函数，语法形式   派生类构造函数名（形参列表）：基类名1（形参1），基类名2（形参2）,...... {......函数体中初始化新增成员}
{
	w=b;														//a为半径，b为边框宽度 
}
boardcircle::boardcircle(boardcircle &obj):circle(obj)			//拷贝构造函数，派生类已经定义的obj，其中的边框长度w给新定义的派生类 
{
	w=obj.w;
}
boardcircle::boardcircle(){};

double boardcircle::innerarea()
{
	double x=getradius();
	return (3.14*(x-w)*(x-w));
}

double boardcircle::borderarea()
{
	return (area()-innerarea());
}

void boardcircle::input()
{
	do{
		circle::input();			//输入半径 
		cin>>w;						//输入边框宽度 
	  if(getradius()<w)
	  {
	  	cout<<"输入的数据有误，请重新输入"<<endl; 
	  }
	  else
	  {
	  	break;
	  }
	  }while(1);
}
*/
