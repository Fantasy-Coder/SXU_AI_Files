#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	circle c1,c2,c3;					//用于聚合类 
	tricircle obj(1,2,3);
	tricircle obj1;
	tricircle obj2(obj);
	cout<<"obj中三个圆的总面积为"<<obj.tarea()<<"总周长为"<<obj.tlen()<<endl<<endl;
	cout<<"请输入obj1中三个圆的半径"<<endl;
	obj1.c1.input(),obj1.c2.input(),obj1.c3.input();
	cout<<endl<<"obj1中三个圆的总面积为"<<obj1.tarea()<<"总周长为"<<obj1.tlen()<<endl<<endl;
	cout<<"obj2中三个圆的总面积为"<<obj2.tarea()<<"总周长为"<<obj2.tlen()<<endl<<endl;
	ptricircle obj3;
	obj3.p1=&c1,obj3.p2=&c2,obj3.p3=&c3;
	cout<<"请输入聚合类obj3中所指向的圆的半径"<<endl;
	c1.input(),c2.input(),c3.input();
	cout<<endl<<"obj3中三个圆的总面积为"<<obj3.tarea()<<"总周长为"<<obj3.tlen()<<endl; 
}

/*
1.h中内容
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

void circle::input()
{
	cin>>r;
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

class tricircle					//类的组合 
{
	public:
		circle c1,c2,c3;		//属于circle类的对象成员 
		double tarea();			//求总面积 
		double tlen();			//求总周长 
		tricircle(double a,double b,double c);		//组合类对象的构造函数，先调用对象成员所属类的构造函数，初始化对象成员，先声明先初始化，再初始化非对象成员
													//因为不确定对象的下级成员的权限，所以采用初始化列表，语法形式，组合类构造函数名（形参列表）：对象成员名1（形参1），对象成员名2（形参2）...... {初始化其他非对象成员}
		tricircle();
		tricircle(tricircle &y);
		~tricircle();								//组合类对象的析构函数，先析构非对象成员，再析构对象成员 
};

tricircle::tricircle(){};													//无参构造函数 
tricircle::tricircle(double a,double b,double c):c1(a),c2(b),c3(c){};			//有参构造函数, 调用顺序，先调用内嵌对象的构造函数，再执行本类构造函数的函数体 
tricircle::tricircle(tricircle &y):c1(y.c1),c2(y.c2),c3(y.c3){};						//拷贝构造函数 
tricircle::~tricircle(){};																						//析构函数析构顺序与构造函数相反

double tricircle::tarea()
{
	double totalarea;
	totalarea=c1.area()+c2.area()+c3.area();			//多级访问受到多级权限的控制，语法形式：组合类对象名.对象成员名.对象成员的下级成员名 
	return totalarea;
}

double tricircle::tlen()
{
	double totallen;
	totallen=c1.len()+c2.len()+c3.len();
	return totallen;	
} 

class ptricircle										//类的聚合，包含对象指针 
{
	public:
		circle *p1,*p2,*p3;								//聚合类的对象要独立创建，聚合类对象只包含指向对象成员的指针，聚合类对象可以公用对象成员 
		double tarea();
		double tlen();
};

double ptricircle::tarea()
{
	double totalarea;
	totalarea=p1->area()+p2->area()+p3->area();
	return totalarea;
}

double ptricircle::tlen()
{
	double tlen;
	tlen=p1->len()+p2->len()+p3->len();
	return tlen;
} 
*/