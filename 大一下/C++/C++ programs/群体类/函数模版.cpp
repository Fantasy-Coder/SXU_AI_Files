#include"iostream"
using namespace std;

template<typename T>					//定义函数模板，语法 template<类型参数列表>									类型参数是一种数据类型参数，以typename或class定义
T maxium(T x,T y)						//					 	函数类型  函数名（形参列表）{函数体} 				类型参数可以用来定义函数类型，定义局部变量，是一种通用数据类型
{										//																			不用类型实参的函数模版调用语句将生成不同类型的重载函数，调用时呈现出参数多态性 
	return (x>y?x:y);
}

int main()
{
	cout<<maxium(1,2)<<endl;
	cout<<maxium(1.1,1.0)<<endl;	
}