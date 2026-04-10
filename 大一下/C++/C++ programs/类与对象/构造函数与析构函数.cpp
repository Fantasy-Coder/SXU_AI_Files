#include"iostream"
#include"2.h"
using namespace std;
int main()
{
	student obj1("zhangsan","2017",18,"请输入备注");
	student obj2(obj1);
	cout<<obj1.age<<"	"<<obj1.ID<<"	"<<obj1.name<<"	"<<obj1.Memo<<endl;
	cout<<"***"<<endl;	
	cout<<obj2.age<<"	"<<obj2.ID<<"	"<<obj2.name<<"	"<<obj2.Memo<<endl;

}

/*
如果有student stu1(obj1),则系统自动生成默认拷贝函数，函数体为
student::student(student &obj)
{
	strcpy(name,obj.name);
	strcpy(ID,obj.ID);
	age=obj.age;
	Memo=obj.Memo;				//此种自动生成为浅拷贝，拷贝备注指针信息时，没有再分配内存，两者公用一个内存 
}
*/

/*如果要实现深拷贝，即 obj2中的备注信息Memo有自己的内存空间，则需自己写函数
student::student(student &obj) 
{
	int len=strlen(obj.Memo);
	strcpy(name,obj.name);
	strcpy(ID,obj.ID);
	age=obj.age;
	if(len<=0)
	{
		Memo=0;
	}
	else
	{
		Memo=new char [len+1];
		strcpy(Memo,obj.Memo);
	}
	cout<<"深拷贝调用"<<endl;
}
*/
/*
2.h内容 
#include"iostream"
#include"string.h"
using namespace std;
class student 
{
	public:
		char name[100],ID[100];
		char *Memo;
		int age;																				
		student(char *pname,char *pID,int iniage);						//构建重载构造函数，每一个重载函数都要声明 
		student(char *pname,char *pID,int iniage,char *pmemo);			//添加memo为备注 
		student(student &obj);															//只要定义了一个构造函数，系统将不再提供缺省构造函数
		~student();														//构建析构函数，析构函数只能有一个 
};
student::student(char *pname,char *pID,int iniage)
{
	strcpy(name,pname);
	strcpy(ID,pID);
	age=iniage;
	cout<<"student::student(char *pname,char *pID,int iniage)called"<<endl;
}
student::student(char *pname,char *pID,int iniage,char *pmemo)
{
	int len=strlen(pmemo);
	strcpy(name,pname);
	strcpy(ID,pID);
	age=iniage;
	if(len<=0)	
	{
		Memo=0;
	}
	else					//如果有备注则录入 
	{
		Memo=new char[len+1];
		strcpy(Memo,pmemo);
	}
	cout<<"student::student(char *pname,char *pID,int iniage,char *pmemo)called"<<endl;
}
student::student(student &obj) 
{
	int len=strlen(obj.Memo);
	strcpy(name,obj.name);
	strcpy(ID,obj.ID);
	age=obj.age;
	if(len<=0)
	{
		Memo=0;
	}
	else
	{
		Memo=new char [len+1];
		strcpy(Memo,obj.Memo);
	}
	cout<<"深拷贝调用"<<endl;
}

student::~student()
{
	if(Memo!=0)
	{
		delete []Memo;
	}
	cout<<"~student()called"<<endl;
}
*/