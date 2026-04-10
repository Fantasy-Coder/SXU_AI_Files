#include"iostream"
#include"string"
using namespace std;
int main()
{
	string st="Hello world",st1="smile";
	cout<<"源字符串st为："<<st<<"	st1为："<<st1<<endl;
	st.insert(1,st1);//insert函数，将st1所指向的字符串插入在本串的1位置之前 
	cout<<"字符串st的长度为："<<st.size()<<endl;//size()函数，返回字符串的长度（字符的个数） 
	cout<<"insert函数处理后的字符串为："<<st<<endl;
	cout<<"取st1中1至5号位的字符串为："<<st.substr(1,5)<<endl;//substr(int a,int b)函数,取字符串由a位置开始的后b个字符 
	cout<<"字串st1在st中第一次出现的位置为："<<st.find(st1)<<endl;//find(string x)函数，查找并返回x在本串中第一次出现的位置 
	st.swap(st1);//swap(sting x)函数，将本串与x中的字符串进行交换 
	cout<<"st与st1交换后st为: "<<st<<"	st1为: "<<st1<<endl;
	st.append(st1);//append(string x)函数，将字符串x添加在本串的末尾 
	cout<<"将st1添加在st后,字符串st为："<<st<<endl;	
	cout<<st.compare(st1)<<endl;//compare(string x)函数，比较当前字符串与x字符串的大小，按照ASCII码，返回1,0，-1 
}