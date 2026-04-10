#include"iostream"
#include"string"
using namespace std;
void reverse(string &st,int i,int end,int mid)
{
	if(i==mid+1)
	{
		return;
	}
	swap(st[i],st[end]);
	i++,end--;
	reverse(st,i,end,mid);
}
int main()
{
	string st;
	getline(cin,st);
	int i,end,mid;
	i=0;
	end=st.size()-1;
	mid=(i+end)/2;
	reverse(st,i,end,mid);
	cout<<st;
}
