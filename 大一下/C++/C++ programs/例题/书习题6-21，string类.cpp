#include"iostream"
#include"string"
using namespace std;
void f(const string &st,int i)
{
	int count=1,t=0;
	while(t<i)
	{
		if(st[t]==' ')
		{
			count++;
		}
		t++;
	}
	cout<<"The number of words are "<<count;
}
int main()
{
	int i,t=0;
	string st;
	cout<<"please input a sentence:";
	getline(cin,st);//用getline(cin,string,'分隔的符号')，来使字符串读入空格或回车等特殊符号 
	i=st.size();//size返回字符串大小 
	f(st,i);
}
