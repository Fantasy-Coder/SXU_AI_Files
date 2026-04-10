#include"iostream"
#include"typeinfo"
using namespace std;
class base
{
	public:
		virtual ~base(){}
};
class derived:public base{};
void fun(base *b)
{
	const type_info &info1=typeid(b);
	const type_info &info2=typeid(*b);
	cout<<"typeid(b):"<<info1.name()<<endl;//返回base类的指针 
	cout<<"typeif(*b):"<<info2.name()<<endl;//取*为取内容，返回base类的对象的具体类型 
	if(info2==typeid(base))
	{
		cout<<"pb pointing to a base object"<<endl;
	}
	else
	{
		cout<<"pb pointing to a derived object"<<endl;
	}
}
int main()
{
	base b;
	fun(&b);
	derived d;
	fun(&d);
	const type_info &a=typeid(int);//用typeid获取运行时类型信息，得到的是一个type_info类型的常引用 
	cout<<a.name();//type_info类有const char *name() const的函数，来获得类型名称 
}