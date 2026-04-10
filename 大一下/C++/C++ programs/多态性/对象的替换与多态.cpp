#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	void setGMT(clock &robj,int hgmt,int mgmt,int sgmt);		//将小时加8 	
	watch obj;
	obj.set(8,30,0);
	cout<<"GMT时间为";	    obj.show();
	clock obj1;
	obj1=obj;													//派生类对象初始化基类对象 
	setGMT(obj1,8,30,0);
	cout<<endl<<"北京时间为"; 	obj1.show();
}
	void setGMT(clock &robj,int hgmt,int mgmt,int sgmt)		
	{
		robj.set(hgmt+8,mgmt,sgmt);
	} 
	
/*
1.h的内容
#include"iostream"
using namespace std;
class clock
{
	private:
		int hour,minute,second;
	public:
		void set(int h,int m,int s)
			{
				hour=h; minute=m; second=s;
			}
		void show()
			{
				cout<<hour<<":"<<minute<<":"<<second;
			}	
};

class watch:public clock										//Liskov替换准则：（1）派生类对象可以赋值给基类对象 （2）派生类对象可以初始化基类引用 （3）基类的对象指针可以指向派生类对象 
{																//                 使用限制，派生类必须为公有继承，通过基类对象引用，访问派生类对象，只能访问基类成员 
	public:
		int band;				//表带类型
		void show()
			{
				cout<<"watch";
				clock::show();		
			}
};

class divingwatch:public watch									//多级派生，形成类族 
{
	public:
		int depth;    			 //最大下潜深度
		void show()
			{
				cout<<"divingwatch";
				clock::show();
			}	
}; 
*/