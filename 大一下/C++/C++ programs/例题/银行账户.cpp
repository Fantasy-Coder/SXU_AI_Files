#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	int x;
	char str[10];
	float y;
	cout<<"请输入账号，帐户名，存款金额等开户信息"<<endl;
	cin>>x>>str>>y;
	account obj(x,str,y);
	int choice;
	while(true)
	{
		cout<<" 1-存款\n 2-取款\n 3-查询余额\n 0-退出\n请选择"<<endl;
		cin>>choice;
		if(choice==0)
		{
			break;
		}
		if(choice==1)
		{
			obj.deposit();
			cout<<endl;
		}
		if(choice==2)
		{
			obj.withdraw();
			cout<<endl;
		}
		if(choice==3)
		{
			obj.show();
			cout<<endl;
		}
	}
}

//1.h内容 

#include"iostream"
#include"string.h"
using namespace std;
class account
{
	private:
		int num;
		char name[10];
		float money;
	public:	
		void deposit();
		void withdraw();
		void show();
		account(int x,char *y,float z);
}; 

account::account(int x,char *y,float z)
{
	num=x;
	strcpy(name,y);
	money=z;
}
void account::deposit()
{
	cout<<"请输入存款金额"<<endl;
	float x;
	cin>>x;
	money+=x;
	show();
}

void account::withdraw()
{
	cout<<"请输入取款金额"<<endl;
	float x;
	cin>>x;
	if(money<x)
	{
		cout<<"账户余额不足"<<endl;
	}
	else
	{
		money-=x;
	}
	show();
}

void account::show()
{
	cout<<"账号"<<num<<"的账户余额为："<<money<<"元"<<endl;
}