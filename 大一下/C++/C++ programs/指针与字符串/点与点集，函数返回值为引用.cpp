#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	int count,a,i,j,k;
	cout<<"输入点的个数";
	cin>>count;
	arrpoint points(count);
	for(i=0;i<count;i++)
	{
		points.element(i).move(i+1,i+1);
	}
	cout<<"输入查询点的序号";
	cin>>a;
	points.element(a-1).showpoint(a);
} 
/*
1.h的内容
#include"iostream"
#include"cassert"
using namespace std;
class point
{
	public:
		point():x(0),y(0){}
		point(int x,int y):x(x),y(y){}
		~point(){}
		int getx() const{return x;}
		int gety() const{return y;}
		void showpoint(int a)
		{
			cout<<"第"<<a<<"个点的坐标为（"<<x<<","<<y<<")"<<endl;
		}
		void move(int x1,int y1)//给点的坐标赋值 
		{
			x=x1;
			y=y1;
		}
	private:
		int x,y;
};
class arrpoint
{
	public:
		arrpoint(int size):size(size)
		{
			points=new point[size];
		}
		~arrpoint()
		{
			delete []points;
		}
		point &element(int index)//函数值返回引用，代表返回的是元素自身，若不用引用，代表返回的是复制值 
		{
			assert(index>=0&&index<size);//防止数组越界 
			return points[index];//若不返回引用，则函数调用完后返回的元素内存会被释放，不能做到双向改变 
		}
	private:
		point *points;
		int size;
}; 
*/
