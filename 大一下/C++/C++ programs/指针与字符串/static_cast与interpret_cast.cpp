#include"iostream"
using namespace std;
int main()
{
	float f=1;
	float *pf=&f;
	float &rf=f;
	int i=static_cast<int>(f);//正确，static_cast支持实体到实体之间的转换，指针与指针之间的转换，但不支持实例和指针之间的转换 
	//int *pi=static_cast<int*>(pf);//非法，虽然为指针与指针之间的转换，但源类型与目标类型不相关 
	void *vp=&f;
	int *p=static_cast<int*>(vp);//用static_cast将void指针显式转换为具体类型的指针式，一定要转换为最初void指针的指针类型

	//int x=reinterpret_cast<int>(f);//非法，reinterpret_cast不支持实体到实体之间的转换
	//int *q=reinterpret_cast<int*>(f);//非法，reinterpret_cast不支持实数转换为指针
	//float of=reinterpret_cast<float>(f);//非法，reinterpret_cast不支持实体到实体之间的转换 
	//int j=reinterpret_cast<int>(pf);//非法，reinterpret_cast不支持指针转换为实体 
	int *px=reinterpret_cast<int*>(1);//正确，reinterpret_cast支持整数转换成指针，但不支持实数转化成指针
	int &ri=reinterpret_cast<int&>(rf);//正确，reinterpret_cast支持不通类型的引用之间的转换
	int *pi=reinterpret_cast<int*>(pf);//正确，reinterpret_cast支持不同类型的指针之间的转换
}
/*
总 结

　　去const属性用const_cast。

　　基本类型转换用static_cast。

　　多态类之间的类型转换用daynamic_cast。

　　不同类型的指针类型转换用reinterpreter_cast。
*/

