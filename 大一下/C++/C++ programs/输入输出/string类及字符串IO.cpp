#include"iostream"
#include"sstream"
#include"string"
using namespace std;
int main()
{
	string str;									//定义字符串对象str，未初始化 
	string str1("Hello world");					//定义字符串对象的四种初始化方法 
	string str2="Hello world";
	string str3(str2);	
	char ch[]="Hello world";
	string str4(ch);
	cout<<str1<<endl;
	cout<<"str1的长度为	"<<str1.length()<<endl;													//函数length返回字符串长度 
	cout<<"str1中的ll的位置为	"<<str1.find("ll")<<endl;										//函数find查找子串的位置 
	cout<<"str1中第1个位置后的4个字符为	"<<str1.substr(1,4)<<endl;								//函数substr取出子串 
	str1.append("123");cout<<"str1后追加字符123	"<<str1<<endl;									//函数append追加字符串 
	
	str="1 9.8";
	int x;double y;
	istringstream strin(str);					//定义字符串输入流类istringstream对象strin，用str初始化 
	strin>>x>>y;								//从串流对象strin中为变量x,y输入数据
	cout<<endl<<"x="<<x<<"," <<"y="<<y<<endl;
	
	ostringstream strout;						//定义字符串输出流类ostringstream对象strout							
	strout<<"x="<<x<<","<<"y="<<y<<endl;		//向串流对象strout中输出数据 
	string str5=strout.str();					//将串流对象strout中的字符串赋值给字符串对象str5 
	cout<<str5<<endl;
}