#include"iostream"
#include"string.h"
using namespace std;

class error																				//使用类描述异常，类类型的异常可以提供更多的异常信息和异常处理功能 
{
	public:
		int errcode;
		char msg[100];
		error(int code,char msge[100])
		{
			errcode=code;
			strcpy(msg,msge);
		}
		void show()
		{
			cout<<msg<<endl<<"异常代码："<<errcode<<endl; 
		}
};
int div(int n)
{
	if(n==0)
		{
			throw (-1);//异常处理流程，抛出异常，然后退出当前函数的执行					//throw 异常表达式	异常表达式结果的数据类型备用于区分不同类型的异常，结果的值被用于描述异常的详细信息 
		}
	if(n<0)
		{
			error err(-2,"输入的数不能为负数");
			throw (err);
		}
	return 100/n;
}

int main()
{
	int n;
	cin>>n;
	try
	{
		int result=div(n);
		cout<<"100/"<<n<<"="<<result<<endl;	
	}		
	catch(int x)//x为形参，可接受throw语句中异常表达式的结果							//catch子句负责捕获异常，每个catch子句只负责一种类型的异常，异常类型为throw语句中表达式结果的类型 
	{
		cout<<"输入的数不能为0"<<endl;
		cout<<"异常代码："<<x<<endl;
	}
	catch(error e)
	{
		e.show();
		cout<<endl;
	}
	catch(...)																			//catch(...)可匹配并捕获任意类型的异常，其后面的catch子句都是无效子句，一班catch(...)放在最后 
	{
		cout<<"发生了其它异常"<<endl;
	}
}