#include"iostream"
#include"1.h"
using namespace std;
int main()
{
	employee obj("Mike","Chang An jie","Beijing","100000","");
	obj.display();
	obj.setname();
	obj.display();
}
/*
1.h的内容
#include"iostream"
#include"string.h"
using namespace std;
class employee
{
	private:
		string name;
		string address;
		string city;
		string email;
		char *memo;
	public:
		void setname();
		void display();
		employee(string,string,string,string,char *);
};
void employee::display()
{
	cout<<"姓名："<<name<<endl<<"地址: "<<address<<endl<<"城市: "<<city<<endl<<"邮编: "<<email<<endl; 
	int len=strlen(memo);
	if(len>0)
	{
		cout<<"备注信息: "<<memo<<endl;
	}
}
void employee::setname()
{
	cout<<"请输入名字：";
	string t;
	cin>>t;
	name=t; 
}
employee::employee(string x1,string x2,string x3,string x4,char *p)
{
	name=x1;
	address=x2;
	city=x3;
	email=x4;
	memo=p;
} 
*/
