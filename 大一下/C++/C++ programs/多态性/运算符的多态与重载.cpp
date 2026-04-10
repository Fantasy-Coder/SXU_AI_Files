#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	complex c1(1,2),c2(2,3),temp;
	cout<<"复数c1与c2相加的结果为 "; 
	(c1+c2).show();//同c3=c1+c2;c3.show() 
	++c1;
	cout<<"c1前置++的运算结果为 ";
	c1.show(); 
	cout<<"c2后置++的运算结果为 "; 
	temp=c2++;
	temp.show();
	cout<<"运算后c2的结果为 ";
	c2.show();
	if(c1==c2)
	{
		cout<<"c1与c2相等"<<endl;
	}
	else
	{
		cout<<"c1与c2不相等"<<endl;
	}
} 
/*
1.h的内容
#include"iostream"
using namespace std;
class complex													
{
	private:																							
		double real,image;
																				//重载为复数类的函数成员 	类重载运算符，实现类运算，重载运算符使用函数的形式来重新定义运算符的运算规则
																              	//语法规则      函数类型 operator 运算符 (形式参数){函数体}				 
	public:
		complex(double x,double y);
		complex();
		complex(complex &c);
		void show()
		{
			cout<<real<<"+"<<image<<"i"<<endl;
		}
		complex operator+(complex c)	//此处函数返回值不用引用，为了防止改变原本元素	//接受一个复数类对象c，再将其实部和虚部分别加到当前对象的实部和虚部,在返回复数类对象result 
		{
			complex result;
			result.real=this->real+c.real;								//用函数成员，+是函数成员名，调用时相当于 c1+(c2),c1为对象名，c2是实参 
			result.image=this->image+c.image;
			return result;
		}								
		complex &operator++()										//实现前置++的运算符的函数成员      结果是一个复数类的引用,用&，相当用引用传递，是双向传递的 
		{
			this->real++;
			this->image++;
			return *this;											//this是指向当前对象的对象指针 ，*this是将当前对象的引用作为函数的返回值 
		}
		complex operator++(int)										//实现后置++运算符的函数成员 		用int形参，目的是使重名函数具有不同的形参，进行重载 
		{
			complex temp=*this;//使temp等于未++前的值 
			this->real++;
			this->image++;
			return temp;											//返回后置++表达式的结果，加1之前的对象 
		} 
		 bool operator==(complex c);								//实现关系运算符== 
};

bool complex::operator==(complex c)					//运算符重载为成员函数时，函数的形参个数比原来的操作数个数要少一个，第一个操作数会被作为函数调用为目的对象，无需出现在参数表中 
{
	return (real==c.real&&image==c.image);
}

complex::complex(double x,double y)
{
	real=x;
	image=y;
}
complex::complex():real(0),image(0){};
complex::complex(complex &c)
{
		real=c.real;
		image=c.image;	
}		


/*
class complex													
{
	private:																							
		double real,image;											//重载为复数类的友元函数 
	public:
		complex(double x,double y){real=x,image=y;}
		complex():real(0),image(0){}
		complex(complex &c){real=c.real,image=c.image;}	
		void show()
		{
			cout<<real<<"+"<<image<<"i"<<endl;
		}
		friend complex operator+(complex c1,complex c2);			//当运算符重载为非成员函数时，参数个数与原操作个数相同，运算符的所有操作数必须是显示通过参数传递 
};
complex operator+(complex c1,complex c2)
		{
			complex result;
			result.real=c1.real+c2.real;							//用友元函数,+时函数成员名，调用时相当于+(c1,c2)，c1和c2是实参 
			result.image=c1.image+c2.image;
			return result;
		}			
*/	
*/
