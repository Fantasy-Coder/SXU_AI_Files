#include"iostream"
using namespace std;
int f(int a,int b)
{
	int t,i,k=1;
	if(a>b)
	{
		k=a%b;
		if(k!=0)
		{
		while(k!=0)
		{
			t=a%b;
			a=b;
			b=t;
			k=a%b;
			if(k==0)
			{
				return t;
			}
		}
		}
		else
		{
			return b;
		}
	}
	else
	{
		k=b%a;
		if(k!=0)
		{
		while(k!=0)
		{
			t=b%a;
			b=a;
			a=t;
			k=b%a;
			if(k==0)
			{
				return t;
			}
		}
		}
		else
		{
			return a;
		}
	}
}
int main()
{
	int a=8,b=6,x;
	x=f(18,6);
	cout<<x;
}