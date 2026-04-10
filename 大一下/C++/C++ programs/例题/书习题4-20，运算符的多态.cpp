#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	complex c1(1,2),c2(2,3);
	c1.show();
	c1.add(c2);
	c1.show();
	complex c3;
	c3=2;
	c3.show();
}
/*1.hµÄÄÚÈÝ
#include"iostream"
using namespace std;
class complex
{
	private:
		double real,image;
	public:
		void add(complex &x);
		void show();
		int getreal();
		int getimage();
		complex(int,int);
		complex();
		complex operator =(int);
};
complex::complex(int a,int b)
{
	real=a;
	image=b;
}
complex::complex(){}
void complex::show()
{
	cout<<real<<"+"<<image<<"i"<<endl;
}
int complex::getreal()
{
	return real;
}
int complex::getimage()
{
	return image;
}
void complex::add(complex &x)
{
	this->real=this->real+x.getreal();
	this->image=this->image+x.getimage();
}
complex complex::operator = (int a)
{
	this->real=a;
	this->image=0;
	return *this;
}
*/ 
