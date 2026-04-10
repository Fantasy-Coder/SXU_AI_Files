#include"iostream"
using namespace std;

template<typename T> //类模版A							//定义类模版 语法  		template<类型参数列表> 
class A				//类声明部分						//						   class 类名 {类成员声明}				
{														//						   template<类型参数列表>	
	private:											//							函数类型  类名<类型参数列表>::函数名(形参列表) {函数体} 
		T a1;											//类模版的编译原理：类模版是具有类型参数的类，首先按照给定的实际数据类型对类模版进行实例化，用实例类定义所要的对象 
		int a2;
	public:
		A(T p1,int p2);
		T sum();
		void show();
};
template<typename T>//类实现部分
A<T>::A(T p1,int p2)//构造函数 
{
	a1=p1;
	a2=p2;
}
template<typename T>
T A<T>::sum()		//求数据成员和 
{
	return (T)(a1+a2);
}
template<typename T>
void A<T>::show()
{
	cout<<a1<<" "<<a2<<endl;
}

template<typename T,typename TT>//新增类型参数 
class B:public A<T>	//派生类B，公有继承类模版A 
{
	private:
		TT b;//新增数据成员 
	public:
		B(T p1,TT p2):A<T>(p1,p2)
		{
			b=p2;
		}
		void show()
		{
			A<T>::show();
			cout<<"b="<<b<<endl;
		}
};

int main()
{
	A<double> obj1(1.1,2);								//使用类模版定义对象时需要明确给出类型参数所指代的实际数据类型 
	obj1.show();
	cout<<endl;
	A<int> obj2(1,2);
	obj2.show();
	cout<<endl;	
	typedef A<double> doubleA;							//可用typedef显式地实例化类模版		生成实例类doubleA,可用doubleA定义类的对象 
	doubleA obj3(1.2,2);
	obj3.show();
	cout<<endl<<"派生类模板"<<endl;						
	B<double,int> obj4(1.3,2);							//使用派生类模板定义对象时，需给出T和TT的实际数据类型 
	obj4.show();
}