#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	boat obj1(1);
	car obj2(2);
	int x;
	x=getweight(obj1,obj2);
	cout<<x;
}
/*
1.h的内容
#include"iostream"
using namespace std;
class car;//互相都有定义，使用前向引用声明，可以定义对象指针（都可以）或对象引用（用在函数形参中），但不能定义对象 
class boat;
class boat
{
	public:
		boat(int a);
		friend int getweight(boat &obj1,car &obj2);
	private:
		int weight;

};
class car
{
	public:
		car(int a);
		friend int getweight(boat &obj1,car &obj2);
	private:
		int weight;
	
};
boat::boat(int a)
{
	weight=a;
}
car::car(int a)
{
	weight=a;
}
int getweight(boat &obj1,car &obj2)
{
	int x;
	x=obj1.weight+obj2.weight;
	return x;	
}  
*/
