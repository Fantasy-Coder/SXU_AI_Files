#include"iostream"
#include"iomanip"
using namespace std;
int main()
{
	cout<<"get使用演示"<<endl;
	char ch;
	while(true)
	{
		ch=cin.get();						//get的使用，每次从流缓冲区中读出1个字符 
		if(ch=='\n')
		{
			break;	
		}
		if(ch>='a'&&ch<='z')
		{
			ch-=32;
		}
		if(ch==' ')
		{
			ch='*';
		}
		cout<<ch;
	}
	
	fflush(stdin);
	cout<<endl<<endl<<"width使用演示"<<endl;
	
	char str1[10];							//数组越界，width的使用，设置下一个输入项最大字符个数为5（包含字符串结束符） 
	cin.width(5);			
	cin>>str1;
	cout<<str1<<endl;
	cin>>str1;
	cout<<str1;
	
	fflush(stdin);
	cout<<endl<<endl<<"put使用演示"<<endl;
	
	char ch1,str[]="abcd";
	int n=0;
	while(str[n]!='\0')
	{
		ch1=str[n];
		cout<<ch1;
		cout.put(ch1-32);
		n++;	
	} 
		
	fflush(stdin);
	cout<<endl<<endl<<"设置输出位数及填充字符演示"<<endl;
	
	char *name[2]={"手电筒","电池"};
	double price[]={10,20};
	cout.fill('#');						//位数不足部分补#，cout.fill改变填充字符 
	cout.width(8);	cout<<name[0];
	cout.width(6);	cout<<price[0];
	cout<<endl;
	cout.width(8);	cout<<name[1];
	cout.width(6);	cout<<price[1]; 
	
	fflush(stdin);
	cout<<endl<<endl<<"设置浮点数的输出格式演示"<<endl;	
	double x=12.3456;
	cout.flags(ios::fixed);				//定点表示法 
	cout.precision(2);					//保留2位小数
	cout<<x<<endl;
	cout<<resetiosflags(ios::fixed);	//取消定点格式 
	cout<<setiosflags(ios::scientific)<<setprecision(8)<<x; 	//科学表示法，保留8位小数 
}