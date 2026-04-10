#include"iostream"
using namespace std;
int main()
{
	int a=0,b=0;
	const int *p1=&a;//定义常量指针 
	int *const p2=&b;//定义指针常量 
	//*p1=1; 非法，常量指针不可修改所指对象 
	a=1;// 合法，a可以不为常亮 
	p1=&b;// 合法，常量指针可以重新指向新对象、
	*p2=1;// 合法，指针常量可以修改所指对象 
	//p2=&a; 非法，指针常量只能进行一次赋值，不能进行修改指向新对象 
}
